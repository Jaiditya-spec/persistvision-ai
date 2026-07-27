from app.router import route_question
from app.executor import execute_function_calls


def generate_final_answer(question, tool_results):
    """
    Convert tool outputs into a human-readable response
    without calling Gemini again.
    """

    if not tool_results:
        return "No information was found."

    lines = []

    for item in tool_results:

        result = item["result"]

        if result["status"] != "success":
            lines.append(result["message"])
            continue

        if "overall_persistency" in result:
            lines.append(
                f"Overall Persistency : {result['overall_persistency']}%"
            )

        elif "product" in result:
            lines.append(
                f"{result['product']} Persistency : {result['persistency']}%"
            )

        elif "line_of_business" in result:
            lines.append(
                f"{result['line_of_business']} Persistency : {result['persistency']}%"
            )

        elif "duration" in result:
            lines.append(
                f"Duration {result['duration']} Persistency : {result['persistency']}%"
            )

    return "\n".join(lines)


def ask_agent(question):

    function_calls = route_question(question)

    if not function_calls:
        return "Sorry, I couldn't understand your question."

    tool_results = execute_function_calls(function_calls)

    return generate_final_answer(question, tool_results)