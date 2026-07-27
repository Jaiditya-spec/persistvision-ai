import re

from app.data import df


# -----------------------------
# Load valid values from dataset
# -----------------------------

VALID_PRODUCTS = sorted(
    df["Product_Name"].dropna().str.upper().unique().tolist()
)

VALID_LOBS = sorted(
    df["Line_of_business"].dropna().str.upper().unique().tolist()
)

VALID_DURATIONS = sorted(
    df["Duration"].dropna().unique().tolist()
)


# -----------------------------
# Detect Intent
# -----------------------------

def detect_intent(question):

    q = question.upper()

    # Overall
    if "OVERALL" in q:
        return "overall"

    # Compare
    if "COMPARE" in q:
        return "compare"

    # Duration
    if any(str(d) in q for d in VALID_DURATIONS):
        return "duration"

    # Product
    if any(product in q for product in VALID_PRODUCTS):
        return "product"

    # Line of Business
    if any(lob in q for lob in VALID_LOBS):
        return "lob"

    return "unknown"


def extract_entities(question):

    q = question.upper()

    products = []

    lobs = []

    durations = []


    # Products

    for product in VALID_PRODUCTS:

        if product in q:

            products.append(product)


    # LOBs

    for lob in VALID_LOBS:

        if lob in q:

            lobs.append(lob)


    # Duration

    matches = re.findall(r"\d+", q)

    for m in matches:

        durations.append(int(m))


    return {

        "products": products,

        "lobs": lobs,

        "durations": durations

    }


def route_question(question):

    intent = detect_intent(question)

    entities = extract_entities(question)

    function_calls = []


    if intent == "overall":

        function_calls.append({

            "function_name": "overall_persistency",

            "arguments": {}

        })


    elif intent == "product":

        for p in entities["products"]:

            function_calls.append({

                "function_name": "product_persistency",

                "arguments": {

                    "product_name": p

                }

            })


    elif intent == "lob":

        for lob in entities["lobs"]:

            function_calls.append({

                "function_name": "lob_persistency",

                "arguments": {

                    "lob_name": lob

                }

            })


    elif intent == "duration":

        for d in entities["durations"]:

            function_calls.append({

                "function_name": "duration_persistency",

                "arguments": {

                    "duration": d

                }

            })


    elif intent == "compare":

        for p in entities["products"]:

            function_calls.append({

                "function_name": "product_persistency",

                "arguments": {

                    "product_name": p

                }

            })


        for lob in entities["lobs"]:

            function_calls.append({

                "function_name": "lob_persistency",

                "arguments": {

                    "lob_name": lob

                }

            })


    return function_calls