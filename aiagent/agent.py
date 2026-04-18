"""Functions related to the agent."""

from enum import Enum

from aiagent.context import Context
from aiagent.models import GeminiModels
from aiagent.prompts import system_prompt
from aiagent.tools import available_functions, call_function
from google.genai import Client
from google.genai.types import Content, GenerateContentConfig, Part


class AgentResult(Enum):
    """Enum representing the result of the agent."""

    DONE = 0
    CONTINUE = 1


def init_context(user_prompt: str, is_verbose: bool = False) -> None:
    """Initialises the messages list for the agent in preparation for run_agent.

    Args:
        user_prompt: The initial prompt/message sent from the user.
        is_verbose: Whether to print verbose output.
    """
    if is_verbose:
        print(f"User prompt: {user_prompt}")

    Context().add_messages([Content(role="user", parts=[Part(text=user_prompt)])])


def run_agent(
    client: Client, is_verbose: bool = False
) -> AgentResult:
    """Runs the agent.

    Args:
        client: The gemini client to use (with credentials).
        user_prompt: The prompt to send to the agent.
        is_verbose: Whether to print verbose output.
    """
    response = client.models.generate_content(  # pyright: ignore[reportUnknownMemberType]
        model=GeminiModels.GEMINI_2_5_FLASH,
        contents=Context().messages,
        config=GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        )
    )

    # Add candidates content to singleton messages list
    if response.candidates:
        Context().add_messages(
            [c.content for c in response.candidates if c.content]
        )

    metadata = response.usage_metadata
    if not metadata:
        raise RuntimeError("API request failed!")

    prompt_token_count: int = metadata.prompt_token_count or 0
    response_token_count: int = metadata.candidates_token_count or 0
    if prompt_token_count == 0 or response_token_count == 0:
        raise RuntimeError("Prompt or response token count is 0!")

    if is_verbose:
        print(f"Messages: {Context().messages}")
        print(f"Prompt tokens: {prompt_token_count}")
        print(f"Response tokens: {response_token_count}")

    if response.function_calls:
        func_results: list[list[Part]] = []
        for function_call in response.function_calls:
            func_call_res = call_function(function_call, verbose=is_verbose)

            func_parts = func_call_res.parts
            if not func_parts:
                raise ValueError("Missing parts property in function call response")

            func_response = func_parts[0].function_response
            if not func_response:
                raise ValueError("Missing function_response property in function call response")
            if not func_response.response:
                raise ValueError("Missing response property in function call response")

            func_results.append(func_parts)

            # Add the function's result to the messages list
            Context().add_message(Content(role="user", parts=func_parts))

            if is_verbose:
                print(f"-> {func_response.response}")

        # If the agent had to run a function, then it might not be done yet
        return AgentResult.CONTINUE
    else:
        print(f"Response:\n{response.text}")
        # Usually, if the agent sends a text message, then it probably has no
        # functional task to do and therefore, the agent is done
        return AgentResult.DONE
