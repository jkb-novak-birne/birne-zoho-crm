from zcrmsdk.src.com.zoho.crm.api import HeaderMap, ParameterMap
from zcrmsdk.src.com.zoho.crm.api.record import *
from zcrmsdk.src.com.zoho.crm.api.record import Record as ZCRMRecord
from .utils import handle_list_value,handle_value

def getRecords(module_api_name):
    """
    This method is used to get all the records of a module and print the response.
    :param module_api_name: The API Name of the module to fetch records
    """
    has_more_records = True
    page = 1

    response_record_list = []
    # Get instance of RecordOperations Class
    record_operations = RecordOperations()

    # Get instance of ParameterMap Class
    param_instance = ParameterMap()

    # Get instance of HeaderMap Class
    header_instance = HeaderMap()

    # Call get_record method

    while has_more_records:
        param_instance = ParameterMap()
        param_instance.add(GetRecordsParam.page, page)
        print(f"Fetching {module_api_name} - page {page}")
        response = record_operations.get_records(module_api_name, param_instance, header_instance)

        if response is not None:
            if response.get_status_code() in [204, 304]:
                return None  # No content or not modified

            response_object = response.get_object()

            info = response_object.get_info()
            if info is not None:
                if info.get_more_records() is not None:
                    has_more_records = info.get_more_records()
                else:
                    has_more_records = False

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
                    response_record_list.append(record_data)
                

            elif isinstance(response_object, APIException):
                return {
                    "status": response_object.get_status().get_value(),
                    "code": response_object.get_code().get_value(),
                    "details": response_object.get_details(),
                    "message": response_object.get_message().get_value()
                }
            page += 1

    return response_record_list


