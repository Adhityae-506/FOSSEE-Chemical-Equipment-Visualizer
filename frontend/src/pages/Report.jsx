// src/pages/Report.jsx
import React, { useState } from "react";
import { downloadReportToBlob } from "../api/api";

export default function Report() {
  const [status, setStatus] = useState(null);

  const handleDownload = async () => {
    setStatus("Preparing report...");
    try {
      const blob = await downloadReportToBlob();

      // Create a URL and trigger download
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = blob.filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);

      setStatus("Report downloaded successfully ✅");
    } catch (err) {
      console.error(err);
      setStatus("Failed to download report ❌");
    }
  };

  return (
    <div className="page">
      <div className="card">
        <h2 style={{ color: "#0B5394" }}>Download Latest Report</h2>
        <p>
          Click the button below to generate and download the latest equipment
          summary report as a PDF.
        </p>
        <button
          onClick={handleDownload}
          style={{
            padding: "10px 16px",
            backgroundColor: "#0B5394",
            color: "white",
            border: "none",
            borderRadius: "5px",
            cursor: "pointer",
          }}
        >
          Download Report
        </button>

        {status && (
          <p style={{ marginTop: "12px", fontStyle: "italic", color: "#555" }}>
            {status}
          </p>
        )}
      </div>
    </div>
  );
}
