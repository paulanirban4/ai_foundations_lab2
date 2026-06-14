from requests import request
from pydantic import BaseModel, ValidationError
import requests

#1. Define the Validation Model
class UserInsight(BaseModel):
    user_name: str
    sentiment_score: int
    is_flagged_for_review: bool

print("--- MODEL INITIALIZED ---")
print(
    "Pydantic Schema enforces: "
    "user_name (str), sentiment_score (int), "
    "is_flagged_for_review (bool)\n"
)

#2. Construct and Execute API Call
def analyze_user_data_via_api():
    

    api_url = "https://jsonplaceholder.typicode.com/posts"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer sk-mock-api-key-12345"
    }

    payload = {
        "model": "gpt-4-turbo",
        "messages": [
            {
                "role": "system",
                "content": "You analyze user sentiment."
            },
            {
                "role": "user",
                "content": "Analyze the sentiment for user 'Alice'."
            }
        ]
    }

    print("--- TRANSMITTING HTTP POST REQUEST ---")
    try:
        response = requests.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=5
        )
        # Raise error if status code is 4xx or 5xx
        response.raise_for_status()
        print(f"Network Success! Status Code: {response.status_code}\n")

    except request.exceptions.RequestException as e:
        print(f"[NETWORK CRASH] Failed to reach API: {e}")
        return None



if __name__ == "__main__":
    raw_api_data = analyze_user_data_via_api()

    if raw_api_data:
        print("--- VALIDATING RAW LLM OUTPUT ---")
        print(f"Raw Data received: {raw_api_data}")

        try:
            # Step B: Validate raw data using Pydantic
            validated_insight = UserInsight(**raw_api_data)

            print("--- VALIDATION SUCCESSFUL! ---")
            print(f"Secured Object: {validated_insight}")

            # Now sentiment_score is a real integer
            print(
                f"Cleaned Score (Now a true Integer): "
                f"{validated_insight.sentiment_score + 10}"
            )

            # Now is_flagged_for_review is a real boolean
            print(
                f"Review Flag Type: "
                f"{type(validated_insight.is_flagged_for_review)}"
            )

        except ValidationError as e:
            print(
                "[VALIDATION CRASH] "
                "The LLM failed to match our schema:\n"
            )
            print(e.json())
        

        
