import requests

for k in range(100,700):
    requests.get("http://127.0.0.1:8000/api/db_get_id/"+f"{k}")
