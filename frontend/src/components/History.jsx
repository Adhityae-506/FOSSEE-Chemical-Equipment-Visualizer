import { useEffect, useState } from "react";
import { getHistory } from "../api/api";

export default function History() {
  const [history, setHistory] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchHistory() {
      try {
        const res = await getHistory();
        setHistory(res);
      } catch (err) {
        setError("Failed to fetch history");
      }
    }
    fetchHistory();
  }, []);

  if (error) return <p style={{ color: "red" }}>{error}</p>;

  return (
    <div>
      <h2>Upload History (Last 5)</h2>
      {history.length === 0 && <p>No uploads found.</p>}
      <ul>
        {history.map((item, idx) => (
          <li key={idx}>
            <strong>{item.file_name}</strong> – uploaded on 
            {new Date(item.upload_time).toLocaleString()}
          </li>
        ))}
      </ul>
    </div>
  );
}
