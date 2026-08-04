import { useState, useEffect } from "react";
import LobGraph from "./LobGraph";

const API_BASE = "https://persistvision-ai-backend.onrender.com";

function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [openLob, setOpenLob] = useState(null);
  const [breakdown, setBreakdown] = useState(null);
  const [loadingBreakdown, setLoadingBreakdown] = useState(false);

  useEffect(() => {
    fetch(`${API_BASE}/dashboard-summary`)
      .then((res) => res.json())
      .then((data) => setSummary(data))
      .catch(() => setSummary({ status: "error" }));
  }, []);

  function toggleLob(lob) {
    setBreakdown(null);
    setOpenLob(openLob === lob ? null : lob);
  }

  async function loadBreakdown(lob, period) {
    setLoadingBreakdown(true);
    try {
      const res = await fetch(`${API_BASE}/lob-products?lob=${lob}&period=${period}`);
      const data = await res.json();
      setBreakdown(data);
    } catch (err) {
      setBreakdown({ status: "error", message: "Could not reach the backend." });
    }
    setLoadingBreakdown(false);
  }

  const cards = [
    {
      title: "Overall Persistency",
      value: summary ? `${summary.overall_persistency}%` : "...",
      clickable: false,
      className: "card"
    },
    {
      title: "Savings",
      value: summary ? `${summary.savings_persistency}%` : "...",
      clickable: true,
      lob: "SAVINGS",
      className: "card card-savings"
    },
    {
      title: "Protection",
      value: summary ? `${summary.protection_persistency}%` : "...",
      clickable: true,
      lob: "PROTECTION",
      className: "card card-protection"
    }
  ];

  return (
    <div className="dashboard">
      {cards.map((card, index) => (
        <div key={index}>
          <div
            className={card.className}
            onClick={() => card.clickable && toggleLob(card.lob)}
            style={{ cursor: card.clickable ? "pointer" : "default" }}
          >
            <h3>{card.title}</h3>
            <h1>{card.value}</h1>
          </div>

          {card.clickable && openLob === card.lob && (
            <div className="period-picker">
              <p>Choose a period:</p>
              <button className="period-btn" onClick={() => loadBreakdown(card.lob, "oct_25")}>
                YTD Oct'25
              </button>
              <button className="period-btn" onClick={() => loadBreakdown(card.lob, "jun_26")}>
                YTD Jun'26
              </button>
            </div>
          )}
        </div>
      ))}

      {loadingBreakdown && (
        <p style={{ gridColumn: "1 / -1" }}>Loading product breakdown...</p>
      )}

      {breakdown && breakdown.status === "success" && (
        <div className="analysis-section" style={{ gridColumn: "1 / -1", margin: "10px 0 0 0" }}>
          <h3>
            {breakdown.line_of_business} - {breakdown.period === "oct_25" ? "YTD Oct'25" : "YTD Jun'26"}
          </h3>
          <p style={{ color: "#4A5D78", marginBottom: "10px", fontFamily: "Inter, sans-serif" }}>
            LOB Persistency:{" "}
            <strong style={{ color: "#10243E", fontFamily: "JetBrains Mono, monospace" }}>
              {breakdown.lob_persistency}%
            </strong>
          </p>
          <table className="styled-table">
            <thead>
              <tr>
                <th>Product</th>
                <th>Persistency</th>
              </tr>
            </thead>
            <tbody>
              {breakdown.products.map((p, i) => (
                <tr key={i}>
                  <td>{p.product}</td>
                  <td>{p.persistency}%</td>
                </tr>
              ))}
            </tbody>
          </table>

          <LobGraph lob={breakdown.line_of_business} period={breakdown.period} />
        </div>
      )}

      {breakdown && breakdown.status === "error" && (
        <p style={{ color: "#A93A2C", gridColumn: "1 / -1" }}>{breakdown.message}</p>
      )}
    </div>
  );
}

export default Dashboard;
