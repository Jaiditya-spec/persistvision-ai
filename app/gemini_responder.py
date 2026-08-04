import json

from google.genai import types

from app.config import client, MODEL_NAME
from app.prompts import RESPONSE_SYSTEM_PROMPT, CONVERSATIONAL_SYSTEM_PROMPT, ASSUMPTION_INSIGHTS_SYSTEM_PROMPT, BLOCK_COMMENTARY_SYSTEM_PROMPT
from app.logger import logger


def generate_ai_final_answer(question, tool_results):
    """
    Sends the tool results to Gemini and asks it to write a clear,
    professional final answer grounded strictly in that data.
    Returns None if the call fails, so the caller falls back to the
    deterministic formatter.
    """

    try:
        payload = json.dumps(tool_results, default=str)

        prompt = (
            f"User question: {question}\n\n"
            f"Tool results (JSON): {payload}\n\n"
            "Write the final answer for the user based only on this data."
        )

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=RESPONSE_SYSTEM_PROMPT
            )
        )

        text = response.text

        if not text or not text.strip():
            return None

        logger.info("Gemini generated the final answer.")
        return text.strip()

    except Exception as e:
        logger.info(f"Gemini final-answer generation failed, will fall back. Reason: {e}")
        return None


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


def generate_conversational_reply(question, history=None):
    """
    Handles greetings / small talk / vague / off-topic messages that
    don't need a tool call. Returns None on failure.
    """

    try:
        history_text = _format_history(history)
        prompt = f"{history_text}Current user message: {question}"

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=CONVERSATIONAL_SYSTEM_PROMPT
            )
        )

        text = response.text

        if not text or not text.strip():
            return None

        return text.strip()

    except Exception as e:
        logger.info(f"Gemini conversational reply failed. Reason: {e}")
        return None


def generate_assumption_insights(cohort_results):
    """
    Writes the executive summary for the Assumption Setting Word report,
    grounded strictly in the cohort results. Returns None on failure so
    the caller can fall back to a generic placeholder paragraph.
    """

    try:
        payload = json.dumps(cohort_results, default=str)

        prompt = (
            f"Cohort results (JSON): {payload}\n\n"
            "Write the executive summary for the assumption setting report "
            "based only on this data."
        )

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=ASSUMPTION_INSIGHTS_SYSTEM_PROMPT
            )
        )

        text = response.text

        if not text or not text.strip():
            return None

        logger.info("Gemini generated the assumption-setting executive summary.")
        return text.strip()

    except Exception as e:
        logger.info(f"Gemini executive summary generation failed. Reason: {e}")
        return None


def generate_block_commentaries(full_breakdown):
    """
    Writes per-block (ERA x Channel) commentary for the Word report in a
    single Gemini call, rather than one call per block. Returns a dict
    keyed by (era, channel) -> commentary text. Returns an empty dict on
    failure, so the caller can fall back to a generic per-block note.
    """

    try:
        payload = json.dumps(full_breakdown, default=str)

        prompt = (
            f"Full breakdown for all 28 blocks (JSON): {payload}\n\n"
            "Write the per-block commentary as described, for every block "
            "in this list."
        )

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=BLOCK_COMMENTARY_SYSTEM_PROMPT
            )
        )

        text = response.text

        if not text or not text.strip():
            return {}

        cleaned = text.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`")
            if cleaned.lower().startswith("json"):
                cleaned = cleaned[4:]
            cleaned = cleaned.strip()

        parsed = json.loads(cleaned)

        commentary_map = {}
        for item in parsed:
            key = (item.get("era"), item.get("channel"))
            commentary_map[key] = item.get("commentary", "")

        logger.info(f"Gemini generated commentary for {len(commentary_map)} blocks.")
        return commentary_map

    except Exception as e:
        logger.info(f"Gemini block commentary generation failed. Reason: {e}")
        return {}