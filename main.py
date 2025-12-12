import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key == None:
    raise RuntimeError("api key not found")

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt_contents", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

#user_prompt_contents = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
client = genai.Client(api_key=api_key)
#response = client.models.generate_content(
#            model='gemini-2.5-flash', contents = user_prompt_contents
#        )

#message = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]




def main():

    args = parser.parse_args()
    if args.verbose == True:
        print(f"User prompt: {args.user_prompt_contents}")
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt_contents)])]
    response = client.models.generate_content(
            model = 'gemini-2.5-flash', contents = messages)
    if not response.usage_metadata == None:
        if args.verbose == True:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else: 
        raise RuntimeError("usage_metadata is None. Likely a failed API request.")

    print("Response:")
    print(response.text)


if __name__ == "__main__":
    main()
