import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions

#Load the API key from the .env file. If the key is not found, raise runtime error.
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key == None:
    raise RuntimeError("api key not found")

#Define the parser for command line arguments. Accepts a prompt and an optional verbose flag.
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt_contents", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

client = genai.Client(api_key=api_key)




def main():
    #Calls the parser to get the command line arguments.
    args = parser.parse_args()

    #Separates the API call into client and messages for better organization.
    messages: list[types.Content] = [types.Content(role="user", parts=[types.Part(text=args.user_prompt_contents)])]
    
    #Calls the API to generate content based on the messages list.
    response = client.models.generate_content(
            model = 'gemini-2.5-flash', 
            contents = messages,
            config = types.GenerateContentConfig(
                tools=[available_functions], 
                system_instruction = system_prompt
                )
            )
    
    #Verbose output and error handling for missing usage metadata.
    if not response.usage_metadata == None:
        if args.verbose == True:
            print(f"User prompt: {args.user_prompt_contents}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else: 
        raise RuntimeError("usage_metadata is None. Likely a failed API request.")

    print("Response:")
    if response.function_calls == None:
        print({response.text})
    else:
        for FunctionCall in response.function_calls:
            print(f'Calling function: {FunctionCall.name}({FunctionCall.args})')


if __name__ == "__main__":
    main()
