from app.router import route_question

questions = [

    "Overall persistency",

    "SWP persistency",

    "Compare SWP and SWAG",

    "Compare SAVINGS and PROTECTION",

    "Duration 2 persistency"

]

for q in questions:

    print("\n=====================")

    print(q)

    print(route_question(q))