import os
import json
import argparse
import sys
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions
from call_function import call_function

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if not api_key:
    raise RuntimeError("OPENROUTER_API_KEY is not set in the environment variables.")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]

def chat_func():
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )

    prompt_tokens = response.usage.prompt_tokens
    Response_tokens = response.usage.completion_tokens
    message = response.choices[0].message
    messages.append(message)

    def print_response():
        if message.tool_calls:
            for tool_call in message.tool_calls:
                function_args = json.loads(tool_call.function.arguments or "{}")
                result_message = call_function(tool_call, verbose=args.verbose)
                messages.append(result_message)
                if len(result_message["content"]) == 0:
                    raise Exception("Function call failed or returned None.")
                if args.verbose:
                    print(f"-> {result_message['content']}")
            return False
        else:
            print("Response:")
            print(message.content)
            return True

    if (prompt_tokens == None) or (Response_tokens == None):
        result = False
        raise RuntimeError("Token usage information is missing in the response.")
    elif args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {Response_tokens}")
        result = print_response()
    else:
        result = print_response()
    return result

for _ in range(20):
    done = chat_func()
    if done:
        break
else:
    print("Something went wrong...")
    sys.exit(1)