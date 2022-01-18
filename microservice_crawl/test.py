import requests
import json

host = "http://172.20.10.5:5001/crawl"

resp = requests.get(host)

if resp.status_code == 200:
    data = json.loads(resp.text)
    print(data) #dict
else:
    print(f'HTTP Error code = {resp.status_code}')