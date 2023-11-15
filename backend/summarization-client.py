import requests

# Define the URL of your Flask API
API_URL = 'http://localhost:5000/summarize_transcript'

# Define the transcript you want to summarize
transcript = """
[Music] my parents always told me i was destined for greatness [Music] [Applause] [Music] and with that firmly held belief i never cowered and i never quit [Music] i'm sure it's so mankind and helpful my name as the board may have told you we'll see you with him adam is too smart to do anything dumb right sly boy you are not falling for evan armstrong please say that i think i need to transfer why do you even like someone like her but she's nothing special [Music] i'm going to become a supreme court judge 15 what happened if i'm not the best then what am i [Music] i'm finally ready to move forward with my life will you get mad again [Music] [Applause] [Music] everybody on knows radios [Music] [Music] make sure hey ollie didn't see you there you
"""

# Create a JSON payload with the transcript
payload = {'transcript': transcript}

# Send a POST request to the API
response = requests.post(API_URL, json=payload)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    summarized_transcript = data.get('summarized_transcript')
    print("Original Transcript:")
    print(transcript)
    print("\nSummarized Transcript:")
    print(summarized_transcript)
else:
    print("Error:", response.status_code, response.text)
