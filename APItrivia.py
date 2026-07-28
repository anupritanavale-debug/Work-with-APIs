import requests



# Trivia API endpoint

url = "https://opentdb.com/api.php?amount=3&type=multiple&category=17"  # Fetch 3 questions



# Send GET request to fetch trivia questions

response = requests.get(url)



# Check if the request was successful

if response.status_code == 200:

    trivia_data = response.json()

    score = 0



    # Loop through each trivia question

    for i, question_data in enumerate(trivia_data["results"]):

        print(f"Question {i + 1}: {question_data['question']}")

        options = question_data['incorrect_answers'] + [question_data['correct_answer']]  # Add correct answer to options

        options = sorted(options)  # Shuffle options

        for j, option in enumerate(options):

            print(f"{j + 1}. {option}")



        # Collect user's answer

        user_answer = input("Your answer (1/2/3/4): ")



        # Check if the answer is correct

        if options[int(user_answer) - 1] == question_data["correct_answer"]:

            print("Correct!")

            score += 1

        else:

            print(f"Wrong! The correct answer was: {question_data['correct_answer']}")



        print("\n")



    print(f"Your final score: {score}/{len(trivia_data['results'])}")



else:

    print("Failed to retrieve trivia")