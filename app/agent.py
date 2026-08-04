from app.router import route_question
from app.gemini_router import route_question_gemini
from app.gemini_responder import generate_ai_final_answer, generate_conversational_reply
from app.executor import execute_function_calls


def generate_final_answer(question, tool_results):
    """
    Deterministic fallback formatter — used only if Gemini's own
    final-answer generation fails.
    """

    if not tool_results:
        return "No information was found."

    lines = []

    for item in tool_results:

        result = item["result"]

        if result["status"] != "success":
            lines.append(result["message"])
            continue

        if "prophet_updates" in result:
            lines.append(
                f"Assumption Setting complete — {result['cohorts_updated']} cohorts updated "
                f"({result['improved']} improved, {result['declined']} declined, {result['unchanged']} unchanged). "
                f"Files generated: {result['summary_file']}, {result['prophet_file']}, and {result['word_file']}."
            )
            for row in result["prophet_updates"]:
                tag = "[UP]" if row["zone"] == "green" else "[DOWN]" if row["zone"] == "red" else "[FLAT]"
                lines.append(
                    f"{tag} {row['era']} | {row['channel']} | {row['pay_type']} : "
                    f"prior {row['prior_assumption_duration1']*100:.2f}% -> "
                    f"proposed {row['proposed_assumption_duration1']*100:.2f}% "
                    f"(ultimate {row['proposed_assumption_ultimate']*100:.2f}%)"
                )

        elif "results" in result and "threshold" in result:
            if result["flagged_count"] == 0:
                lines.append(
                    f"No cohorts are out of line with assumptions by more than 2 points at "
                    f"Duration {result['duration_checked']}. Prophet table saved as "
                    f"{result['prophet_file']} (no changes)."
                )
            else:
                lines.append(
                    f"Red/Green Zone: {result['flagged_count']} cohort(s) deviating from assumptions "
                    f"by more than 2 points at Duration {result['duration_checked']}. Prophet table "
                    f"saved as {result['prophet_file']} with only these cohorts updated:"
                )
                for r in result["results"]:
                    tag = "[UP]" if r["zone"] == "green" else "[DOWN]"
                    lines.append(
                        f"{tag} {r['era']} | {r['channel']} | {r['pay_type']} : "
                        f"actual {r['latest_actual']*100:.2f}% vs proposed {r['proposed_assumption']*100:.2f}% "
                        f"({r['deviation']*100:+.2f} pts)"
                    )

        elif "products" in result:
            lines.append(f"Product breakdown for {result['era']} | {result['channel']} | {result['pay_type']}:")
            for p in result["products"]:
                lines.append(
                    f"{p['product']} : {p['previous_persistency']}% -> {p['latest_persistency']}% "
                    f"({'+' if p['change'] and p['change'] > 0 else ''}{p['change']}%)"
                )

        elif "results" in result:
            lines.append("Experience Analysis (Oct 25 vs Jun 26):")
            for row in result["results"]:
                tag = "[UP]" if row["zone"] == "green" else "[DOWN]" if row["zone"] == "red" else "[FLAT]"
                sign = "+" if row["change"] > 0 else ""
                lines.append(
                    f"{tag} {row['era']} | {row['channel']} | {row['pay_type']} : "
                    f"{row['persistency_period1']}% -> {row['persistency_period2']}% "
                    f"({sign}{row['change']}%)"
                )

        elif "overall_persistency" in result:
            lines.append(f"Overall Persistency : {result['overall_persistency']}%")

        elif "product" in result:
            lines.append(f"{result['product']} Persistency : {result['persistency']}%")

        elif "line_of_business" in result:
            lines.append(f"{result['line_of_business']} Persistency : {result['persistency']}%")

        elif "duration" in result:
            lines.append(f"Duration {result['duration']} Persistency : {result['persistency']}%")

        elif "filters" in result:
            filt_desc = ", ".join(f"{k}={v}" for k, v in result["filters"].items())
            lines.append(
                f"Persistency for {filt_desc} ({result['period']}) : {result['persistency']}%"
            )

    return "\n".join(lines)


def ask_agent(question, history=None):

    function_calls = route_question_gemini(question, history)

    if not function_calls:
        function_calls = route_question(question)

    if not function_calls:
        conversational = generate_conversational_reply(question, history)
        if conversational:
            return conversational
        return (
            "Sorry, I couldn't understand your question. Try asking about "
            "overall, product, Line of Business, or duration persistency, "
            "'do experience analysis', 'do assumption setting', or "
            "'identify red zone'."
        )

    tool_results = execute_function_calls(function_calls)

    ai_answer = generate_ai_final_answer(question, tool_results)

    if ai_answer:
        return ai_answer

    return generate_final_answer(question, tool_results)