from .birne_record_operations import BirneRecordOperations

def search_records_wrapper(module_api_name, search_criteria, page=1):
    """
    A simple wrapper function to search records from a specific module using the SEARCH_RECORD operation.
    
    :param module_api_name: The API Name of the module to search records from.
    :param search_criteria: The search criteria for filtering records (e.g., "(Last_Name:starts_with:Smith)").
    :param page: The page number to fetch search results from, defaults to 1.
    :return: A list of records matching the search criteria for the specified module.
    """
    # Create an instance of the BirneZohoCRM class
    crm_instance = BirneRecordOperations(module_api_name=module_api_name)
    
    # Call the perform_operation method with 'SEARCH_RECORD' as the operation_name
    records = crm_instance.perform_operation("SEARCH_RECORD", record_id=None, search_params=search_criteria)
    
    return records