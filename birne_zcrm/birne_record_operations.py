from zcrmsdk.src.com.zoho.crm.api import HeaderMap, ParameterMap
from zcrmsdk.src.com.zoho.crm.api.record import *
from zcrmsdk.src.com.zoho.crm.api.record import Record as ZCRMRecord
from .utils import handle_list_value, handle_value

class BirneRecordOperations:
    def __init__(self, module_api_name=None, trigger=None):
        self.module_api_name = module_api_name
        self.trigger = trigger if trigger else []
        self.record_operations = RecordOperations()
        self.header_instance = HeaderMap()
    
    def perform_operation(self, operation_name, record_id=None, search_params=None, record_data:ZCRMRecord=None):
        page = 1
        has_more_records = True
        response_record_list = []

        while has_more_records:
            param_instance = self._create_param_instance(page, search_params)
            response = self._execute_operation(operation_name, record_id, param_instance, record_data)
            
            if response is None:
                return None

            response_object = response.get_object()
            if isinstance(response_object, ActionWrapper):
                return self._process_action_response(response_object)

            if isinstance(response_object, ResponseWrapper):
                response_record_list.extend(self._process_response_records(response_object))
                has_more_records = self._check_pagination(response_object)
                page += 1

            elif isinstance(response_object, APIException):
                return self._process_api_exception(response_object)
        
        return response_record_list if operation_name != "GET_RECORD" else response_record_list[0] if response_record_list else None

    def _create_param_instance(self, page, search_params=None):
        param_instance = ParameterMap()
        param_instance.add(GetRecordsParam.page, page)
        if search_params:
            param_instance.add(SearchRecordsParam.criteria, search_params)
        return param_instance
    
    def _execute_operation(self, operation_name, record_id, param_instance, record_data):
        match operation_name:
            case "GET_RECORDS":
                print(f"Fetching {self.module_api_name} - page {param_instance}")
                return self.record_operations.get_records(self.module_api_name, param_instance, self.header_instance)
            case "GET_RECORD":
                return self.record_operations.get_record(record_id, self.module_api_name, param_instance, self.header_instance)
            case "SEARCH_RECORD":
                return self.record_operations.search_records(self.module_api_name, param_instance, self.header_instance)
            case "UPDATE_RECORD":
                request = BodyWrapper()
                request.set_data([record_data])
                request.set_trigger(self.trigger)
                return self.record_operations.update_record(record_id, self.module_api_name, request, self.header_instance)
            case "CREATE_RECORD":
                request = BodyWrapper()
                request.set_data([record_data])
                request.set_trigger(self.trigger)
                return self.record_operations.create_records(self.module_api_name, request, self.header_instance)
        return None

    def _process_action_response(self, response_object):
        returnObj = {}
        for action_response in response_object.get_data():
            if isinstance(action_response, SuccessResponse):
                returnObj.update(action_response.get_details())
            elif isinstance(action_response, APIException):
                return self._process_api_exception(action_response)
        return returnObj

    def _process_response_records(self, response_object):
        record_data_list = []
        for record in response_object.get_data():
            record_dict = self._map_record_fields(record)
            record_data_list.append(record_dict)
        return record_data_list

    def _map_record_fields(self, record):
        record_dict = {
            "id": record.get_id(),
            "created_by": self._map_user_fields(record.get_created_by()),
            "modified_by": self._map_user_fields(record.get_modified_by()),
            "created_time": str(record.get_created_time()),
            "modified_time": str(record.get_modified_time())
        }
        
        # Fetch Key-Value fields
        key_values = record.get_key_values()
        for key_name, value in key_values.items():
            record_dict[key_name] = handle_value(value)
        return record_dict
    
    def _map_user_fields(self, user):
        if user is None:
            return None
        return {
            "name": user.get_name(),
            "id": user.get_id(),
            "email": user.get_email(),
        }

    def _check_pagination(self, response_object):
        info = response_object.get_info()
        return info.get_more_records() if info else False

    def _process_api_exception(self, api_exception):
        return {
            "status": api_exception.get_status().get_value(),
            "code": api_exception.get_code().get_value(),
            "details": api_exception.get_details(),
            "message": api_exception.get_message().get_value(),
        }
