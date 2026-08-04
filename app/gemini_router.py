from google.genai import types

from app.config import client, MODEL_NAME
from app.function_declarations import tools
from app.prompts import ROUTING_SYSTEM_PROMPT
from app.logger import logger


def _format_history(history):
    if not history:
        return ""

    lines = []

    for turn in history[-8:]:
        sender = turn.get("sender")
        text = turn.get("text")

        if not text:
            continue

        speaker = "Assistant" if sender == "bot" else "User"
        lines.append(f"{speaker}: {text}")

    if not lines:
        return ""

    return "Conversation so far:\n" + "\n".join(lines) + "\n\n"


def route_question_gemini(question, history=None):
    """
    Asks Gemini to pick the right tool(s) using native function calling,
    with recent conversation history folded in as plain text so follow-up
    questions resolve correctly. Returns None if Gemini didn't return a
    usable function call, so the caller can fall back to the keyword router.
    """

    try:
        history_text = _format_history(history)
        prompt = f"{history_text}Current user message: {question}"

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=ROUTING_SYSTEM_PROMPT,
                tools=tools
            )
        )

        function_calls = []
        candidate = response.candidates[0]

        for part in candidate.content.parts:
            if part.function_call:
                function_calls.append({
                    "function_name": part.function_call.name,
                    "arguments": dict(part.function_call.args)
                })

        if not function_calls:
            logger.info("Gemini returned no function call.")
            return None

        logger.info(f"Gemini selected: {function_calls}")
        return function_calls

    except Exception as e:
        logger.info(f"Gemini routing failed, will fall back. Reason: {e}")
        return None