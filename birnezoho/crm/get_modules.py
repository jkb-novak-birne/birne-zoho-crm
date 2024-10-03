from zcrmsdk.src.com.zoho.crm.api.modules.modules_operations import ModulesOperations
 
def getModules():
    """
    Fetch and return all Zoho CRM modules.
    
    Returns:
    list: List of modules in Zoho CRM.
    """
    try:
        modules_operations = ModulesOperations()
        response = modules_operations.get_modules()
        
        if response is not None and response.get_status_code() == 200:
            modules = response.get_object().get_modules()
            return [module.get_api_name() for module in modules]
        return []
    
    except Exception as e:
        print(f"Error fetching modules: {e}")
        return []