import requests
import datetime

server_url = "http://188.245.216.211"

print(datetime.datetime.now().isoformat)

requests.post(f"{server_url}:8000/api/normattiva", json={
    "dateTime": datetime.datetime.now().isoformat(),
    "fileName": "test_report.pdf",
    "fileLink": f'{server_url}/public/download/2024/test_report.pdf',
    "status": True
})