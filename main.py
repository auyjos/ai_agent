import argparse
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Generate content using Gemini API")
parser.add_argument("prompt", type=str, help="The prompt to generate content for")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

user_prompt = args.prompt
verbose = args.verbose

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]
response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=messages
)

if verbose:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")