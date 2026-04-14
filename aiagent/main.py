"""Main endpoint for the ai-agent project."""

import argparse
from dataclasses import dataclass

from aiagent.config import gemini_api_key
from aiagent.models import GeminiModels
from aiagent.prompts import system_prompt
from aiagent.tools import available_functions, call_function
from dotenv import load_dotenv
from google import genai
from google.genai.types import Content, GenerateContentConfig, Part

# Load all environment variables from a .env file if it exists
_ = load_dotenv()


@dataclass()
class AppArgs:
    """Dataclass representing the arguments a user can pass through the CLI."""
    user_prompt: str
    verbose: bool = False


def main() -> None:
    """Main entrypoint function."""
    parser = argparse.ArgumentParser(description="AI Chatbot")
    _ = parser.add_argument("user_prompt", type=str, help="User prompt")
    _ = parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = AppArgs(**vars(parser.parse_args()))  # pyright: ignore[reportAny]

    client = genai.Client(api_key=gemini_api_key)

    messages: list[Content] = [Content(role="user", parts=[Part(text=args.user_prompt)])]
    response = client.models.generate_content(  # pyright: ignore[reportUnknownMemberType]
        model=GeminiModels.GEMINI_2_5_FLASH,
        contents=messages,
        config=GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        )
    )

    metadata = response.usage_metadata
    if not metadata:
        raise RuntimeError("API request failed!")

    prompt_token_count: int = metadata.prompt_token_count or 0
    response_token_count: int = metadata.candidates_token_count or 0
    if prompt_token_count == 0 or response_token_count == 0:
        raise RuntimeError("Prompt or response token count is 0!")

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {prompt_token_count}")
        print(f"Response tokens: {response_token_count}")

    if response.function_calls:
        func_results: list[list[Part]] = []
        for function_call in response.function_calls:
            func_call_res = call_function(function_call, verbose=args.verbose)

            func_parts = func_call_res.parts
            if not func_parts:
                raise ValueError("Missing parts property in function call response")

            func_response = func_parts[0].function_response
            if not func_response:
                raise ValueError("Missing function_response property in function call response")
            if not func_response.response:
                raise ValueError("Missing response property in function call response")

            func_results.append(func_parts)

            if args.verbose:
                print(f"-> {func_response.response}")
    else:
        print(f"Response:\n{response.text}")


if __name__ == "__main__":
    main()
