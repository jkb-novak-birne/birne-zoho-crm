# birne-zoho-crm
wrapper library for easier handling zoho crm requests

## Installation

```bash
pip install git+https://github.com/jkb-novak-birne/birne-zoho-crm.git
```

## Usage
Here is a sample usage for the library:

```python
from birnezoho.crm import ZohoCRMWrapper

# Initialize the ZohoCRMWrapper with your credentials
crm = ZohoCRMWrapper(
    client_id='',
    client_secret='',
    refresh_token='',
    redirect_url='https://example.com',
    user_email='email@example.com'
)

# Fetch available modules from Zoho CRM
modules = crm.get_modules()
print(modules)
```

### Fetch a Record by ID

```python
record = crm.getRecordById(module_api_name='Leads', record_id='1234567890')
print(record)
```

### Search Records

```python
search_criteria = "(Last_Name:starts_with:Smith)"
records = crm.searchRecords(module_api_name='Leads', searchCriteria=search_criteria)
print(records)
```

### Get All Records

```python
records = crm.getRecords(module_api_name='Leads')
print(records)
```

### Update a Record

```python
record_data = {
    'Last_Name': 'Doe',
    'First_Name': 'John'
}
result = crm.updateRecord(module_api_name='Leads', record_id='1234567890', record_data=record_data)
print(result)
```

### Create a Record

```python
record_data = {
    'Last_Name': 'Doe',
    'First_Name': 'Jane'
}
result = crm.createRecord(module_api_name='Leads', record_data=record_data)
print(result)
```

### Upsert File Record Parameter

```python
result = crm.upsertFileRecordParam(
    module_api_name='Leads',
    record_id='1234567890',
    field_api_name='File_Upload',
    file_path='path/to/your/file.txt'
)
print(result)
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.