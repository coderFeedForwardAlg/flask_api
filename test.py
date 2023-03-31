import requests
data = {[1,2,3]: [4,5,6]}

responce = requests.get("http://127.0.0.1:5000/test/max")
# r = requests.post("http://127.0.0.1:5000/json_example", json=data)
r = requests.post("https://flask-api-kr3iijg4ca-uc.a.run.app/json_example", json=data)

print(r.json())