from app.tools import (
    overall_persistency,
    product_persistency,
    lob_persistency,
    duration_persistency,
    experience_analysis,
    filtered_persistency
)
from app.assumption_setting import run_assumption_setting
from app.red_zone import identify_red_zone, red_zone_product_breakdown

tool_functions = {
    "overall_persistency": overall_persistency,
    "product_persistency": product_persistency,
    "lob_persistency": lob_persistency,
    "duration_persistency": duration_persistency,
    "experience_analysis": experience_analysis,
    "filtered_persistency": filtered_persistency,
    "run_assumption_setting": run_assumption_setting,
    "identify_red_zone": identify_red_zone,
    "red_zone_product_breakdown": red_zone_product_breakdown
}


def execute_function_calls(function_calls):

    results = []

    for call in function_calls:

        function_name = call["function_name"]
        arguments = call["arguments"]

        print("\n----------------------------")
        print("Executing :", function_name)
        print("Arguments :", arguments)

        try:
            output = tool_functions[function_name](**arguments)
        except Exception as e:
            output = {"status": "error", "message": str(e)}

        results.append({
            "function": function_name,
            "arguments": arguments,
            "result": output
        })

    return results