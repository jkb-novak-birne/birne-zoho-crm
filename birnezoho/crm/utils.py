from zcrmsdk.src.com.zoho.crm.api.layouts import Layout
from zcrmsdk.src.com.zoho.crm.api.record import *
from zcrmsdk.src.com.zoho.crm.api.record import Record as ZCRMRecord
from zcrmsdk.src.com.zoho.crm.api.tags import Tag
from zcrmsdk.src.com.zoho.crm.api.users import User
from zcrmsdk.src.com.zoho.crm.api.util import Choice
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