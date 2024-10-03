from zcrmsdk.src.com.zoho.crm.api import HeaderMap, ParameterMap
from zcrmsdk.src.com.zoho.crm.api.query import *

def coqlQuery(query):
    query_operations = QueryOperations()
    body_wrapper = BodyWrapper()
    body_wrapper.set_select_query(query)
    response = query_operations.get_records(body_wrapper)
    record_array = []
    if response is not None:

        # Get the status code from response
        #print('Status Code: ' + str(response.get_status_code()))

        if response.get_status_code() in [204, 304]:
            print('No Content' if response.get_status_code() == 204 else 'Not Modified')
            return record_array

        # Get object from response
        response_object = response.get_object()

        if response_object is not None:

            # Check if expected ResponseWrapper instance is received.
            if isinstance(response_object, ResponseWrapper):

                # Get the list of obtained Record instances
                record_list = response_object.get_data()

                for record in record_list:
                    resp_record = {}
                    #print('Record KeyValues: ')

                    key_values = record.get_key_values()

                    for key_name, value in key_values.items():

                        if isinstance(value, list):
                            #print("Record KeyName : " + key_name)

                            for data in value:
                                if isinstance(data, dict):
                                    for dict_key, dict_value in data.items():
                                        #print(dict_key + " : " + str(dict_value))
                                        resp_record[key_name + "_" +dict_key] = dict_value


                                else:
                                    print(str(data))

                        elif isinstance(value, dict):
                            #print("Record KeyName : " + key_name + " -  Value : ")

                            for dict_key, dict_value in value.items():
                               # print(dict_key + " : " + str(dict_value))
                                resp_record[key_name + "_" +dict_key] = dict_value

                        else:
                            #print("Record KeyName : " + key_name + " -  Value : " + str(value))
                            resp_record[key_name] = value
                    record_array.append(resp_record)
                    info = response_object.get_info()

                    if info is not None:
                        #if info.get_count() is not None:
                            # Get the Count from Info
                            #print('Record Info Count: ' + str(info.get_count()))

                        if info.get_more_records() is not None:
                            # Get the MoreRecords from Info
                            if info.get_more_records() == True:
                                print('Record Info MoreRecords: ' + str(info.get_more_records()))

            # Check if the request returned an exception
            elif isinstance(response_object, APIException):
                # Get the Status
                print("Status: " + response_object.get_status().get_value())

                # Get the Code
                print("Code: " + response_object.get_code().get_value())

                print("Details")

                # Get the details dict
                details = response_object.get_details()

                for key, value in details.items():
                    print(key + ' : ' + str(value))

                # Get the Message
                print("Message: " + response_object.get_message().get_value())
    return record_array