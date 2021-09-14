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
    VERSION = "0.0.3"
    GIT_URL = "git@github.com:Tianhao-Gu/GenericsService.git"
    GIT_COMMIT_HASH = "87dc106cd7d846c5372a8746649d4129938c9416"

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
        :returns: instance of type "FetchDataReturn" (Output of the
           fetch_data function data_matrix: a pandas dataframe in json
           format) -> structure: parameter "data_matrix" of String
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

    def count_attribute_value(self, ctx, params):
        """
        count_attribute_value: return count of each attribute value for a given attribute
        :param params: instance of type "AttriCountParams" (attribute_name:
           name of attribute dimension: 'row' or 'col', 'row' by default) ->
           structure: parameter "matrix_ref" of type "obj_ref" (An X/Y/Z
           style reference), parameter "attribute_name" of String, parameter
           "dimension" of String
        :returns: instance of type "AttriCountReturn" -> structure: parameter
           "attributes_count" of mapping from String to Long
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN count_attribute_value
        fetch_utils = Fetch(self.config, ctx)
        returnVal = fetch_utils.count_attribute_value(params)
        #END count_attribute_value

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method count_attribute_value return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def select_col_ids(self, ctx, params):
        """
        select_col_ids: list selected column IDs in the matrix
        :param params: instance of type "SelectIDParams" (Input of the
           select_data function matrix_ref: generics matrix object reference
           row_attribute_query: selects rows where the value of an attribute
           field equals value in the specified array. e.g. 1. query =
           {'chemical_type': ['specific']} - selected all rows where
           associated row attribute mapping has 'specific' value for
           'chemical_type' field 2. query = {'chemical_type': ['specific',
           'exometabolite']} - selected all rows where associated row
           attribute mapping has 'specific' or 'exometabolite' value for
           'chemical_type' field 3. query = {'chemical_type': ['specific',
           'exometabolite'], 'units': ['mg/l']} - selected all rows where
           associated row attribute mapping has 'specific' or 'exometabolite'
           value for 'chemical_type' field and 'mg/l' value for 'units' field
           NOTE: If row_attribute_query is set for the select_col_ids
           function, the function will return col_ids whose data entries are
           non-empty and whose row attributes satisfy the row_attribute_query
           col_attribute_query: selects columns where the value of an
           attribute field equals value in the specified array. NOTE: If
           col_attribute_query is set for the select_row_ids function, the
           function will return row_ids whose data entries are non-empty and
           whose column attributes satisfy the col_attribute_query) ->
           structure: parameter "matrix_ref" of type "obj_ref" (An X/Y/Z
           style reference), parameter "row_attribute_query" of mapping from
           String to list of String, parameter "col_attribute_query" of
           mapping from String to list of String
        :returns: instance of type "SelectIDReturn" (Output of the
           select_col/row_ids function) -> structure: parameter "ids" of list
           of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN select_col_ids
        #END select_col_ids

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method select_col_ids return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def select_row_ids(self, ctx, params):
        """
        select_row_ids: list selected row IDs in the matrix
        :param params: instance of type "SelectIDParams" (Input of the
           select_data function matrix_ref: generics matrix object reference
           row_attribute_query: selects rows where the value of an attribute
           field equals value in the specified array. e.g. 1. query =
           {'chemical_type': ['specific']} - selected all rows where
           associated row attribute mapping has 'specific' value for
           'chemical_type' field 2. query = {'chemical_type': ['specific',
           'exometabolite']} - selected all rows where associated row
           attribute mapping has 'specific' or 'exometabolite' value for
           'chemical_type' field 3. query = {'chemical_type': ['specific',
           'exometabolite'], 'units': ['mg/l']} - selected all rows where
           associated row attribute mapping has 'specific' or 'exometabolite'
           value for 'chemical_type' field and 'mg/l' value for 'units' field
           NOTE: If row_attribute_query is set for the select_col_ids
           function, the function will return col_ids whose data entries are
           non-empty and whose row attributes satisfy the row_attribute_query
           col_attribute_query: selects columns where the value of an
           attribute field equals value in the specified array. NOTE: If
           col_attribute_query is set for the select_row_ids function, the
           function will return row_ids whose data entries are non-empty and
           whose column attributes satisfy the col_attribute_query) ->
           structure: parameter "matrix_ref" of type "obj_ref" (An X/Y/Z
           style reference), parameter "row_attribute_query" of mapping from
           String to list of String, parameter "col_attribute_query" of
           mapping from String to list of String
        :returns: instance of type "SelectIDReturn" (Output of the
           select_col/row_ids function) -> structure: parameter "ids" of list
           of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN select_row_ids
        #END select_row_ids

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method select_row_ids return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def fetch_attributes(self, ctx, params):
        """
        return non-empty attributes for given row/col ids
        :param params: instance of type "FetchAttriParams" (ids: name of
           row/col ids dimension: 'row' or 'col', 'row' by default) ->
           structure: parameter "matrix_ref" of type "obj_ref" (An X/Y/Z
           style reference), parameter "ids" of list of String, parameter
           "dimension" of String
        :returns: instance of type "FetchAttriReturn" (attributes in dict
           format e.g. {'PB-Low-5': {'IGSN': 'IEAWH0001'}}) -> structure:
           parameter "attributes" of mapping from String to mapping from
           String to String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN fetch_attributes
        fetch_utils = Fetch(self.config, ctx)
        returnVal = fetch_utils.fetch_attributes(params)
        #END fetch_attributes

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method fetch_attributes return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def fetch_data_by_ids(self, ctx, params):
        """
        return matrix data for specific row/col ids
        :param params: instance of type "FetchDataByIDParams" (row_ids: name
           of target row ids. If empty, return all row ids. col_ids: name of
           target col ids. If empty, return all col ids.) -> structure:
           parameter "matrix_ref" of type "obj_ref" (An X/Y/Z style
           reference), parameter "row_ids" of list of String, parameter
           "col_ids" of list of String
        :returns: instance of type "FetchDataByIDReturn" -> structure:
           parameter "data" of type "FloatMatrix2D" (A simple 2D matrix of
           values with labels/ids for rows and columns.  The matrix is stored
           as a list of lists, with the outer list containing rows, and the
           inner lists containing values for each column of that row. Row/Col
           ids should be unique. row_ids - unique ids for rows. col_ids -
           unique ids for columns. values - two dimensional array indexed as:
           values[row][col] @metadata ws length(row_ids) as n_rows @metadata
           ws length(col_ids) as n_cols) -> structure: parameter "row_ids" of
           list of String, parameter "col_ids" of list of String, parameter
           "values" of list of list of Double
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN fetch_data_by_ids
        #END fetch_data_by_ids

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method fetch_data_by_ids return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def fetch_all(self, ctx, params):
        """
        return all matrix data including attribute information
        :param params: instance of type "FetchAllParams" -> structure:
           parameter "matrix_ref" of type "obj_ref" (An X/Y/Z style reference)
        :returns: instance of type "FetchAllReturn" -> structure: parameter
           "row_attributes" of mapping from String to mapping from String to
           String, parameter "col_attributes" of mapping from String to
           mapping from String to String, parameter "data" of type
           "FloatMatrix2D" (A simple 2D matrix of values with labels/ids for
           rows and columns.  The matrix is stored as a list of lists, with
           the outer list containing rows, and the inner lists containing
           values for each column of that row. Row/Col ids should be unique.
           row_ids - unique ids for rows. col_ids - unique ids for columns.
           values - two dimensional array indexed as: values[row][col]
           @metadata ws length(row_ids) as n_rows @metadata ws
           length(col_ids) as n_cols) -> structure: parameter "row_ids" of
           list of String, parameter "col_ids" of list of String, parameter
           "values" of list of list of Double
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN fetch_all
        #END fetch_all

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method fetch_all return value ' +
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
