import { useState } from "react";

function ExperienceAnalysis() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function runAnalysis() {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("https://persistvision-ai-backend.onrender.com/experience-analysis");
      const json = await res.json();
      setData(json.results);
    } catch (err) {
      setError("Could not reach the backend. Is the server running?");
    }
    setLoading(false);
  }

  return (
    <div className="analysis-section accent-teal">
      <h3>Experience Analysis</h3>

      <button className="run-button" onClick={runAnalysis} disabled={loading}>
        {loading ? "Analysing..." : "Run Experience Analysis"}
      </button>

      {error && <p style={{ color: "#c62828", marginTop: "10px" }}>{error}</p>}

      {data && (
        <table className="styled-table">
          <thead>
            <tr>
              <th>ERA</th>
              <th>Channel</th>
              <th>Pay Type</th>
              <th>Oct 25 %</th>
              <th>Jun 26 %</th>
              <th>Change</th>
            </tr>
          </thead>
          <tbody>
            {data.map((row, i) => (
              <tr key={i} className={`zone-${row.zone}`}>
                <td>{row.era}</td>
                <td>{row.channel}</td>
                <td>{row.pay_type}</td>
                <td>{row.persistency_period1}%</td>
                <td>{row.persistency_period2}%</td>
                <td>
                  <span
                    className={`change-badge ${
                      row.change > 0 ? "change-up" : row.change < 0 ? "change-down" : "change-flat"
                    }`}
                  >
                    {row.change > 0 ? "▲" : row.change < 0 ? "▼" : "–"} {row.change}%
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default ExperienceAnalysis;
