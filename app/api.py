from fastapi import FastAPI
from app.agent import ask_agent

app = FastAPI(
    title="Insurance AI Agent",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Insurance AI Agent is running!"
    }


@app.get("/ask")
def ask(question: str):
    answer = ask_agent(question)
    return {
        "question": question,
        "answer": answer
    }