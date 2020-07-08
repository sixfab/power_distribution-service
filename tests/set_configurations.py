import requests

r = requests.post('http://localhost:1453/configurations')

print(r.text)