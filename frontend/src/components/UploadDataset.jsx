import { useState } from "react";
import { uploadFile } from "../api/api";

export default function UploadDataset() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");
    setError("");

    if (!file) {
      setError("Please select a CSV file to upload.");
      return;
    }

    try {
      const res = await uploadFile(file);
      setMessage(`✅ ${res.message}`);
    } catch (err) {
      setError(err.payload?.detail || "Upload failed. Please try again.");
    }
  };

  return (
    <div className="upload-container">
      <h2>Upload Dataset</h2>
      <form onSubmit={handleSubmit}>
        <input type="file" accept=".csv" onChange={(e) => setFile(e.target.files[0])} />
        <button type="submit">Upload</button>
      </form>
      {message && <p style={{ color: "green" }}>{message}</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}
