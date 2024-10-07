from .birne_record_operations import birne_record_operations

def searchRecords(module_api_name:str,search_params:str) -> list[dict]:
    """
    Returns records based on search params.
    
    :param module_api_name: The API Name of the module to fetch records from (string).
    :param search_params: Search parameters of zcrm api
    :return: A list of dictionaries, where each dictionary represents a record.
    """
    return birne_record_operations("SEARCH_RECORD",module_api_name=module_api_name,search_params=search_params)