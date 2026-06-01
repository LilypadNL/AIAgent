from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions


#Calls the API to generate content based on the messages list.
def generate_content(client, messages: list[types.Content]) -> types.GenerateContentResponse:
    
    generated_content = client.models.generate_content(
        model = 'gemini-2.5-flash',
        contents = messages,
        config = types.GenerateContentConfig(
            tools = [available_functions],
            system_instruction = system_prompt
        )
    )
    return generated_content
