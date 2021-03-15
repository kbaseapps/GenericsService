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

  /* Ouput of the fetch_data function
    data_matrix: a pandas dataframe in json format
  */
  typedef structure {
    string data_matrix;
  } FetchDataReturn;

  /* fetch_data: fetch generics data as pandas dataframe for a generics data object*/
  funcdef fetch_data(FetchDataParams params) returns(FetchDataReturn returnVal) authentication required;


  /* Input of the select_data function
    obj_ref: generics object reference
    query: selects col/row where the value of an attribute field equals vluae in the sepecified array.
            e.g.
            1. query = {'chemical_type': ['specific']} - selected all rows where associated row attribute mapping has 'specific' value for 'chemical_type' field
            2. query = {'chemical_type': ['specific', 'exometabolite']} - selected all rows where associated row attribute mapping has 'specific' or 'exometabolite' value for 'chemical_type' field
            3. query = {'chemical_type': ['specific', 'exometabolite'], 'units': ['mg/l']} - selected all rows where associated row attribute mapping has 'specific' or 'exometabolite' value for 'chemical_type' field and 'mg/l' value for 'units' field
            4. query = {'id': ['Acetate', 'Al2O3', 'Ba']} - return only matrix data and row attribute mapping data where row id equals one of ['Acetate', 'Al2O3', 'Ba']
    Optional arguments:
    return_id_only: only return selected ids (default False)
  */
  typedef structure {
    obj_ref obj_ref;
    mapping<string, list<string>> query;
    boolean return_id_only;
  } SelectDataParams;


  /* Ouput of the select_data function
    data_matrix: a pandas dataframe in json format represeting matrix data
    attribute_data_matrix: a pandas dataframe in json format represeting associated attribute mapping data
    selected_ids: selected row/col ids
  */
  typedef structure {
    string attribute_data_matrix;
    string data_matrix;
    list<string> selected_ids;
  } SelectDataReturn;

  /* select_data: select generics data as pandas dataframe for a generics data object*/
  funcdef select_data(SelectDataParams params) returns(SelectDataReturn returnVal) authentication required;

};
