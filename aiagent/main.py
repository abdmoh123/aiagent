"""Main endpoint for the ai-agent project."""

from aiagent.config import gemini_api_key
from aiagent.models import GeminiModels
from dotenv import load_dotenv
from google import genai

# Load all environment variables from a .env file if it exists
_ = load_dotenv()


def main() -> None:
    """Main entrypoint function."""
    client = genai.Client(api_key=gemini_api_key)

    user_prompt: str = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    response = client.models.generate_content(model=GeminiModels.GEMINI_2_5_FLASH, contents=user_prompt)  # pyright: ignore[reportUnknownMemberType]

    metadata = response.usage_metadata
    if not metadata:
        raise RuntimeError("API request failed!")

    prompt_token_count: int = metadata.prompt_token_count or 0
    response_token_count: int = metadata.candidates_token_count or 0
    if prompt_token_count == 0 or response_token_count == 0:
        raise RuntimeError("Prompt or response token count is 0!")

    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {prompt_token_count}")
    print(f"Response tokens: {response_token_count}")
    print(f"Response:\n{response.text}")


if __name__ == "__main__":
    main()
