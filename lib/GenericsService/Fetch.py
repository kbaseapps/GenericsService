import json
import logging
import re
import traceback

import pandas as pd

from installed_clients.WorkspaceClient import Workspace as workspaceService

GENERICS_TYPE = ['FloatMatrix2D']  # add case in _convert_data for each additional type


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

        generics_types = [generics_type for generics_type in GENERICS_TYPE
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

        if not set(GENERICS_TYPE) >= set(data_types):
            raise ValueError('Found unknown generics data type in:\n{}\n'.format(data_types))

        if data_types == ['FloatMatrix2D']:
            key = list(generics_module.keys())[list(generics_module.values()).index('FloatMatrix2D')]
            values = data[key]['values']
            index = data[key]['row_ids']
            columns = data[key]['col_ids']
            df = pd.DataFrame(values, index=index, columns=columns)
        else:
            raise ValueError('Unexpected Data Type: {}'.format(data_types))

        return df.to_json()

    def _retrieve_data(self, obj_ref, generics_module=None):
        """
        _retrieve_data: retrieve object data and return a dataframe in json format
        """
        logging.info('Start retrieving data')
        obj_source = self.wsClient.get_objects2(
            {"objects": [{'ref': obj_ref}]})['data'][0]

        obj_info = obj_source.get('info')
        obj_data = obj_source.get('data')

        if not generics_module:
            generics_module = self._find_generics_type(obj_info[2])

        try:
            data = {k: v for k, v in obj_data.items() if k in generics_module.keys()}
        except KeyError:
            raise ValueError('Retrieved wrong generics type name')

        data_matrix = self._convert_data(data, generics_module)

        return data_matrix

    def __init__(self, config):
        self.ws_url = config["workspace-url"]
        self.token = config['KB_AUTH_TOKEN']
        self.scratch = config['scratch']
        self.wsClient = workspaceService(self.ws_url, token=self.token)

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

        logging.info('--->\nrunning DataUtil.fetch_data\n' +
                     'params:\n{}'.format(json.dumps(params, indent=1)))

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