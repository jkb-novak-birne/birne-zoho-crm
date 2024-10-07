from .birne_record_operations import birne_record_operations
from .utils import handle_dict_to_record

def updateRecord(module_api_name: str,record_id:int,record_data:dict) -> dict:
    """
    Updates record by its ID.
    
    :param module_api_name: The API Name of the module to fetch records from (string).
    :return: A list of dictionaries, where each dictionary represents a record.
    """
    record_to_update = handle_dict_to_record(module_api_name=module_api_name,record_data=record_data)
    return birne_record_operations(operation_name="UPDATE_RECORD",module_api_name=module_api_name,record_id=record_id,record_data=record_to_update)
