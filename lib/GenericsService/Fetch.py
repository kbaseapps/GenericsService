import json
import logging
import re
import traceback

import pandas as pd

from installed_clients.WorkspaceClient import Workspace as workspaceService

GENERICS_TYPES = ['FloatMatrix2D', 'Attribute']  # add case in convert_data for each additional type


class Fetch:
    def _find_between(self, s, start, end):
        """
        _find_between: find string in between start and end
        """

        return re.search('{}(.*){}'.format(start, end), s).group(1)

    def _find_type_spec(self, obj_type):
        """
        _find_type_spec: find body spec of type
        """
        obj_type_name = self._find_between(obj_type, '\.', '\-')

        type_info = self.wsClient.get_type_info(obj_type)
        type_spec = type_info.get('spec_def')

        type_spec_list = type_spec.split(obj_type_name + ';')
        obj_type_spec = type_spec_list[0].split('structure')[-1]
        logging.debug('Found spec for {}\n{}\n'.format(obj_type, obj_type_spec))

        return obj_type_spec

    def _find_generics_type(self, obj_type):
        """
        _find_generics_type: try to find generics type in an object
        """

        logging.info('Start finding generics type and name')

        obj_type_spec = self._find_type_spec(obj_type)

        if not obj_type_spec:
            raise ValueError('Cannot retrieve spec for: {}'.format(obj_type))

        generics_types = [generics_type for generics_type in GENERICS_TYPES
                          if generics_type in obj_type_spec]

        if not generics_types:
            error_msg = 'Cannot find generics type in spec:\n{}\n'.format(obj_type_spec)
            raise ValueError(error_msg)

        generics_module = dict()
        for generics_type in generics_types:
            for item in obj_type_spec.split(generics_type)[1:]:
                generics_type_name = item.split(';')[0].strip().split(' ')[-1].strip()
                generics_module.update({generics_type_name: generics_type})

        logging.debug('Found generics type:\n{}\n'.format(generics_module))

        return generics_module

    def _convert_data(self, data, generics_module):
        """
        _convert_data: convert data to df based on data_type
        """

        data_types = list(generics_module.values())

        if not set(GENERICS_TYPES) >= set(data_types):
            raise ValueError('Found unknown generics data type in:\n{}\n'.format(data_types))

        if data_types == ['FloatMatrix2D']:
            key = list(generics_module.keys())[list(generics_module.values()).index('FloatMatrix2D')]
            values = data[key]['values']
            index = data[key]['row_ids']
            columns = data[key]['col_ids']
            df = pd.DataFrame(values, index=index, columns=columns)
        elif data_types == ['Attribute']:
            values = data['instances'].values()
            index = data['instances'].keys()
            columns = [x['attribute'] for x in data['attributes']]
            df = pd.DataFrame(values, index=index, columns=columns)
        else:
            raise ValueError('Unexpected Data Type: {}'.format(data_types))

        return df.to_json()

    def _retrieve_data(self, obj_ref, generics_module=None):
        """
        _retrieve_data: retrieve object data and return a dataframe in json format
        """
        obj_info, obj_data = self._retrieve_object(obj_ref)

        if not generics_module:
            generics_module = self._find_generics_type(obj_info[2])

        data_matrix = self._convert_data(obj_data, generics_module)

        return data_matrix

    def _retrieve_object(self, obj_ref):
        logging.info('Start retrieving object {}'.format(obj_ref))
        obj_source = self.wsClient.get_objects2(
            {"objects": [{'ref': obj_ref}]})['data'][0]

        obj_info = obj_source.get('info')
        obj_data = obj_source.get('data')

        return obj_info, obj_data

    @staticmethod
    def validate_params(params, expected, opt_param=set()):
        """Validates that required parameters are present. Warns if unexpected parameters appear"""
        expected = set(expected)
        opt_param = set(opt_param)
        pkeys = set(params)
        if expected - pkeys:
            raise ValueError("Required keys {} not in supplied parameters"
                             .format(", ".join(expected - pkeys)))
        defined_param = expected | opt_param
        for param in params:
            if param not in defined_param:
                logging.warning("Unexpected parameter {} supplied".format(param))

    def __init__(self, config, context):
        self.ws_url = config["workspace-url"]
        self.scratch = config['scratch']
        self.wsClient = workspaceService(self.ws_url, token=context['token'])

    def fetch_attributes(self, params):
        """
        arguments:
        matrix_ref: generics object reference
        ids: name of row/col ids
        dimension: 'row' or 'col', 'row' by default
        """
        logging.info('--->\nrunning Fetch.fetch_attributes\n'
                     + 'params:\n{}'.format(json.dumps(params, indent=1)))

        self.validate_params(params, ('matrix_ref', 'ids'),
                                     ('dimension'))

        matrix_ref = params.get('matrix_ref')
        ids = params.get('ids')
        dimension = params.get('dimension', 'row')

        _, matrix_data = self._retrieve_object(matrix_ref)

        attribute_ref = matrix_data.get('{}_attributemapping_ref'.format(dimension))

        if not attribute_ref:
            raise ValueError('Matrix object does not have {} attribute mapping object'.format(
                dimension))
        _, attri_data = self._retrieve_object(attribute_ref)

        values = attri_data['instances'].values()
        index = attri_data['instances'].keys()
        columns = [x['attribute'] for x in attri_data['attributes']]
        df = pd.DataFrame(values, index=index, columns=columns)

        inter_ids = df.index.intersection(ids).to_list()
        if not inter_ids:
            raise ValueError('Matrix {} ids have no intersection with given IDs'.format(dimension))

        diff = len(ids) - len(inter_ids)
        if diff:
            logging.info('Found {} given IDs not included in the matrix {} ids'.format(diff,
                                                                                       dimension))

        attributes = dict()
        selected_attri = df.loc[inter_ids]
        for idx in selected_attri.index:
            attributes[idx] = selected_attri.loc[idx].to_dict()

        returnVal = {'attributes': attributes}

        return returnVal

    def count_attribute_value(self, params):
        """
        arguments:
        matrix_ref: generics object reference
        attribute_name: name of attribute
        dimension: 'row' or 'col', 'row' by default
        """
        logging.info('--->\nrunning Fetch.count_attribute_value\n'
                     + 'params:\n{}'.format(json.dumps(params, indent=1)))

        self.validate_params(params, ('matrix_ref', 'attribute_name'),
                                     ('dimension'))

        matrix_ref = params.get('matrix_ref')
        attribute_name = params.get('attribute_name')
        dimension = params.get('dimension', 'row')

        _, matrix_data = self._retrieve_object(matrix_ref)

        attribute_ref = matrix_data.get('{}_attributemapping_ref'.format(dimension))

        if not attribute_ref:
            raise ValueError('Matrix object does not have {} attribute mapping object'.format(
                dimension))
        _, attri_data = self._retrieve_object(attribute_ref)

        values = attri_data['instances'].values()
        index = attri_data['instances'].keys()
        columns = [x['attribute'] for x in attri_data['attributes']]
        df = pd.DataFrame(values, index=index, columns=columns)

        if attribute_name not in df:
            raise ValueError('Cannot find {} from attribute mapping {}'.format(attribute_name,
                                                                               attribute_ref))

        attributes_count = df[attribute_name].value_counts().to_dict()
        returnVal = {'attributes_count': attributes_count}

        return returnVal

    def fetch_data(self, params):
        """
        fetch_data: fetch generics data as pandas dataframe for a generics data object

        arguments:
        obj_ref: generics object reference

        optional arguments:
        generics_module: the generics data module to be retrieved from
                        e.g. for an given data type like below:
                        typedef structure {
                          FloatMatrix2D data;
                          condition_set_ref condition_set_ref;
                        } SomeGenericsMatrix;
                        generics_module should be
                        {'data': 'FloatMatrix2D',
                         'condition_set_ref': 'condition_set_ref'}

        return:
        data_matrix: a pandas dataframe in json format
        """

        logging.info('--->\nrunning Fetch.fetch_data\n'
                     + 'params:\n{}'.format(json.dumps(params, indent=1)))

        for p in ['obj_ref']:
            if p not in params:
                raise ValueError('"{}" parameter is required, but missing'.format(p))

        try:
            data_matrix = self._retrieve_data(params.get('obj_ref'),
                                              params.get('generics_module'))
        except Exception:
            error_msg = 'Running fetch_data returned an error:\n{}\n'.format(
                traceback.format_exc())
            error_msg += 'Please try to specify generics type and name as generics_module\n'
            raise ValueError(error_msg)

        returnVal = {'data_matrix': data_matrix}

        return returnVal
