from app.agent import ask_agent

questions = [

    "Overall persistency",

    "SWP persistency",

    "Compare SWP and SWAG",

    "Compare SAVINGS and PROTECTION",

    "Duration 2 persistency"

]

for q in questions:

    print("\n===================================")

    print("USER:", q)

    print()

    print(ask_agent(q))