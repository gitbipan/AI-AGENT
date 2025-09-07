import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key,
                      http_options=types.HttpOptions(api_version='v1alpha')
                      )
if len(sys.argv) <2:
    print("No arguments provided")
    user_input = input("Enter your prompt: ")
else:
    print("Args", sys.argv)
    user_input = sys.argv[1]
messages = [
    types.Content(role="user", parts=[types.Part(text=user_input)]),
]


response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
)

print(response.text)
print(f"Prompt Tokens:{response.usage_metadata.prompt_token_count}")
print(f"Response Tokens:{response.usage_metadata.candidates_token_count}")