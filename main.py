import argparse
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.call_function import call_function
from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Generate content using Gemini API")
parser.add_argument("prompt", type=str, help="The prompt to generate content for")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

user_prompt = args.prompt
verbose = args.verbose

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]
if verbose:
    print(f"User prompt: {user_prompt}")

max_iterations = 20
iteration = 0
try:
    while iteration < max_iterations:
        iteration += 1
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
        system_instruction=system_prompt
    )
)

        if verbose:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        for candidate in response.candidates:
            messages.append(candidate.content)

        has_function_call = False
        has_text_response = False
        if response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'function_call') and part.function_call:
                    has_function_call = True
                    function_call_part = part.function_call
                    if verbose:
                        print(f" - Calling function: {function_call_part.name}")
                    
                    function_call_result = call_function(function_call_part, verbose)
                    
                    if not hasattr(function_call_result.parts[0], 'function_response'):
                        raise Exception("Fatal: Expected a function response")
                    
                    if verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")
                    
                    # Add function response to conversation
                    messages.append(function_call_result)

                elif hasattr(part, 'text') and part.text.strip():
                    has_text_response = True
                    if verbose:
                        print(f"Text response: {part.text}")
        if has_text_response and not has_function_call:
            print("Final response from agent:")
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'text') and part.text.strip():
                    print(f"-> {part.text}")
            break

        if has_function_call and not has_text_response:
            continue
        if has_function_call and has_text_response:
            continue

except Exception as e:
    print(f"Error occurred: {e}")
    sys.exit(1)

if iteration >= max_iterations:
    print("Maximum iterations reached. The agent may need more steps to complete the task.")