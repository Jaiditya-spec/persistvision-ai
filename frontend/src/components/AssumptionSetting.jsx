import { useState } from "react";

const API_BASE = "https://persistvision-ai-backend.onrender.com";

function AssumptionSetting() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function runAssumptionSetting() {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(API_BASE + "/assumption-setting/run", { method: "POST" });
      const json = await res.json();
      setData(json);
    } catch (err) {
      setError("Could not reach the backend. Is the server running?");
    }
    setLoading(false);
  }

  return (
    <div className="analysis-section accent-gold">
      <h3>Assumption Setting</h3>

      <button className="run-button" onClick={runAssumptionSetting} disabled={loading}>
        {loading ? "Running..." : "Run Assumption Setting"}
      </button>

      {error && <p style={{ color: "#c62828", marginTop: "10px" }}>{error}</p>}

      {data && data.status === "success" && (
        <div>
          <p style={{ color: "#4A5D78", margin: "12px 0" }}>
            {data.cohorts_updated} cohorts updated - {data.improved} improved, {data.declined} declined, {data.unchanged} unchanged.
          </p>

          <div style={{ display: "flex", gap: "10px", marginBottom: "16px", flexWrap: "wrap" }}>
            <a href={API_BASE + "/assumption-setting/download/" + data.summary_file} className="run-button" style={{ textDecoration: "none" }}>Download Assumption Summary</a>
            <a href={API_BASE + "/assumption-setting/download/" + data.prophet_file} className="period-btn" style={{ textDecoration: "none", display: "inline-flex", alignItems: "center" }}>Download Prophet Table</a>
            <a href={API_BASE + "/assumption-setting/download/" + data.word_file} className="period-btn" style={{ textDecoration: "none", display: "inline-flex", alignItems: "center" }}>Download Word Report</a>
          </div>

          <table className="styled-table">
            <thead>
              <tr>
                <th>ERA</th>
                <th>Channel</th>
                <th>Pay Type</th>
                <th>Prior (Dur 1)</th>
                <th>Proposed (Dur 1)</th>
                <th>Ultimate</th>
                <th>Change</th>
              </tr>
            </thead>
            <tbody>
              {data.prophet_updates.map((row, i) => (
                <tr key={i} className={"zone-" + row.zone}>
                  <td>{row.era}</td>
                  <td>{row.channel}</td>
                  <td>{row.pay_type}</td>
                  <td>{(row.prior_assumption_duration1 * 100).toFixed(2)}%</td>
                  <td>{(row.proposed_assumption_duration1 * 100).toFixed(2)}%</td>
                  <td>{(row.proposed_assumption_ultimate * 100).toFixed(2)}%</td>
                  <td>
                    <span className={"change-badge " + (row.movement > 0 ? "change-up" : row.movement < 0 ? "change-down" : "change-flat")}>
                      {row.movement > 0 ? "UP" : row.movement < 0 ? "DOWN" : "FLAT"} {(row.movement * 100).toFixed(2)}%
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default AssumptionSetting;
