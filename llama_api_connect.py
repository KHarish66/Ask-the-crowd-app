import os
import requests
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Fetch API key from the .env file
api_key = os.getenv("GROQCLOUD_API_KEY")

# Define the model endpoint for llama-3.1-8b-instant
model_endpoint = "https://api.groqcloud.com/models/llama-3.1-8b-instant"

# Set up headers, including the API key
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}


# Function to summarize the Reddit comments
def summarize_reddit_comments(comments):
    # Combine the comments into a single prompt
    prompt = "Summarize the following Reddit comments in a simple and understandable way:\n\n"
    prompt += "\n\n".join(comments)  # Join all comments into one prompt

    # Define input data for the model
    input_data = {
        "prompt": prompt,
        "max_tokens": 150,  # You can adjust the max_tokens as needed
        "temperature": 0.7
    }

    # Retry logic for the API request
    max_retries = 5
    for attempt in range(max_retries):
        try:
            # Send the request to the API
            response = requests.post(model_endpoint, json=input_data, headers=headers)

            # Check if the request was successful
            if response.status_code == 200:
                result = response.json()
                return result.get('output', 'No summary found.')
            else:
                print(f"Failed with status code {response.status_code}: {response.text}")
                return "Failed to retrieve summary."

        except requests.exceptions.ConnectionError as e:
            print(f"Connection error: {e}")
            if attempt < max_retries - 1:
                print("Retrying...")
                time.sleep(5)  # Wait for 5 seconds before retrying
            else:
                print("Max retries reached. Exiting.")
                return "Connection error occurred."

