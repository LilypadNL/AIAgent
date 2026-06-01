import os
import argparse
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function
from generate_content import generate_content

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
    
    #Limiting iterations to 20 to limit API token usage.
    for iteration in range(20):

        #calls client.models.generate_content to API to generate content based on the message list. 
        response = generate_content(client, messages)

        #Verbose output and error handling for missing usage metadata.
        if not response.usage_metadata == None:
            if args.verbose == True:
                print(f"User prompt: {args.user_prompt_contents}")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        else: 
            raise RuntimeError("usage_metadata is None. Likely a failed API request.")

        
        #Ensure that in each loop the model is aware of the messages and tool requests previously generated. Check if response has a .candidates property.
        if response.candidates != None: 
            for candidate in response.candidates:
                messages.append(candidate.content)
        
        #If there are no function calls, the API has come up with a solution and we can return the response.
        if response.function_calls == None:
            print("Response:")
            print({response.text})
            return
        else:
            function_results = []
            for FunctionCall in response.function_calls:
                function_call_result = call_function(FunctionCall, verbose = args.verbose)
                if function_call_result.parts == None: 
                    raise RuntimeError("types.Content object from call_function has no parts.")
                if function_call_result.parts[0].function_response == None:
                    raise RuntimeError("types.Part object from call_function has no function_response.")
                if function_call_result.parts[0].function_response.response == None:
                    raise RuntimeError("function_response object from call_function has no response.")
                function_results.append(function_call_result.parts[0])
                if args.verbose == True:
                    print(f'-> {function_call_result.parts[0].function_response.response}')
            messages.append(types.Content(role="user", parts=function_results))
                


    if iteration == 20:
        print("Maximum iterations reached. Ending process.")
        sys.exit(1)



if __name__ == "__main__":
    main()
