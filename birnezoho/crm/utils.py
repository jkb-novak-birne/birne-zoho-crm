from zcrmsdk.src.com.zoho.crm.api.layouts import Layout
from zcrmsdk.src.com.zoho.crm.api.record import *
from zcrmsdk.src.com.zoho.crm.api.record import Record as ZCRMRecord
from zcrmsdk.src.com.zoho.crm.api.tags import Tag
from zcrmsdk.src.com.zoho.crm.api.users import User
from zcrmsdk.src.com.zoho.crm.api.util import Choice
from zcrmsdk.src.com.zoho.crm.api.fields import *
from zcrmsdk.src.com.zoho.crm.api.fields import Field as ZCRMField
from zcrmsdk.src.com.zoho.crm.api import HeaderMap, ParameterMap
from datetime import datetime

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

def handle_dict_to_record(module_api_name:str,record_data:dict=None)->ZCRMRecord:
    fields = get_module_fields(module_api_name)
    crm_record = ZCRMRecord()
    for key, value in record_data.items():
        converted_value = convert_to_sdk_type(key,value,fields)
        crm_record.add_key_value(key,converted_value)
    return crm_record

zoho_field_mappings = {
    'lookup': ZCRMRecord, # Assuming lookups are dictionaries
    'date': str,          # Date strings can be parsed into datetime objects if needed
    'text': str,          # Text fields are mapped to strings
    'picklist': str,      # Picklist fields can be treated as strings
    'multiselect':Choice, # 
    'subform': list,      #
    'phone': str,
    'email': str,
    'integer': int,       # Integer fields are mapped to integers
    'datetime': str,      # You can later convert it to datetime
    'boolean': bool,      # Boolean fields map to Python's bool
    'double': float,      # Double fields map to Python's float
    'multiselectlookup': list,  # Multiselect lookups could be stored as lists
    'multiselectpicklist': list[Choice],
    'textarea': str,      # Text areas can also be strings
    'fileupload': dict,   # File uploads could be dictionaries (metadata about files)
    'subform': list,      # Subforms can be lists of dictionaries
    'formula': float,     # Formula fields may result in numbers
    'id': str,            # ID fields can be strings
    'autonumber': int,    # Auto-number fields are usually integers
}


def convert_to_sdk_type(field_api_name,value,fields):
    """
    Converts dictionary values to Zoho SDK objects based on the field's API name and corresponding type.
    """
    field_type = fields.get(field_api_name)
    crm_field_type = zoho_field_mappings.get(field_type)
    if crm_field_type == int:
        return int(value)
    elif crm_field_type == str:
        return str(value)
    elif crm_field_type == bool:
        return bool(value)
    elif crm_field_type == float:
        return float(value)
    elif crm_field_type == list[Choice]:
        return [Choice(x) for x in value]
    elif crm_field_type == ZCRMRecord:  # Handle lookup fields
        record_instance = ZCRMRecord()  # Create an instance of the Record class
        record_instance.set_id(value['id'])  # Assuming the lookup field contains an 'id' key
        return record_instance
    elif crm_field_type == list:
        subform = []
        for item in value:
            converted_item = handle_dict_to_record(field_api_name,item)
            subform.append(converted_item)
        return subform
    elif crm_field_type == None:
        print(f"didnt find matching type for {field_api_name}")
        return value
    # Add more conversions as necessary
    return value  # Default case

def get_module_fields(module_api_name):
    # Initialize the fields operations
    fields_operations = FieldsOperations(module_api_name)
    # Create a parameter map instance (if required)
    param_instance = ParameterMap()
    # Fetch the fields details
    fields_detail = fields_operations.get_fields(param_instance)
    # Get the fields object
    fields_objects = fields_detail.get_object()
    # Initialize a dictionary to store API name and data type
    fields_array = {}
    # Loop through the fields and populate the dictionary
    fields = fields_objects.get_fields()
    for field in fields:
        fields_array[field.get_api_name()] = field.get_data_type()
    # Optional: Add the "id" field manually
    #fields_array["id"] = "id"
    return fields_array