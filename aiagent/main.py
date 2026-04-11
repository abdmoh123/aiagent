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
    response = client.models.generate_content(model=GeminiModels.GEMINI_2_5_FLASH, contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.")  # pyright: ignore[reportUnknownMemberType]
    print(response.text)


if __name__ == "__main__":
    main()
