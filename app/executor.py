from app.tools import (
    overall_persistency,
    product_persistency,
    lob_persistency,
    duration_persistency
)

tool_functions = {

    "overall_persistency": overall_persistency,

    "product_persistency": product_persistency,

    "lob_persistency": lob_persistency,

    "duration_persistency": duration_persistency

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

            output = {

                "status": "error",

                "message": str(e)

            }

        results.append({

            "function": function_name,

            "arguments": arguments,

            "result": output

        })

    return results