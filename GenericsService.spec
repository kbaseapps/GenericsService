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

};
