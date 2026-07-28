import requests

url="https://opentdb.com/api.php?amount=10&type=multiple"

response=requests.get(url)

if response.status_code==200:
    trivia_data = response.json()
    print(trivia_data)

else:
    print("Failed to retrieve trivia")