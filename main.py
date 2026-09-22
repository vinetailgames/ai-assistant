import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if not api_key:
    raise RuntimeError("OPENROUTER_API_KEY is not set in the environment variables.")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

user_prompt = "Why is Boot.dev such a great platform for learning backend development? Use one paragraph maximum"

response = client.chat.completions.create(
    model="openrouter/free",
    messages=[
        {
            "role": "user",
            "content": user_prompt
        }
    ],
)

print(f"User prompt: {user_prompt}")

prompt_tokens = response.usage.prompt_tokens
Response_tokens = response.usage.completion_tokens

if (prompt_tokens or Response_tokens) == None:
    raise RuntimeError("Token usage information is missing in the response.")
else:
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {Response_tokens}")

print("Response:")
print(response.choices[0].message.content)