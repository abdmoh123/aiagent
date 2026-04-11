"""Main endpoint for the ai-agent project."""

import argparse
from dataclasses import dataclass

from aiagent.config import gemini_api_key
from aiagent.models import GeminiModels
from dotenv import load_dotenv
from google import genai
from google.genai.types import Content, Part

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
    response = client.models.generate_content(model=GeminiModels.GEMINI_2_5_FLASH, contents=messages)  # pyright: ignore[reportUnknownMemberType]

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
    print(f"Response:\n{response.text}")


if __name__ == "__main__":
    main()
