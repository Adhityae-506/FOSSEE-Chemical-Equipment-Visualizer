// import React from "react";
// import { Link, useNavigate } from "react-router-dom";
// import { AuthContext } from "../contexts/AuthContext";

// export default function Navbar() {
//   const { token, logout } = React.useContext(AuthContext); 
//   const nav = useNavigate();

  
//   if (!token) return null;

//   return (
//     <nav className="navbar">
//       <div className="nav-container">

//         <div className="nav-left">Chemical Equipment Visualizer</div>

//         <div className="nav-right">
//           <Link to="/">Upload</Link>
//           <Link to="/summary">Summary</Link>
//           <Link to="/history">History</Link>
//           <Link to="/report">Report</Link>

//           <button
//             className="logout-btn"
//             onClick={() => {
//               logout();      
//               nav("/login"); 
//             }}
//           >
//             Logout
//           </button>
//         </div>

//       </div>
//     </nav>
//   );
// }

// import React from "react";
// import { Link, useNavigate } from "react-router-dom";
// import { AuthContext } from "../contexts/AuthContext";
// import "../components/Navbar.css";

// export default function Navbar() {
//   const { token, logout } = React.useContext(AuthContext);
//   const nav = useNavigate();

//   if (!token) return null;

//   return (
//     <nav className="navbar">
//       <div className="nav-container">

//         <div className="nav-left">Chemical Equipment Visualizer</div>

//         <div className="nav-right">
//           <Link to="/">Upload</Link>
//           <Link to="/summary">Summary</Link>
//           <Link to="/history">History</Link>
//           <Link to="/report">Report</Link>

//           <button
//             className="logout-btn"
//             onClick={() => {
//               logout();
//               nav("/login");
//             }}
//           >
//             Logout
//           </button>
//         </div>

//       </div>
//     </nav>
//   );
// }

// import React from "react";
// import { Link } from "react-router-dom";
// import "../components/Navbar.css";

// export default function Navbar() {
//   return (
//     <nav className="navbar">
//       <div className="nav-container">

//         <div className="nav-left">Chemical Equipment Visualizer</div>

//         <div className="nav-right">
//           <Link to="/">Upload</Link>
//           <Link to="/summary">Summary</Link>
//           <Link to="/history">History</Link>
//           <Link to="/report">Report</Link>
//         </div>

//       </div>
//     </nav>
//   );
// }

// src/components/Navbar.jsx
import React from "react";
import { Link } from "react-router-dom";
import "./Navbar.css";

export default function Navbar() {
  return (
    <nav className="navbar">
      <div className="nav-container">
        <div className="nav-left">Chemical Equipment Visualizer</div>
        <div className="nav-right">
          <Link to="/">Upload</Link>
          <Link to="/summary">Summary</Link>
          <Link to="/history">History</Link>
          <Link to="/report">Report</Link>
        </div>
      </div>
    </nav>
  );
}
