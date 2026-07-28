import requests

url = "https://official-joke-api.appspot.com/random_joke"

response=requests.get(url)

if response.status_code == 200:
    number_data = response.json()
    print(number_data)
else:
    print("Failed to retrieve the data")