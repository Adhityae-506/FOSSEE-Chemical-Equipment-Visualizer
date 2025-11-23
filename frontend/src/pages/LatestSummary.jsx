import React, { useEffect, useState } from "react";
import { getLatestSummary } from "../api/api";
import ChartPie from "../components/ChartPie";
import ChartLine from "../components/ChartLine";

export default function LatestSummary() {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getLatestSummary()
      .then((data) => {
        console.log("✅ SUMMARY DATA RECEIVED:", data); // Debug log
        setSummary(data);
        setLoading(false);
      })
      .catch(() => {
        alert("Unable to fetch latest summary. Please upload a dataset first.");
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading...</p>;
  if (!summary) return <p>No summary available</p>;

  // return (
  //   <div style={{ padding: "20px" }}>
  //     <h2 style={{ color: "#0B5394" }}>Latest Dataset Summary</h2>
  //     <p><strong>Total Equipment:</strong> {summary.total_equipment}</p>
  //     <p><strong>Average Flowrate:</strong> {summary.average_flowrate}</p>
  //     <p><strong>Average Pressure:</strong> {summary.average_pressure}</p>
  //     <p><strong>Average Temperature:</strong> {summary.average_temperature}</p>

  //     <div style={{ display: "flex", flexWrap: "wrap", gap: "40px" }}>
  //       <ChartLine summary={summary} />
  //       <ChartPie data={summary.type_distribution} />
  //     </div>
  //   </div>
  // );

  return (
    <div className="page">
      <div className="card">
        <h2>Latest Dataset Summary</h2>

        <p>
          <strong>Total Equipment:</strong> {summary.total_equipment}
        </p>
        <p>
          <strong>Average Flowrate:</strong> {summary.average_flowrate}
        </p>
        <p>
          <strong>Average Pressure:</strong> {summary.average_pressure}
        </p>
        <p>
          <strong>Average Temperature:</strong> {summary.average_temperature}
        </p>

        <div
          style={{
            display: "flex",
            flexWrap: "wrap",
            gap: "40px",
            marginTop: "20px",
          }}
        >
          <div className="chart-wrapper">
            <ChartLine summary={summary} />
          </div>
          <div className="chart-wrapper">
            <ChartPie data={summary.type_distribution} />
          </div>
        </div>
      </div>
    </div>
  );
}
