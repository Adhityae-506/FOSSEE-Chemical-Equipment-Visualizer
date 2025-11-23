// import React from "react";
// import "./App.css";
// import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
// import { AuthProvider, AuthContext } from "./contexts/AuthContext";
// import Login from "./pages/Login";
// import Upload from "./pages/Upload";
// import LatestSummary from "./pages/LatestSummary";
// import History from "./pages/History";
// import Report from "./pages/Report";
// import Navbar from "./components/Navbar";
// function ProtectedRoute({ children }) {
//   const { token } = React.useContext(AuthContext);
//   if (!token) return <Navigate to="/login" replace />;
//   return children;
// }

// export default function App() {
//   return (
//     <AuthProvider>
//       <BrowserRouter>
//         <Navbar />
//         <Routes>
//           <Route path="/login" element={<Login />} />
//           <Route
//             path="/"
//             element={
//               <ProtectedRoute>
//                 <Upload />
//               </ProtectedRoute>
//             }
//           />
//           <Route
//             path="/summary"
//             element={
//               <ProtectedRoute>
//                 <LatestSummary />
//               </ProtectedRoute>
//             }
//           />
//           <Route
//             path="/history"
//             element={
//               <ProtectedRoute>
//                 <History />
//               </ProtectedRoute>
//             }
//           />
//           <Route
//             path="/report"
//             element={
//               <ProtectedRoute>
//                 <Report />
//               </ProtectedRoute>
//             }
//           />{" "}
//           {/* ✅ Added Report route */}
//         </Routes>
//       </BrowserRouter>
//     </AuthProvider>
//   );
// }
// import React from "react";
// import "./App.css";
// import { BrowserRouter, Routes, Route } from "react-router-dom";

// import Upload from "./pages/Upload";
// import LatestSummary from "./pages/LatestSummary";
// import History from "./pages/History";
// import Report from "./pages/Report";
// import Navbar from "./components/Navbar";

// export default function App() {
//   return (
//     <BrowserRouter>
//       <Navbar />

//       <Routes>
//         <Route path="/" element={<Upload />} />
//         <Route path="/summary" element={<LatestSummary />} />
//         <Route path="/history" element={<History />} />
//         <Route path="/report" element={<Report />} />
//       </Routes>
//     </BrowserRouter>
//   );
// }
// src/App.jsx
import React from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Upload from "./pages/Upload";
import LatestSummary from "./pages/LatestSummary";
import History from "./pages/History";
import Report from "./pages/Report";
import Navbar from "./components/Navbar";

export default function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<Upload />} />
        <Route path="/summary" element={<LatestSummary />} />
        <Route path="/history" element={<History />} />
        <Route path="/report" element={<Report />} />
      </Routes>
    </BrowserRouter>
  );
}
