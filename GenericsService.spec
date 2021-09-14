/*
A KBase module: GenericsService
*/

module GenericsService {
  /* A boolean - 0 for false, 1 for true.
  */
  typedef int boolean;

  /* An X/Y/Z style reference
  */
  typedef string obj_ref;

  /* workspace name of the object */
  typedef string workspace_name;

  /* Input of the fetch_data function
    obj_ref: generics object reference

    Optional arguments:
    generics_module: the generics data module to be retrieved from
                    e.g. for an given data type like below:
                    typedef structure {
                      FloatMatrix2D data;
                      condition_set_ref condition_set_ref;
                    } SomeGenericsMatrix;
                    generics_module should be
                    {'data': 'FloatMatrix2D',
                     'condition_set_ref': 'condition_set_ref'}
  */
  typedef structure {
    obj_ref obj_ref;
    mapping<string, string> generics_module;
  } FetchDataParams;

  /* Output of the fetch_data function
    data_matrix: a pandas dataframe in json format
  */
  typedef structure {
    string data_matrix;
  } FetchDataReturn;

  /* fetch_data: fetch generics data as pandas dataframe for a generics data object*/
  funcdef fetch_data(FetchDataParams params) returns(FetchDataReturn returnVal) authentication required;

  /*
    attribute_name: name of attribute
    dimension: 'row' or 'col', 'row' by default
  */
  typedef structure {
    obj_ref matrix_ref;
    string attribute_name;
    string dimension;
  } AttriCountParams;

  typedef structure {
    mapping<string, int> attributes_count;
  } AttriCountReturn;

  /* count_attribute_value: return count of each attribute value for a given attribute*/
  funcdef count_attribute_value(AttriCountParams params) returns(AttriCountReturn returnVal) authentication required;


  /* Input of the select_data function
    matrix_ref: generics matrix object reference

    row_attribute_query:
    selects rows where the value of an attribute field equals value in the specified array.
            e.g.
            1. query = {'chemical_type': ['specific']} - selected all rows where associated row attribute mapping has 'specific' value for 'chemical_type' field
            2. query = {'chemical_type': ['specific', 'exometabolite']} - selected all rows where associated row attribute mapping has 'specific' or 'exometabolite' value for 'chemical_type' field
            3. query = {'chemical_type': ['specific', 'exometabolite'], 'units': ['mg/l']} - selected all rows where associated row attribute mapping has 'specific' or 'exometabolite' value for 'chemical_type' field and 'mg/l' value for 'units' field
    NOTE: If row_attribute_query is set for the select_col_ids function, the function will return col_ids whose data entries are non-empty and whose row attributes satisfy the row_attribute_query

    col_attribute_query:
    selects columns where the value of an attribute field equals value in the specified array.
    NOTE: If col_attribute_query is set for the select_row_ids function, the function will return row_ids whose data entries are non-empty and whose column attributes satisfy the col_attribute_query
  */

  typedef structure {
    obj_ref matrix_ref;
    mapping<string, list<string>> row_attribute_query;
    mapping<string, list<string>> col_attribute_query;
  } SelectIDParams;

  /* Output of the select_col/row_ids function
  */
  typedef structure {
    list<string> ids;
  } SelectIDReturn;


  /* select_col_ids: list selected column IDs in the matrix*/
  funcdef select_col_ids(SelectIDParams params) returns(SelectIDReturn returnVal) authentication required;


  /* select_row_ids: list selected row IDs in the matrix*/
  funcdef select_row_ids(SelectIDParams params) returns(SelectIDReturn returnVal) authentication required;

  /*
    ids: name of row/col ids
    dimension: 'row' or 'col', 'row' by default
  */
  typedef structure {
    obj_ref matrix_ref;
    list<string> ids;
    string dimension;
  } FetchAttriParams;

  /* attributes in dict format
    e.g.
    {'PB-Low-5': {'IGSN': 'IEAWH0001'}}
  */
  typedef structure {
    mapping<string, mapping<string, string>> attributes;
  } FetchAttriReturn;

  /* return non-empty attributes for given row/col ids */
  funcdef fetch_attributes(FetchAttriParams params) returns(FetchAttriReturn returnVal) authentication required;

  /*
    row_ids: name of target row ids. If empty, return all row ids.
    col_ids: name of target col ids. If empty, return all col ids.
  */
  typedef structure {
    obj_ref matrix_ref;
    list<string> row_ids;
    list<string> col_ids;
  } FetchDataByIDParams;

  /*
    A simple 2D matrix of values with labels/ids for rows and
    columns.  The matrix is stored as a list of lists, with the outer list
    containing rows, and the inner lists containing values for each column of
    that row.  Row/Col ids should be unique.

    row_ids - unique ids for rows.
    col_ids - unique ids for columns.
    values - two dimensional array indexed as: values[row][col]

    @metadata ws length(row_ids) as n_rows
    @metadata ws length(col_ids) as n_cols
  */
  typedef structure {
    list<string> row_ids;
    list<string> col_ids;
    list<list<float>> values;
  } FloatMatrix2D;

  typedef structure {
    FloatMatrix2D data;
  } FetchDataByIDReturn;

  /* return matrix data for specific row/col ids */
  funcdef fetch_data_by_ids(FetchDataByIDParams params) returns(FetchDataByIDReturn returnVal) authentication required;

  typedef structure {
    obj_ref matrix_ref;
  } FetchAllParams;

  typedef structure {
    mapping<string, mapping<string, string>> row_attributes;
    mapping<string, mapping<string, string>> col_attributes;
    FloatMatrix2D data;
  } FetchAllReturn;

  /* return all matrix data including attribute information */
  funcdef fetch_all(FetchAllParams params) returns(FetchAllReturn returnVal) authentication required;

};
