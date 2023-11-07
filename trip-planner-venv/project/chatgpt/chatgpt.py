import os
import openai
from datetime import date

today = date.today().strftime("%m/%d/%Y")
print(today)

openai.api_key = "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"

user_answers = {}

# Define the questions to ask
questions = {
    "name": "What is your name?",
    "age": "How old are you?",
    "hobby": "What is your favorite hobby?",
    "start_location": "Where is your start location?",
    "end_location": "Where do you want to go?",
}

# Ask each question and save the response
for key, question in questions.items():
    user_answers[key] = input(question + " ")


# completion = openai.ChatCompletion.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": "You are a tourist guy, skilled in planning trip."},
#     {"role": "user", "content": "Is Washington a valid clear location in United State? Just answer 0 for no and 1 for yes and 2 for need more information"}
#   ]
# )

# print(completion.choices[0].message)

# print("In order to help you, I will need some information about your trip.n")
# valid_location = 0
# while valid_location == 0:
    user_input_location = input("1.Tell me about your location?")
    # print(user_input_location)
    completion = openai.chat.completions.create(
    model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a tourist guy, skilled in planning trip."},
            {"role": "user", "content": f"Is {user_input_location} a valid and unique location in United State? Answer 0 for no, 1 for yes"}
        ]
    )

    user_input_location = completion.choices[0].message.content
    # print(f"user_input_location = {user_input_location}")
    if user_input_location == "0":
        valid_location = 0
        print("I can't find your place, can you provide more information")
    elif user_input_location == "1":
        valid_location = 1
        valid_start_date = 0
        while valid_start_date == 0:
            user_input_start_date = input("2.Tell me about your start date (mm/dd/yyyy)?")
            print(f"1.user_input_start_date = {user_input_start_date}")
            completion = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a tourist guy, skilled in planning trip."},
                    {"role": "user", "content": f"Today is {today}. Try to convert {user_input_start_date} to mm/dd/yyyy format and tell me is it a valid date. Answer 0 for no, and converted format for yes, no addition information needed"}
                ]
            )
            user_input_start_date = completion.choices[0].message.content
            print(f"2.user_input_start_date = {user_input_start_date}")
            if user_input_start_date == "0":
                valid_start_date = 0
                print("That's not a valid start date")
            else:
                valid_start_date = 1
                valid_end_date = 0
                while valid_end_date == 0:
                    user_input_end_date = input("2.Tell me about your end date?")
                    completion = openai.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a tourist guy, skilled in planning trip."},
                            {"role": "user", "content": f"Is {user_input_end_date} a valid date? Answer 0 for no, and convert it to mm/dd/yyy format for yes"}
                        ]
                    )
                    user_input_end_date = completion.choices[0].message.content
                    if user_input_end_date == "0":
                        valid_end_date = 0
                        print("That's not a valid start date")
                    else:
                        valid_end_date = 1
                        completion = openai.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {"role": "system", "content": "You are a tourist guy, skilled in planning trip."},
                                {"role": "user", "content": f"Plan a trip to {user_input_location} start from {user_input_start_date} to {user_input_end_date}"}
                            ]
                        )
                        result = user_input_end_date = completion.choices[0].message.content
                        print(result)


    