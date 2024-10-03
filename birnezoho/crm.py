# birnezoho/crm.py

import os 
from zcrmsdk.src.com.zoho.crm.api.user_signature import UserSignature
from zcrmsdk.src.com.zoho.crm.api.dc import EUDataCenter
from zcrmsdk.src.com.zoho.api.authenticator.oauth_token import OAuthToken
from zcrmsdk.src.com.zoho.api.authenticator.store import FileStore
from zcrmsdk.src.com.zoho.api.logger import Logger
from zcrmsdk.src.com.zoho.crm.api.sdk_config import SDKConfig
from zcrmsdk.src.com.zoho.crm.api.initializer import Initializer
from zcrmsdk.src.com.zoho.crm.api.modules.modules_operations import ModulesOperations

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
        self.initialize_zoho_sdk()

    def initialize_zoho_sdk(self):
        """
        Initialize the Zoho SDK with OAuth credentials and environment configuration.
        """

        # Define the zohoStore folder path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        zoho_store_path = os.path.join(current_dir, "zohoStore")

        # Check if the folder exists; if not, create it
        if not os.path.exists(zoho_store_path):
            os.makedirs(zoho_store_path)

        # Define paths for logger and token files
        logger_path = os.path.join(zoho_store_path, "zcrm_logger.log")
        token_store_path = os.path.join(zoho_store_path, "zcrm_tokens.txt")

        # User signature
        user = UserSignature(self.user_email)
        
        # OAuth token
        token = OAuthToken(
            client_id=self.client_id,
            client_secret=self.client_secret,
            refresh_token=self.refresh_token,
            redirect_url=self.redirect_url
        )
        
        # API environment
        environment = EUDataCenter.PRODUCTION()
        
        #KEY STORE
        store = FileStore(file_path=token_store_path)

        # Create logger instance
        logger = Logger.get_instance(level=Logger.Levels.INFO, file_path=logger_path)

        # SDK configuration
        config = SDKConfig(auto_refresh_fields=True, pick_list_validation=False)
        
        #resource path
        resource_path = '.'

        #Initialize SDK
        Initializer.initialize(user=user, environment=environment, token=token, store=store, sdk_config=config, resource_path = resource_path, logger=logger)
    
    def get_modules(self):
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
