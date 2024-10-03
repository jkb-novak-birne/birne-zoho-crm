from zcrmsdk.src.com.zoho.crm.api import HeaderMap, ParameterMap
from zcrmsdk.src.com.zoho.crm.api.attachments import Attachment
from zcrmsdk.src.com.zoho.crm.api.layouts import Layout
from zcrmsdk.src.com.zoho.crm.api.record import *
from zcrmsdk.src.com.zoho.crm.api.record import Record as ZCRMRecord
from zcrmsdk.src.com.zoho.crm.api.tags import Tag
from zcrmsdk.src.com.zoho.crm.api.users import User
from zcrmsdk.src.com.zoho.crm.api.util import Choice, StreamWrapper
from datetime import datetime

def getRecordById(module_api_name, record_id):

    # Get instance of RecordOperations Class
    record_operations = RecordOperations()

    # Get instance of ParameterMap Class
    param_instance = ParameterMap()

    # Get instance of HeaderMap Class
    header_instance = HeaderMap()

    # Call get_record method
    response = record_operations.get_record(record_id, module_api_name, param_instance, header_instance)

    if response is not None:
        if response.get_status_code() in [204, 304]:
            return None  # No content or not modified

        response_object = response.get_object()

        if isinstance(response_object, ResponseWrapper):
            record_list = response_object.get_data()
            if not record_list:
                return None

            record_data = {}

            for record in record_list:
                record_dict = {}
                record_dict["id"] = record.get_id()

                created_by = record.get_created_by()
                if created_by is not None:
                    record_dict["created_by"] = {
                        "name": created_by.get_name(),
                        "id": created_by.get_id(),
                        "email": created_by.get_email(),
                    }

                record_dict["created_time"] = str(record.get_created_time())
                record_dict["modified_time"] = str(record.get_modified_time())

                modified_by = record.get_modified_by()
                if modified_by is not None:
                    record_dict["modified_by"] = {
                        "name": modified_by.get_name(),
                        "id": modified_by.get_id(),
                        "email": modified_by.get_email(),
                    }

                # Fetch Key-Value fields
                key_values = record.get_key_values()
                for key_name, value in key_values.items():
                    if isinstance(value, list):
                        record_dict[key_name] = [handle_list_value(v) for v in value]
                    else:
                        record_dict[key_name] = handle_value(value)

                record_data = record_dict

            return record_data

        elif isinstance(response_object, APIException):
            return {
                "status": response_object.get_status().get_value(),
                "code": response_object.get_code().get_value(),
                "details": response_object.get_details(),
                "message": response_object.get_message().get_value()
            }

    return None

def handle_list_value(value):
    if isinstance(value, FileDetails):
        return {
            "extn": value.get_extn(),
            "is_preview_available": value.get_is_preview_available(),
            "download_url": value.get_download_url(),
            "file_name": value.get_file_name(),
            "file_size": value.get_file_size(),
        }
    elif isinstance(value, Choice):
        return value.get_value()
    elif isinstance(value, ZCRMRecord):
        return {key: val for key, val in value.get_key_values().items()}
    elif isinstance(value, Tag):
        return {"name": value.get_name(), "id": value.get_id()}
    # Add more cases as needed for other list types
    return str(value)

def handle_value(value):
    if isinstance(value, User):
        return {"id": value.get_id(), "name": value.get_name(), "email": value.get_email()}
    elif isinstance(value, Layout):
        return {"id": value.get_id(), "name": value.get_name()}
    elif isinstance(value, ZCRMRecord):
        return {"id": value.get_id(), "name": value.get_key_value('name')}
    elif isinstance(value, Choice):
        return value.get_value()
    elif isinstance(value, datetime):
        return str(value)
    elif isinstance(value, dict):
        return {key: str(val) for key, val in value.items()}
    # Handle other value types as needed
    return str(value)