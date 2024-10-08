from .birne_record_operations import BirneRecordOperations

def get_records_wrapper(module_api_name):
    """
    A simple wrapper function to fetch records from a specific module using the GET_RECORDS operation.
    
    :param module_api_name: The API Name of the module to fetch records from.
    :param page: The page number to fetch records from, defaults to 1.
    :return: A list of records for the specified module.
    """
    # Create an instance of the BirneZohoCRM class
    crm_instance = BirneRecordOperations(module_api_name=module_api_name)
    
    # Call the perform_operation method with 'GET_RECORDS' as the operation_name
    records = crm_instance.perform_operation("GET_RECORDS", record_id=None, search_params=None, record_data=None)
    
    return records