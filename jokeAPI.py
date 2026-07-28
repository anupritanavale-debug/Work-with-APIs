import requests



# Define the API endpoint

url = "https://official-joke-api.appspot.com/random_joke"



# Send GET request to the API

response = requests.get(url)



# Check if the request was successful

if response.status_code == 200:

    # Parse the JSON response

    joke_data = response.json()

    print(f"Joke: {joke_data['setup']} - {joke_data['punchline']}")

else:

    print(f"Failed to retrieve joke. Status code: {response.status_code}")