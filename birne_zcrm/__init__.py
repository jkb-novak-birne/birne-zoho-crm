from .initialize_sdk import initialize_zoho_sdk
from .get_modules import getModules
from .coql_query import coqlQuery
from .search_records import search_records_wrapper
from .get_record import get_record_wrapper
from .get_records import get_records_wrapper
from .update_record import update_record_wrapper
from .create_record import create_record_wrapper
class ZohoCRMWrapper:
    def __init__(self, client_id: str, client_secret: str, refresh_token: str, redirect_url: str, user_email:str,api_domain: str = "www.zohoapis.com"):
        """
        Initialize the Zoho CRM SDK with OAuth credentials.
        
        Parameters:
        client_id (str): OAuth client ID.
        client_secret (str): OAuth client secret.
        refresh_token (str): OAuth refresh token.
        redirect_url (str): OAuth redirect URL.
        api_domain (str): Zoho CRM API domain.
        """
        print("Initializing zoho crm")
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.redirect_url = redirect_url
        self.api_domain = api_domain
        self.user_email = user_email
        initialize_zoho_sdk(self)
    
    def getModules(self):
        return getModules()
    
    def coqlQuery(self,query):
        return coqlQuery(query)

    def getRecordById(self, module_api_name, record_id):
        return get_record_wrapper(module_api_name,record_id)
    
    def searchRecords(self,module_api_name,searchCriteria):
        return search_records_wrapper(module_api_name,searchCriteria)
    
    def getRecords(self,module_api_name):
        return get_records_wrapper(module_api_name)
    
    def updateRecord(self,module_api_name,record_id:int,record_data:dict,trigger = []):
        return update_record_wrapper(module_api_name,record_id,record_data,trigger)
    
    def createRecord(self,module_api_name,record_data:dict,trigger = []):
        return create_record_wrapper(module_api_name,record_data,trigger)
    