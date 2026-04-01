// frontend/src/components/StarRating.js
import React from "react";

export default function StarRating({ rating = 0, onChange }) {
  return (
    <div style={{ display: "flex", gap: "6px", cursor: "pointer" }}>
      {[1, 2, 3, 4, 5].map((n) => (
        <i
          key={n}
          className={`nes-icon is-small star ${
            n <= rating ? "" : "is-empty"
          }`}
          onClick={() => onChange(n)}
        ></i>
      ))}
    </div>
  );
}