from .birne_record_operations import birne_record_operations

def getRecordById(module_api_name: str, record_id: int) -> dict:
    """
    Returns a specific record by its ID from the specified module.
    
    :param module_api_name: The API Name of the module to fetch the record from (string).
    :param record_id: The ID of the record to be fetched (integer).
    :return: A dictionary representing the record.
    """
    return birne_record_operations("GET_RECORD", module_api_name=module_api_name, record_id=record_id)
