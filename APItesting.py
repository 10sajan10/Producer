import requests

# Base URL for the API
base_url = "https://lril85htk0.execute-api.us-east-1.amazonaws.com/prod/widgets"


create_request = {
    "type": "merge",
    "widgetId": "63738ediuduiy983",
    "owner": "sajan",
    "Age" : 25,
    "Gender":"Male",
    "height" : 172
}
create_response = requests.post(base_url, json=create_request)
print("CREATE Response:", create_response.status_code, create_response.json())
