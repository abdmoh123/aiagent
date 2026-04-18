"""Main endpoint for the ai-agent project."""

import argparse

from aiagent.agent import AgentResult, init_context, run_agent
from aiagent.config import AppArgs, gemini_api_key
from dotenv import load_dotenv
from google import genai

# Load all environment variables from a .env file if it exists
_ = load_dotenv()


def main() -> None:
    """Main entrypoint function."""
    parser = argparse.ArgumentParser(description="AI Chatbot")
    _ = parser.add_argument("user_prompt", type=str, help="User prompt")
    _ = parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = AppArgs(**vars(parser.parse_args()))  # pyright: ignore[reportAny]

    client = genai.Client(api_key=gemini_api_key)
    init_context(args.user_prompt, is_verbose=args.verbose)

    max_runs: int = 20
    result: AgentResult = AgentResult.CONTINUE
    for _ in range(max_runs):
        try:
            result = run_agent(client, args.verbose)
            if (result == AgentResult.DONE):
                break
        except Exception as e:
            # Exit the loop early if an error occurs
            print(f"Agent error: {e}")
            exit(1)

    # Notify user if agent kept retrying indefinitely
    if result == AgentResult.CONTINUE:
        print("Agent has reached the maximum number of runs. Please try again later.")
        exit(1)


if __name__ == "__main__":
    main()
