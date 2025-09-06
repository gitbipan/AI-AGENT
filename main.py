import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key,
                      http_options=types.HttpOptions(api_version='v1alpha')
                      )
response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=input("Enter your prompt: ")
)
print(response.text)