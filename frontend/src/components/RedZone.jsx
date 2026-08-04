import { useState } from "react";

const API_BASE = "https://persistvision-ai-backend.onrender.com";

function RedZone() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [openKey, setOpenKey] = useState(null);
  const [breakdown, setBreakdown] = useState(null);
  const [loadingBreakdown, setLoadingBreakdown] = useState(false);
  const [filter, setFilter] = useState("all");

  async function runRedZone() {
    setLoading(true);
    setError(null);
    setBreakdown(null);
    setOpenKey(null);
    setFilter("all");
    try {
      const res = await fetch(API_BASE + "/red-zone");
      const json = await res.json();
      setData(json);
    } catch (err) {
      setError("Could not reach the backend. Is the server running?");
    }
    setLoading(false);
  }

  async function drillDown(row) {
    const key = row.era + "|" + row.channel + "|" + row.pay_type;

    if (openKey === key) {
      setOpenKey(null);
      setBreakdown(null);
      return;
    }

    setOpenKey(key);
    setLoadingBreakdown(true);
    try {
      const url = API_BASE + "/red-zone/products?era=" + encodeURIComponent(row.era) +
        "&channel=" + encodeURIComponent(row.channel) +
        "&pay_type=" + encodeURIComponent(row.pay_type);
      const res = await fetch(url);
      const json = await res.json();
      setBreakdown(json);
    } catch (err) {
      setBreakdown({ status: "error", message: "Could not reach the backend." });
    }
    setLoadingBreakdown(false);
  }

  function cohortDownloadUrl(row) {
    return API_BASE + "/red-zone/download-cohort?era=" + encodeURIComponent(row.era) +
      "&channel=" + encodeURIComponent(row.channel) +
      "&pay_type=" + encodeURIComponent(row.pay_type);
  }

  const filteredResults = data && data.results
    ? data.results.filter((r) => filter === "all" || r.zone === filter)
    : [];

  return (
    <div className="analysis-section accent-red">
      <h3>Identify Red/Green Zone</h3>

      <button className="run-button" onClick={runRedZone} disabled={loading}>
        {loading ? "Checking..." : "Identify Red/Green Zone"}
      </button>

      {error && <p style={{ color: "#c62828", marginTop: "10px" }}>{error}</p>}

      {data && data.status === "success" && (
        <div>
          <p style={{ color: "#4A5D78", margin: "12px 0" }}>
            {data.flagged_count === 0
              ? "No cohorts are out of line with assumptions by more than 2 points at Duration 1."
              : data.flagged_count + " cohort(s) flagged, out by more than " + (data.threshold * 100).toFixed(0) + " points at Duration 1."}
          </p>

          <a href={API_BASE + "/assumption-setting/download/" + data.prophet_file} className="run-button" style={{ textDecoration: "none", display: "inline-block", marginBottom: "14px" }}>Download Prophet Table (All Flagged Cohorts)</a>

          {data.results.length > 0 && (
            <div style={{ display: "flex", gap: "8px", marginBottom: "14px", flexWrap: "wrap" }}>
              <button className="period-btn" style={filter === "all" ? { background: "#10243E", color: "white" } : {}} onClick={() => setFilter("all")}>All ({data.results.length})</button>
              <button className="period-btn" style={filter === "red" ? { background: "#A93A2C", color: "white", borderColor: "#A93A2C" } : { borderColor: "#A93A2C", color: "#A93A2C" }} onClick={() => setFilter("red")}>Red Zone ({data.results.filter((r) => r.zone === "red").length})</button>
              <button className="period-btn" style={filter === "green" ? { background: "#1F7A4D", color: "white", borderColor: "#1F7A4D" } : { borderColor: "#1F7A4D", color: "#1F7A4D" }} onClick={() => setFilter("green")}>Green Zone ({data.results.filter((r) => r.zone === "green").length})</button>
            </div>
          )}

          {filteredResults.length === 0 && data.results.length > 0 && (
            <p style={{ color: "#4A5D78" }}>No cohorts match this filter.</p>
          )}

          {filteredResults.length > 0 && (
            <table className="styled-table">
              <thead>
                <tr>
                  <th>ERA</th>
                  <th>Channel</th>
                  <th>Pay Type</th>
                  <th>Latest Actual</th>
                  <th>Proposed</th>
                  <th>Deviation</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredResults.map((r, i) => {
                  const key = r.era + "|" + r.channel + "|" + r.pay_type;
                  return (
                    <>
                      <tr key={i} className={"zone-" + r.zone}>
                        <td>{r.era}</td>
                        <td>{r.channel}</td>
                        <td>{r.pay_type}</td>
                        <td>{(r.latest_actual * 100).toFixed(2)}%</td>
                        <td>{(r.proposed_assumption * 100).toFixed(2)}%</td>
                        <td>
                          <span className={"change-badge " + (r.deviation > 0 ? "change-up" : "change-down")}>
                            {r.deviation > 0 ? "+" : ""}{(r.deviation * 100).toFixed(2)} pts
                          </span>
                        </td>
                        <td style={{ whiteSpace: "nowrap" }}>
                          <button className="period-btn" style={{ marginRight: "6px" }} onClick={() => drillDown(r)}>{openKey === key ? "Hide" : "Drill Down"}</button>
                          <a href={cohortDownloadUrl(r)} className="period-btn" style={{ textDecoration: "none", display: "inline-block" }}>Download Prophet</a>
                        </td>
                      </tr>
                      {openKey === key && (
                        <tr>
                          <td colSpan="7" style={{ background: "#FAFAF8" }}>
                            {loadingBreakdown && <p>Loading product breakdown...</p>}
                            {breakdown && breakdown.status === "success" && (
                              <table className="styled-table" style={{ margin: "8px 0" }}>
                                <thead>
                                  <tr>
                                    <th>Product</th>
                                    <th>Previous Period</th>
                                    <th>Latest Period</th>
                                    <th>Change</th>
                                  </tr>
                                </thead>
                                <tbody>
                                  {breakdown.products.map((p, k) => (
                                    <tr key={k}>
                                      <td>{p.product}</td>
                                      <td>{p.previous_persistency !== null ? p.previous_persistency + "%" : "N/A"}</td>
                                      <td>{p.latest_persistency !== null ? p.latest_persistency + "%" : "N/A"}</td>
                                      <td>
                                        {p.change !== null && (
                                          <span className={"change-badge " + (p.change > 0 ? "change-up" : p.change < 0 ? "change-down" : "change-flat")}>
                                            {p.change > 0 ? "+" : ""}{p.change}%
                                          </span>
                                        )}
                                      </td>
                                    </tr>
                                  ))}
                                </tbody>
                              </table>
                            )}
                            {breakdown && breakdown.status === "error" && (
                              <p style={{ color: "#c62828" }}>{breakdown.message}</p>
                            )}
                          </td>
                        </tr>
                      )}
                    </>
                  );
                })}
              </tbody>
            </table>
          )}
        </div>
      )}
    </div>
  );
}

export default RedZone;
