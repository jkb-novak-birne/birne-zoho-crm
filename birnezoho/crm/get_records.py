from .birne_record_operations import birne_record_operations

def getRecords(module_api_name: str) -> list[dict]:
    """
    Returns all records from the specified module, including pagination.
    
    :param module_api_name: The API Name of the module to fetch records from (string).
    :return: A list of dictionaries, where each dictionary represents a record.
    """
    return birne_record_operations("GET_RECORDS", module_api_name=module_api_name)
