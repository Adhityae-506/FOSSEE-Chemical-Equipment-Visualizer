import React, { useEffect, useState } from "react";
import { getHistory } from "../api/api";

export default function History() {
  const [items, setItems] = useState([]);
  useEffect(() => {
    getHistory()
      .then(setItems)
      .catch((err) => console.error(err));
  }, []);

  return (
    <div className="page">
      <div className="card">
        <h2>History (last 5 uploads)</h2>
        <ul>
          {items.map((i) => (
            <li key={i.upload_time}>
              <strong>{i.file_name}</strong> —{" "}
              {new Date(i.upload_time).toLocaleString()}
              <pre>{JSON.stringify(i.summary, null, 2)}</pre>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
