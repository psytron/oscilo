




import requests



url = "http://ip.jsontest.com/"
response = requests.get(url)
data = response.json()
print(data)
