# -*- coding: utf-8 -*-
import inspect
import json
import os
import time
import unittest
from configparser import ConfigParser
import pandas as pd

from GenericsService.GenericsServiceImpl import GenericsService
from GenericsService.GenericsServiceServer import MethodContext
from GenericsService.authclient import KBaseAuth as _KBaseAuth

from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.GenomeFileUtilClient import GenomeFileUtil
from installed_clients.WorkspaceClient import Workspace


class GenericsServiceTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = os.environ.get('KB_AUTH_TOKEN', None)
        config_file = os.environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('GenericsService'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'GenericsService',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = Workspace(cls.wsURL)
        cls.serviceImpl = GenericsService(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']
        suffix = int(time.time() * 1000)
        cls.wsName = "test_ContigFilter_" + str(suffix)
        ret = cls.wsClient.create_workspace({'workspace': cls.wsName})  # noqa

        cls.gfu = GenomeFileUtil(cls.callback_url)
        cls.dfu = DataFileUtil(cls.callback_url)
        cls.prepare_data()

    @classmethod
    def prepare_data(cls):

        # upload genome object
        # genbank_file_name = 'minimal.gbff'
        # genbank_file_path = os.path.join(cls.scratch, genbank_file_name)
        # shutil.copy(genbank_file_name, genbank_file_path)

        # genome_object_name = 'test_Genome'
        # cls.genome_ref = cls.gfu.genbank_to_genome({'file': {'path': genbank_file_path},
        #                                             'workspace_name': cls.wsName,
        #                                             'genome_name': genome_object_name,
        #                                             'generate_ids_if_needed': 1
        #                                             })['genome_ref']

        # upload AttributeMapping object
        workspace_id = cls.dfu.ws_name_to_id(cls.wsName)
        object_type = 'KBaseExperiments.AttributeMapping'
        attribute_mapping_object_name = 'test_attribute_mapping'
        attribute_mapping_data = {'instances': {'test_instance_1': ['1-1', '1-2', '1-3'],
                                                'test_instance_2': ['2-1', '1-2', '2-3'],
                                                'test_instance_3': ['3-1', '3-2', '3-3']},
                                  'attributes': [{'attribute': 'test_attribute_1',
                                                  'attribute_ont_ref': 'attribute_ont_ref_1',
                                                  'attribute_ont_id': 'attribute_ont_id_1',
                                                  'source': 'source'},
                                                 {'attribute': 'test_attribute_2',
                                                  'attribute_ont_ref': 'attribute_ont_ref_2',
                                                  'attribute_ont_id': 'attribute_ont_id_2',
                                                  'source': 'source'},
                                                 {'attribute': 'test_attribute_3',
                                                  'attribute_ont_ref': 'attribute_ont_ref_3',
                                                  'attribute_ont_id': 'attribute_ont_id_3',
                                                  'source': 'source'}],
                                  'ontology_mapping_method': 'user curation'}
        save_object_params = {
            'id': workspace_id,
            'objects': [{'type': object_type,
                         'data': attribute_mapping_data,
                         'name': attribute_mapping_object_name}]
        }

        dfu_oi = cls.dfu.save_objects(save_object_params)[0]
        cls.attribute_mapping_ref = str(dfu_oi[6]) + '/' + str(dfu_oi[0]) + '/' + str(dfu_oi[4])

        cls.col_ids = ['instance_1', 'instance_2', 'instance_3', 'instance_4']
        cls.row_ids = ['WRI_RS00050_CDS_1', 'WRI_RS00065_CDS_1', 'WRI_RS00070_CDS_1']
        cls.values = [[0.1, 0.2, 0.3, 0.4],
                      [0.3, 0.4, 0.5, 0.6],
                      [None, None, None, None]]
        cls.row_mapping = {'WRI_RS00050_CDS_1': 'test_instance_1',
                           'WRI_RS00065_CDS_1': 'test_instance_2',
                           'WRI_RS00070_CDS_1': 'test_instance_3'}
        cls.col_mapping = {'instance_1': 'test_instance_1',
                           'instance_2': 'test_instance_2',
                           'instance_3': 'test_instance_3',
                           'instance_4': 'test_instance_3'}
        cls.feature_mapping = {'WRI_RS00050_CDS_1': 'WRI_RS00050_CDS_1',
                               'WRI_RS00065_CDS_1': 'WRI_RS00065_CDS_1',
                               'WRI_RS00070_CDS_1': 'WRI_RS00070_CDS_1'}

        # upload ExpressionMatrix object
        object_type = 'KBaseMatrices.ExpressionMatrix'
        expression_matrix_object_name = 'test_expression_matrix'
        expression_matrix_data = {'scale': 'log2',
                                  'type': 'level',
                                  # 'col_attributemapping_ref': cls.attribute_mapping_ref,
                                  # 'col_mapping': cls.col_mapping,
                                  'row_attributemapping_ref': cls.attribute_mapping_ref,
                                  'row_mapping': cls.row_mapping,
                                  'feature_mapping': cls.feature_mapping,
                                  'data': {'row_ids': cls.row_ids,
                                           'col_ids': cls.col_ids,
                                           'values': cls.values
                                           }}
        save_object_params = {
            'id': workspace_id,
            'objects': [{'type': object_type,
                         'data': expression_matrix_data,
                         'name': expression_matrix_object_name}]
        }

        dfu_oi = cls.dfu.save_objects(save_object_params)[0]
        cls.expression_matrix_ref = str(dfu_oi[6]) + '/' + str(dfu_oi[0]) + '/' + str(dfu_oi[4])

        expression_matrix_object_name = 'test_expression_matrix_no_attribute_mapping'
        expression_matrix_data = {'scale': 'log2',
                                  'type': 'level',
                                  'data': {'row_ids': cls.row_ids,
                                           'col_ids': cls.col_ids,
                                           'values': cls.values
                                           }}
        save_object_params = {
            'id': workspace_id,
            'objects': [{'type': object_type,
                         'data': expression_matrix_data,
                         'name': expression_matrix_object_name}]
        }

        dfu_oi = cls.dfu.save_objects(save_object_params)[0]
        cls.expression_matrix_nc_ref = str(dfu_oi[6]) + '/' + str(dfu_oi[0]) + '/' + str(dfu_oi[4])

        # upload FitnessMatrix object
        object_type = 'KBaseMatrices.FitnessMatrix'
        fitness_matrix_object_name = 'test_fitness_matrix'
        fitness_matrix_data = {'scale': 'log2',
                               'type': 'level',
                               'row_attributemapping_ref': cls.attribute_mapping_ref,
                               'row_mapping': cls.row_mapping,
                               'data': {'row_ids': cls.row_ids,
                                        'col_ids': cls.col_ids,
                                        'values': cls.values
                                        }}
        save_object_params = {
            'id': workspace_id,
            'objects': [{'type': object_type,
                         'data': fitness_matrix_data,
                         'name': fitness_matrix_object_name}]
        }

        dfu_oi = cls.dfu.save_objects(save_object_params)[0]
        cls.fitness_matrix_ref = str(dfu_oi[6]) + '/' + str(dfu_oi[0]) + '/' + str(dfu_oi[4])

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def start_test(self):
        testname = inspect.stack()[1][3]
        print('\n*** starting test: ' + testname + ' **')

    def fail_fetch_data(self, params, error, exception=ValueError,
                        contains=False):
        with self.assertRaises(exception) as context:
            self.serviceImpl.fetch_data(self.ctx, params)
        if contains:
            self.assertIn(error, str(context.exception.args))
        else:
            self.assertEqual(error, str(context.exception.args[0]))

    def check_fetch_data_output(self, returnVal):
        self.assertTrue('data_matrix' in returnVal)
        data_matrix = json.loads(returnVal.get('data_matrix'))

        col_ids = list(data_matrix.keys())
        self.assertCountEqual(col_ids, self.col_ids)
        for col_id in col_ids:
            self.assertCountEqual(list(data_matrix.get(col_id).keys()), self.row_ids)

    def test_bad_fetch_data_params(self):
        self.start_test()
        invalidate_params = {'missing_obj_ref': 'obj_ref'}
        error_msg = '"obj_ref" parameter is required, but missing'
        self.fail_fetch_data(invalidate_params, error_msg)

    def test_fetch_data(self):
        self.start_test()
        params = {'obj_ref': self.expression_matrix_ref}
        returnVal = self.serviceImpl.fetch_data(self.ctx, params)[0]
        self.check_fetch_data_output(returnVal)

        params = {'obj_ref': self.fitness_matrix_ref}
        returnVal = self.serviceImpl.fetch_data(self.ctx, params)[0]
        self.check_fetch_data_output(returnVal)

        params = {'obj_ref': self.attribute_mapping_ref}
        returnVal = self.serviceImpl.fetch_data(self.ctx, params)[0]
        self.assertIn('data_matrix', returnVal)
        df = pd.DataFrame(json.loads(returnVal['data_matrix']))
        self.assertEqual(df.shape, (3, 3))

        params = {'obj_ref': self.expression_matrix_ref,
                  'generics_module': {'data': 'FloatMatrix2D'}}
        returnVal = self.serviceImpl.fetch_data(self.ctx, params)[0]
        self.check_fetch_data_output(returnVal)

    def test_count_attribute_value(self):
        self.start_test()
        params = {'matrix_ref': self.expression_matrix_ref, 'attribute_name': 'test_attribute_1',
                  'dimension': 'row'}
        returnVal = self.serviceImpl.count_attribute_value(self.ctx, params)[0]

        attributes_count = returnVal['attributes_count']
        expected_count = {'1-1': 1, '2-1': 1, '3-1': 1}
        self.assertTrue(attributes_count == expected_count)

        params = {'matrix_ref': self.expression_matrix_ref, 'attribute_name': 'test_attribute_2',
                  'dimension': 'row'}
        returnVal = self.serviceImpl.count_attribute_value(self.ctx, params)[0]

        attributes_count = returnVal['attributes_count']
        expected_count = {'1-2': 2, '3-2': 1}
        self.assertTrue(attributes_count == expected_count)

    def test_fetch_attributes(self):
        self.start_test()
        params = {'matrix_ref': self.expression_matrix_ref,
                  'ids': ['a', 'test_instance_1', 'test_instance_2'],
                  'dimension': 'row'}
        returnVal = self.serviceImpl.fetch_attributes(self.ctx, params)[0]

        attributes = returnVal['attributes']
        expected_attributes = {'test_instance_1': {'test_attribute_1': '1-1',
                                                   'test_attribute_2': '1-2',
                                                   'test_attribute_3': '1-3'},
                               'test_instance_2': {'test_attribute_1': '2-1',
                                                   'test_attribute_2': '1-2',
                                                   'test_attribute_3': '2-3'}}
        self.assertTrue(attributes == expected_attributes)

    def test_fetch_data_by_ids(self):
        self.start_test()
        params = {'matrix_ref': self.expression_matrix_ref}
        returnVal = self.serviceImpl.fetch_data_by_ids(self.ctx, params)[0]
        data = returnVal['data']

        expected_data = {'row_ids': ['WRI_RS00050_CDS_1',
                                     'WRI_RS00065_CDS_1',
                                     'WRI_RS00070_CDS_1'],
                         'col_ids': ['instance_1', 'instance_2', 'instance_3', 'instance_4'],
                         'values': [[0.1, 0.2, 0.3, 0.4],
                                    [0.3, 0.4, 0.5, 0.6],
                                    [None, None, None, None]]}

        self.assertTrue(data == expected_data)

        params = {'matrix_ref': self.expression_matrix_ref,
                  'row_ids': ['WRI_RS00050_CDS_1', 'WRI_RS00065_CDS_1'],
                  'col_ids': ['instance_1', 'instance_2']}
        returnVal = self.serviceImpl.fetch_data_by_ids(self.ctx, params)[0]
        data = returnVal['data']

        expected_data = {'row_ids': ['WRI_RS00050_CDS_1', 'WRI_RS00065_CDS_1'],
                         'col_ids': ['instance_1', 'instance_2'],
                         'values': [[0.1, 0.2],
                                    [0.3, 0.4]]}

        self.assertTrue(data == expected_data)

    def test_fetch_all(self):
        self.start_test()
        params = {'matrix_ref': self.expression_matrix_ref}
        returnVal = self.serviceImpl.fetch_all(self.ctx, params)[0]

        expected_data = {'data': {'row_ids': ['WRI_RS00050_CDS_1',
                                              'WRI_RS00065_CDS_1',
                                              'WRI_RS00070_CDS_1'],
                                  'col_ids': ['instance_1', 'instance_2',
                                              'instance_3', 'instance_4'],
                                  'values': [[0.1, 0.2, 0.3, 0.4],
                                             [0.3, 0.4, 0.5, 0.6],
                                             [None, None, None, None]]},
                         'row_attributes': {'test_instance_1': {'test_attribute_1': '1-1',
                                                                'test_attribute_2': '1-2',
                                                                'test_attribute_3': '1-3'},
                                            'test_instance_2': {'test_attribute_1': '2-1',
                                                                'test_attribute_2': '1-2',
                                                                'test_attribute_3': '2-3'},
                                            'test_instance_3': {'test_attribute_1': '3-1',
                                                                'test_attribute_2': '3-2',
                                                                'test_attribute_3': '3-3'}},
                         'col_attributes': {}}
        self.assertTrue(returnVal == expected_data)
