import { useEffect, useState } from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from "recharts";

const API_BASE = "https://persistvision-ai-backend.onrender.com";

function LobGraph({ lob, period }) {
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!lob || !period) return;

    setLoading(true);
    setError(null);

    fetch(API_BASE + "/lob-graph?lob=" + encodeURIComponent(lob) + "&period=" + encodeURIComponent(period))
      .then((res) => res.json())
      .then((json) => {
        if (json.status === "success") {
          const formatted = json.data.map((d) => ({
            name: d.era.replace(/_/g, " ") + " - " + d.channel + " - " + d.pay_type,
            persistency: d.persistency
          }));
          setChartData(formatted);
        } else {
          setError(json.message);
        }
      })
      .catch(() => setError("Could not reach the backend."))
      .finally(() => setLoading(false));
  }, [lob, period]);

  if (loading) return <p>Loading graph...</p>;
  if (error) return <p style={{ color: "#c62828" }}>{error}</p>;
  if (!chartData) return null;

  const chartWidth = Math.max(chartData.length * 55, 600);

  return (
    <div style={{ marginTop: "20px" }}>
      <h4 style={{ color: "#10243E", fontFamily: "Fraunces, Georgia, serif", marginBottom: "10px" }}>
        Duration 1 Persistency by ERA / Channel / Pay Type
      </h4>
      <div style={{ width: "100%", overflowX: "auto" }}>
        <div style={{ width: chartWidth + "px", height: "420px" }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} margin={{ top: 20, right: 20, bottom: 110, left: 10 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#E1E3DE" />
              <XAxis dataKey="name" angle={-45} textAnchor="end" interval={0} height={110} tick={{ fontSize: 10, fill: "#4A5D78" }} />
              <YAxis tick={{ fontSize: 11, fill: "#4A5D78" }} label={{ value: "Persistency %", angle: -90, position: "insideLeft", fontSize: 11 }} />
              <Tooltip />
              <Bar dataKey="persistency" fill="#10243E" radius={[4, 4, 0, 0]}>
                {chartData.map((entry, index) => (
                  <Cell key={"cell-" + index} fill="#10243E" />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

export default LobGraph;
