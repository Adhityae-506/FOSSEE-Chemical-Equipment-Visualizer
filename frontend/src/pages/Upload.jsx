// import React, { useState } from "react";
// import { uploadFile, getLatestSummary, downloadReportToBlob } from "../api/api";

// export default function Upload(){
//   const [file, setFile] = useState(null);
//   const [status, setStatus] = useState(null);
//   const [summary, setSummary] = useState(null);

//   const doUpload = async () => {
//     if (!file) return setStatus("Select a file first");
//     setStatus("Uploading...");
//     try {
//       const res = await uploadFile(file);
//       setStatus("Uploaded");
//       setSummary(res.summary || res);
//     } catch (err) {
//     const msg = err.response?.data?.detail || "Something went wrong while uploading.";
//     alert("❌ Upload failed\n\n" + msg);
// }

//   };

//   const downloadReport = async () => {
//     try {
//       const blob = await downloadReportToBlob();
//       const url = window.URL.createObjectURL(blob);
//       const a = document.createElement("a");
//       a.href = url;
//       a.download = "report.pdf";
//       document.body.appendChild(a);
//       a.click();
//       a.remove();
//       window.URL.revokeObjectURL(url);
//     } catch (e) {
//       alert("Download failed");
//     }
//   };

//   // return (
//   //   <div>
//   //     <h2>Upload CSV</h2>
//   //     <input type="file" accept=".csv" onChange={e => setFile(e.target.files[0])} />
//   //     <button onClick={doUpload}>Upload</button>
//   //     <button onClick={downloadReport}>Download Latest Report</button>
//   //     <div>{status}</div>
//   //     {summary && <pre>{JSON.stringify(summary, null, 2)}</pre>}
//   //   </div>
//   // );
//   return (
//   <div className="card">
//     <h2>Upload CSV File</h2>

//     <input
//       type="file"
//       accept=".csv"
//       onChange={e => setFile(e.target.files[0])}
//     />

//     <button onClick={doUpload}>Upload</button>
//     <button onClick={downloadReport}>Download Latest Report</button>

//     <div style={{ marginTop: 10 }}>{status}</div>

//     {summary && (
//       <pre>{JSON.stringify(summary, null, 2)}</pre>
//     )}
//   </div>
// );

// }
import React, { useState } from "react";
import { uploadFile, getLatestSummary, downloadReportToBlob } from "../api/api";

export default function Upload() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState(null);
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState(null); // <-- NEW

  const doUpload = async () => {
    if (!file) {
      setError("⚠️ Please select a CSV file before uploading.");
      return setStatus("Select a file first");
    }

    setStatus("Uploading...");
    setError(null);

    try {
      const res = await uploadFile(file);
      setStatus("Uploaded");
      setSummary(res.summary || res);
    } catch (err) {
      const msg =
        err.response?.data?.detail ||
        "Something went wrong while uploading. Try again!";

      setError(msg); // <-- NEW (replaces alert)
    }
  };

  const downloadReport = async () => {
  try {
    const blob = await downloadReportToBlob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = blob.filename;   // <-- USE BACKEND FILENAME
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
  } catch (e) {
    setError("Unable to download report.");
  }
};


  return (
    <div className="page">
      <div className="card">
        <h2>Upload CSV File</h2>

        <input
          type="file"
          accept=".csv"
          onChange={(e) => {
            setFile(e.target.files[0]);
            setError(null); // clear error when selecting new file
          }}
        />

        <div style={{ display: "flex", gap: "12px", marginTop: "12px" }}>
          <button onClick={doUpload}>Upload</button>
          <button onClick={downloadReport}>Download Latest Report</button>
        </div>

        <div style={{ marginTop: 10 }}>{status}</div>

        {/* 🔥 Inline Error Display (no popup) */}
        {error && (
          <div
            style={{
              marginTop: "12px",
              padding: "10px 14px",
              background: "#ffe6e6",
              color: "#cc0000",
              borderLeft: "5px solid #ff3333",
              borderRadius: "6px",
              fontSize: "15px",
            }}
          >
            {error}
          </div>
        )}

        {summary && <pre>{JSON.stringify(summary, null, 2)}</pre>}
      </div>
    </div>
  );
}
