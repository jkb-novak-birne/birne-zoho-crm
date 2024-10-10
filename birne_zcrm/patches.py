def apply_zoho_patches():
    from zcrmsdk.src.com.zoho.crm.api.util.utility import Utility
    from zcrmsdk.src.com.zoho.crm.api.util import Constants
    # Save the original method for reference if needed
    original_check_data_type = Utility.check_data_type

    # Define the patched version of the static method
    @staticmethod
    def patched_check_data_type(value, type):
        # Custom behavior for handling None values
        if value is None:
            # You can customize the behavior here, for example, return True instead of False
            return True

        # Keep the original logic for other cases
        if type.lower() == Constants.OBJECT.lower():
            return True
        type = Constants.DATA_TYPE.get(type)
        class_name = value.__class__
        if class_name == type:
            return True
        else:
            return False

    # Apply the patch
    Utility.check_data_type = patched_check_data_type
