import requests

# Base URL for the API
base_url = <API INVOKE URL HERE>


create_request = {
    "type": "update",
    "owner": "sajan",
    "Age" : 25,
    "Gender":"Male",
    "height" : 179
}
create_response = requests.post(base_url, json=create_request)
print("CREATE Response:", create_response.status_code, create_response.json())
