// // src/api/api.js
// const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

// export function getToken() {
//   return localStorage.getItem("token");
// }
// export function setToken(token) {
//   localStorage.setItem("token", token);
// }
// export function clearToken() {
//   localStorage.removeItem("token");
// }

// async function request(path, { method="GET", headers={}, body=null, asForm=false } = {}) {
//   const token = getToken();
//   const url = `${API_BASE}${path}`;
//   const opts = { method, headers: { ...headers } };
//   if (token) opts.headers["Authorization"] = `Token ${token}`;
//   if (asForm) {
//     // body is FormData (for file upload); do not set Content-Type manually
//     opts.body = body;
//   } else if (body !== null) {
//     opts.headers["Content-Type"] = "application/json";
//     opts.body = JSON.stringify(body);
//   }
//   const res = await fetch(url, opts);
//   const text = await res.text();
//   // Try parse JSON, fallback to text
//   let data = null;
//   try { data = JSON.parse(text); } catch(e) { data = text; }
//   if (!res.ok) {
//     // throw an object with both raw and parsed content
//     const err = new Error("API error");
//     err.status = res.status;
//     err.payload = data;
//     throw err;
//   }
//   return data;
// }

// export async function login(username, password) {
//   return request("/api/auth/login/", { method: "POST", body: { username, password }});
// }

// export async function uploadFile(file) {
//   const fd = new FormData();
//   fd.append("file", file);
//   return request("/api/datasets/upload/", { method: "POST", asForm: true, body: fd });
// }

// export async function getHistory() {
//   return request("/api/datasets/history/");
// }

// export async function getLatestSummary() {
//   return request("/api/datasets/latest/");
// }

// export async function downloadReportToBlob() {
//   const token = getToken();
//   const headers = token ? { Authorization: `Token ${token}` } : {};
//   const res = await fetch(`${API_BASE}/api/datasets/latest/report/`, { headers });
//   if (!res.ok) throw new Error("Report download failed");
//   const blob = await res.blob();
//   return blob;
// }

// src/api/api.js
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

// export async function downloadReportToBlob() {
//   const res = await fetch(`${API_BASE}/api/datasets/latest/report/`);
//   if (!res.ok) throw new Error("Report download failed");
//   return await res.blob();
// }
import axios from "axios";  // ensure axios is imported

export async function downloadReportToBlob() {
  const res = await axios.get(`${API_BASE}/api/datasets/latest/report/`, {
    responseType: "blob",
  });

  // Extract filename from Content-Disposition
  const disposition = res.headers["content-disposition"];
  let filename = "report.pdf";

  if (disposition && disposition.includes("filename=")) {
    filename = disposition.split("filename=")[1].replace(/"/g, "");
  }

  // Store filename inside blob for frontend use
  const blob = new Blob([res.data], { type: "application/pdf" });
  blob.filename = filename;

  return blob;
}

