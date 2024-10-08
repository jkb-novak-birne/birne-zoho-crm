from .birne_record_operations import BirneRecordOperations
from .utils import handle_dict_to_record

def update_record_wrapper(module_api_name, record_id, record_data, trigger=None):
    """
    A simple wrapper function to update a record in a specific module using the UPDATE_RECORD operation.
    
    :param module_api_name: The API Name of the module to update the record in.
    :param record_id: The ID of the record to update.
    :param record_data: The dict object containing the updated data for the record.
    :param trigger: List of operations to trigger when updating the record (e.g., ["approval", "workflow", "blueprint"]).
    :return: The result of the update operation (success or failure details).
    """
    #convert dict to ZCRM object
    record_data = handle_dict_to_record(module_api_name=module_api_name,record_data=record_data)

    # Create an instance of the BirneZohoCRM class
    crm_instance = BirneRecordOperations(module_api_name=module_api_name, trigger=trigger)
    
    # Call the perform_operation method with 'UPDATE_RECORD' as the operation_name
    result = crm_instance.perform_operation("UPDATE_RECORD", record_id=record_id, record_data=record_data)
    
    return result