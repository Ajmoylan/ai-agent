import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI

from call_function import available_functions, call_function
from prompts import system_prompt


parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument(
    "--verbose",
    action="store_true",
    help="Enable verbose output",
)
args = parser.parse_args()


messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]


load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

print("API key loaded:", api_key is not None)


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)


for _ in range(20):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
        temperature=0,
    )

    message = response.choices[0].message

    messages.append(message)

    if message.tool_calls:
        for tool_call in message.tool_calls:
            result_message = call_function(
                tool_call,
                verbose=args.verbose,
            )

            if not result_message["content"]:
                raise RuntimeError("Function call returned no content")

            if args.verbose:
                print(f"-> {result_message['content']}")

            messages.append(result_message)

        continue

    print("Final response:")
    print(message.content)

    if args.verbose and response.usage is not None:
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    break

else:
    print("Error: Agent reached the maximum number of iterations without finishing.")
    raise SystemExit(1)
