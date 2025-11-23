// src/ui/Card.jsx
import React from "react";
import "./card.css";

export default function Card({ children, style }) {
  return (
    <div className="ui-card" style={style}>
      {children}
    </div>
  );
}
