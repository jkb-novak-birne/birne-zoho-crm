from .birne_record_operations import BirneRecordOperations
from .birne_file_operations import BirneFileOperations
from .utils import handle_dict_to_record
from .update_record import update_record_wrapper
from .get_record import get_record_wrapper
def upsert_file_record_param(module_api_name, record_id, field_api_name, file_path,trigger=None):
    """
    A function to upload file and attach it to a record in a specific upload file field.
    
    :param module_api_name: The API Name of the module to update the record in.
    :param record_id: The ID of the record to update.
    :param field_api_name: Field api name of field of UPLOAD FILE type
    :param file_path: relative path of file to upload
    :param trigger: List of operations to trigger when updating the record (e.g., ["approval", "workflow", "blueprint"]).
    :return: The result of the update operation (success or failure details).
    """
    crmFile = BirneFileOperations()

    file_list = []

    record_data = get_record_wrapper(module_api_name, record_id)
    existing_files = record_data[field_api_name]

    if existing_files is not None and isinstance(existing_files, list):
        for f in existing_files:
            file_list.append((f['attachment_id'], True))
            print(f['attachment_id'])

    uploaded_file = crmFile.upload_file(file_path=file_path)

    file_id = uploaded_file['id']

    file_list.append((file_id,False))

    record_dict = {}

    record_dict[field_api_name] = file_list

    return update_record_wrapper(module_api_name,record_id,record_dict,[])