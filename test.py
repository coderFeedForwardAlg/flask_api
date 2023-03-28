import requests
data = {"name": "max"}

responce = requests.get("http://127.0.0.1:5000/test/max")
r = requests.post("http://127.0.0.1:5000/json_example", json=data)
print(r.json())