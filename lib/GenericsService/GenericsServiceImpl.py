# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os

from GenericsService.Fetch import Fetch
#END_HEADER


class GenericsService:
    '''
    Module Name:
    GenericsService

    Module Description:
    A KBase module: GenericsService
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = ""
    GIT_COMMIT_HASH = ""

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.config = config
        self.shared_folder = config['scratch']
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        #END_CONSTRUCTOR
        pass


    def fetch_data(self, ctx, params):
        """
        fetch_data: fetch generics data as pandas dataframe for a generics data object
        :param params: instance of type "FetchDataParams" (Input of the
           fetch_data function obj_ref: generics object reference Optional
           arguments: generics_module: the generics data module to be
           retrieved from e.g. for an given data type like below: typedef
           structure { FloatMatrix2D data; condition_set_ref
           condition_set_ref; } SomeGenericsMatrix; generics_module should be
           {'data': 'FloatMatrix2D', 'condition_set_ref':
           'condition_set_ref'}) -> structure: parameter "obj_ref" of type
           "obj_ref" (An X/Y/Z style reference), parameter "generics_module"
           of mapping from String to String
        :returns: instance of type "FetchDataReturn" (Ouput of the fetch_data
           function data_matrix: a pandas dataframe in json format) ->
           structure: parameter "data_matrix" of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN fetch_data
        fetch_utils = Fetch(self.config, ctx)
        returnVal = fetch_utils.fetch_data(params)
        #END fetch_data

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method fetch_data return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
