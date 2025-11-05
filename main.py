import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.write_file import schema_write_file
from functions.get_files_content import schema_get_files_content
from functions.run_python_file import schema_run_python_file
from call_function import call_function
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key,
                      http_options=types.HttpOptions(api_version='v1alpha')
                      )
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read the content of a file
- Write to a file(create or update)
- Run a python file with optional arguments
When the user asks about code projects, they are reffering to the working directory. So, you should typically start by looking at the projects files and figuring out how to run the project and how to run its tests. you will always want to run the tests before you make any changes to the code and then verify that behaviour is working.
All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
if len(sys.argv) <2:
    print("No arguments provided")
    user_input = input("Enter your prompt: ")
    verbose_flag = False
elif len(sys.argv) == 3 and sys.argv[2] == "--verbose":
    user_input = sys.argv[1]
    verbose_flag = True
else:
    print("Args", sys.argv)
    user_input = sys.argv[1] 
    verbose_flag = False
    
messages = [
    types.Content(role="user", parts=[types.Part(text=user_input)]),
]

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_run_python_file,
        schema_get_files_content,
        schema_write_file,
    ]
)
config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
)
max_iters=20
for i in range(0,max_iters):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=config,
    )
    if response is None or response.usage_metadata is None:
        print("response is malformed")
        sys.exit(1)
    if verbose_flag:
        print(f"Prompt Tokens:{response.usage_metadata.prompt_token_count}")
        print(f"Response Tokens:{response.usage_metadata.candidates_token_count}")
    if response.candidates:
        for candidate in response.candidates:
            if candidate is None or candidate.content is None:
                continue
            messages.append(candidate.content)     
    if response.function_calls:
        for function_call_part in response.function_calls:
            result = call_function(function_call_part, verbose_flag)
            messages.append(result)
    else:
        print(response.text)
        break


