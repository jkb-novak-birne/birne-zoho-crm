import os 
from zcrmsdk.src.com.zoho.crm.api.user_signature import UserSignature
from zcrmsdk.src.com.zoho.crm.api.dc import EUDataCenter
from zcrmsdk.src.com.zoho.api.authenticator.oauth_token import OAuthToken
from zcrmsdk.src.com.zoho.api.authenticator.store import FileStore
from zcrmsdk.src.com.zoho.api.logger import Logger
from zcrmsdk.src.com.zoho.crm.api.sdk_config import SDKConfig
from zcrmsdk.src.com.zoho.crm.api.initializer import Initializer

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
