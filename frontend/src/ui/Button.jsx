
// import React from "react";
// import "./button.css";

// export default function Button({ children, onClick, type="primary", style }) {
//   return (
//     <button className={`btn btn-${type}`} onClick={onClick} style={style}>
//       {children}
//     </button>
//   );
// }
// src/ui/Button.jsx
import React from "react";
import "./button.css";

export default function Button({ children, onClick, type = "button", className = "", disabled }) {
  return (
    <button
      type={type}
      onClick={onClick}
      className={`ui-button ${className}`}
      disabled={disabled}
    >
      {children}
    </button>
  );
}
