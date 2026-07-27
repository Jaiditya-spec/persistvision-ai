import { useState } from "react";
import axios from "axios";
import "./App.css";
import Dashboard from "./components/Dashboard";

function App() {

  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  async function askAI() {

    if (!question.trim()) return;

    const currentQuestion = question;

    setMessages((prev) => [
      ...prev,
      {
        sender: "user",
        text: currentQuestion
      }
    ]);

    setQuestion("");
    setLoading(true);

    try {

      const response = await axios.post(
        "http://127.0.0.1:8000/ask",
        {
          question: currentQuestion
        }
      );

      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: response.data.answer
        }
      ]);

    }

    catch (error) {

      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: "❌ Unable to connect to the backend."
        }
      ]);

    }

    setLoading(false);

  }

  function handleKeyDown(e) {

    if (e.key === "Enter" && !e.shiftKey) {

      e.preventDefault();

      askAI();

    }

  }

  return (

    <div className="app">

      <div className="header">

        <h1>PersistVision AI</h1>

        <p>
          AI-Powered Insurance Persistency Analytics
        </p>

      </div>

      <Dashboard />

      <div className="chat-window">

        {messages.length === 0 && (

          <div className="message bot">

            <div className="bubble">

              <strong>Welcome to PersistVision AI 👋</strong>

              <br /><br />

              Try asking:

              <br /><br />

              • Overall persistency

              <br />

              • SWP persistency

              <br />

              • Compare SWP and SWAG

              <br />

              • Compare SAVINGS and PROTECTION

              <br />

              • Duration 2 persistency

            </div>

          </div>

        )}

        {messages.map((msg, index) => (

          <div
            key={index}
            className={`message ${msg.sender}`}
          >

            <div className="bubble">

              {msg.text}

            </div>

          </div>

        ))}

        {loading && (

          <div className="message bot">

            <div className="bubble">

              Thinking...

            </div>

          </div>

        )}

      </div>

      <div className="input-area">

        <textarea

          rows={3}

          value={question}

          onChange={(e) => setQuestion(e.target.value)}

          onKeyDown={handleKeyDown}

          placeholder="Ask PersistVision AI anything about your insurance data..."

        />

        <button

          onClick={askAI}

          disabled={loading}

        >

          {loading ? "Thinking..." : "Send"}

        </button>

      </div>

    </div>

  );

}

export default App;