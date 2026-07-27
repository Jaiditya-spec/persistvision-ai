from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.agent import ask_agent

app = FastAPI(
    title="Insurance AI Agent",
    version="1.0"
)

# Allow React frontend to access this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Question(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "Insurance AI Agent API is running."
    }


@app.post("/ask")
def ask(data: Question):

    answer = ask_agent(data.question)

    return {
        "answer": answer
    }