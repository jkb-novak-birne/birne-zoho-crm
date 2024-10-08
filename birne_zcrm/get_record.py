from .birne_record_operations import BirneRecordOperations

def get_record_wrapper(module_api_name, record_id):
    """
    A simple wrapper function to fetch a single record from a specific module using the GET_RECORD operation.
    
    :param module_api_name: The API Name of the module to fetch the record from.
    :param record_id: The ID of the record to fetch.
    :return: The record data for the specified record ID.
    """
    # Create an instance of the BirneZohoCRM class
    crm_instance = BirneRecordOperations(module_api_name=module_api_name)
    
    # Call the perform_operation method with 'GET_RECORD' as the operation_name
    record = crm_instance.perform_operation("GET_RECORD", record_id=record_id)
    
    return record