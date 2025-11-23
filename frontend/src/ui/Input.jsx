// // src/ui/Input.jsx
// import React from "react";
// import "./input.css";

// export default function Input({ type="text", placeholder, onChange, value }) {
//   return (
//     <input
//       className="ui-input"
//       type={type}
//       placeholder={placeholder}
//       onChange={onChange}
//       value={value}
//     />
//   );
// }
// src/ui/Input.jsx
import React from "react";
import "./input.css";

export default function Input({ icon: Icon, type = "text", placeholder, value, onChange, name }) {
  return (
    <div className="ui-input-wrap">
      {Icon && <div className="ui-input-icon"><Icon /></div>}
      <input
        className="ui-input"
        type={type}
        placeholder={placeholder}
        value={value}
        name={name}
        onChange={onChange}
        autoComplete="off"
      />
    </div>
  );
}
