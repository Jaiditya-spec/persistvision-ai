import { useState } from "react";
import axios from "axios";
import "./App.css";
import Dashboard from "./components/Dashboard";
import ExperienceAnalysis from "./components/ExperienceAnalysis";
import RedZone from "./components/RedZone";
import AssumptionSetting from "./components/AssumptionSetting";

function formatMessage(text) {
  const lines = text.split("\n");

  return lines.map((line, i) => {
    const tagMatch = line.match(/^\[(UP|DOWN|FLAT)\]\s*(.+)$/);

    if (tagMatch) {
      const [, tag, rest] = tagMatch;
      const badgeClass =
        tag === "UP" ? "change-up" : tag === "DOWN" ? "change-down" : "change-flat";

      return (
        <div key={i} className="stat-line">
          <span className="stat-label">{rest}</span>
          <span className={`change-badge ${badgeClass}`}>{tag}</span>
        </div>
      );
    }

    const statMatch = line.match(/^(.+?)\s*:\s*([\d.]+%)$/);

    if (statMatch) {
      const [, label, value] = statMatch;
      return (
        <div key={i} className="stat-line">
          <span className="stat-label">{label}</span>
          <span className="stat-value">{value}</span>
        </div>
      );
    }

    if (line.trim() === "") return null;

    return <div key={i}>{line}</div>;
  });
}

function App() {

  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  async function askAI() {

    if (!question.trim()) return;

    const currentQuestion = question;

    setMessages((prev) => [
      ...prev,
      { sender: "user", text: currentQuestion }
    ]);

    setQuestion("");
    setLoading(true);

    try {

      const response = await axios.post(
        "https://persistvision-ai-backend.onrender.com/ask",
        {
          question: currentQuestion,
          history: messages.slice(-8)
        }
      );

      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: response.data.answer }
      ]);

    }

    catch (error) {

      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "Unable to connect to the backend." }
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
        <div className="eyebrow">Actuarial Persistency Intelligence</div>
        <h1>PersistVision AI</h1>
        <p>AI-Powered Insurance Persistency Analytics</p>
      </div>

      <Dashboard />

      <div className="action-grid">
        <ExperienceAnalysis />
        <RedZone />
        <AssumptionSetting />
      </div>

      <div className="chat-window">

        {messages.length === 0 && (
          <div className="message bot">
            <div className="bubble">
              <strong>Welcome to PersistVision AI</strong>
              <p style={{ marginTop: "8px" }}>
                Every policy tells a story - persistency just tells you how it ends.
                Ask me anything about your book, and let's find out together.
              </p>
            </div>
          </div>
        )}

        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            <div className="bubble">
              {msg.sender === "bot" ? formatMessage(msg.text) : msg.text}
            </div>
          </div>
        ))}

        {loading && (
          <div className="message bot">
            <div className="bubble">Thinking...</div>
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
        <button onClick={askAI} disabled={loading}>
          {loading ? "Thinking..." : "Send"}
        </button>
      </div>

    </div>

  );

}

export default App;
