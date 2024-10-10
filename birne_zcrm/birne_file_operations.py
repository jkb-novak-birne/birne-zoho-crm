from zcrmsdk.src.com.zoho.crm.api.file import *
from zcrmsdk.src.com.zoho.crm.api import ParameterMap
from zcrmsdk.src.com.zoho.crm.api.util import StreamWrapper
import os

class BirneFileOperations:
    def __init__(self):
        self.file_operations = FileOperations()
        self.param_instance = ParameterMap()
        self.request = BodyWrapper()

    def upload_file(self, file_path):
        # Get the directory of the root script (Jupyter notebook or script)
        root_dir = os.getcwd()

        # Combine the root directory with the relative path
        absolute_path = os.path.abspath(os.path.join(root_dir, file_path))    

        stream_wrapper2 = StreamWrapper(file_path=absolute_path)

        self.request.set_file([stream_wrapper2]) #, stream_wrapper2, stream_wrapper3])
        
        response = self.file_operations.upload_files(self.request, self.param_instance)
        response_object = response.get_object()
        return self._process_action_response(response_object)        


    def _process_action_response(self, response_object):
        returnObj = {}
        for action_response in response_object.get_data():
            if isinstance(action_response, SuccessResponse):
                returnObj.update(action_response.get_details())
            elif isinstance(action_response, APIException):
                return self._process_api_exception(action_response)
        return returnObj
    