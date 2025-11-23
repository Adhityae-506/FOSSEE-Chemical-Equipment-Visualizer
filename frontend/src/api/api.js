const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

async function request(
  path,
  { method = "GET", headers = {}, body = null, asForm = false } = {}
) {
  const url = `${API_BASE}${path}`;
  const opts = { method, headers: { ...headers } };

  if (asForm) {
    opts.body = body;
  } else if (body !== null) {
    opts.headers["Content-Type"] = "application/json";
    opts.body = JSON.stringify(body);
  }

  const res = await fetch(url, opts);
  const text = await res.text();

  let data;
  try {
    data = JSON.parse(text);
  } catch {
    data = text;
  }

  if (!res.ok) {
    const err = new Error("API error");
    err.status = res.status;
    err.payload = data;
    throw err;
  }
  return data;
}


export async function uploadFile(file) {
  const fd = new FormData();
  fd.append("file", file);
  return request("/api/datasets/upload/", {
    method: "POST",
    asForm: true,
    body: fd,
  });
}

export async function getHistory() {
  return request("/api/datasets/history/");
}

export async function getLatestSummary() {
  return request("/api/datasets/latest/");
}

import axios from "axios";  

export async function downloadReportToBlob() {
  const res = await axios.get(`${API_BASE}/api/datasets/latest/report/`, {
    responseType: "blob",
  });

  
  const disposition = res.headers["content-disposition"];
  let filename = "report.pdf";

  if (disposition && disposition.includes("filename=")) {
    filename = disposition.split("filename=")[1].replace(/"/g, "");
  }

  
  const blob = new Blob([res.data], { type: "application/pdf" });
  blob.filename = filename;

  return blob;
}

