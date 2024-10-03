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