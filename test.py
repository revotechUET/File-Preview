from sendRequest import sendRequest
import json

headers = {'content-type': 'application/json', 'Authorization': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Imh1bmduayIsIndob2FtaSI6Im1haW4tc2VydmljZSIsInJvbGUiOjIsImNvbXBhbnkiOiJFU1MiLCJpYXQiOjE1NzE2MjY1MTYsImV4cCI6MTU3MjQ5MDUxNn0.Pu_Z6Im_wq8XMZmsTqF5wOv4UyB5UWwaZlDLopi3VV0",
           "Storage-Database": json.dumps({"directory": "a9af296dfffec96d57e93949903d2e2391ffa851", "name": "ESS-hungnk", "company": "ESS"})}

params = {
    'file_path': '/A/B/Book1 (Autosaved).xlsx'
}
response = sendRequest(headers, params)
print(response.headers)
print(response.content)
