import { useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();

  return (
    <div
      style={{
        height: "100vh",
        backgroundColor: "#0B0B0B",
        color: "#FFD700",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        textAlign: "center",
      }}
    >
      <h1 style={{ fontSize: "40px", marginBottom: "10px" }}>
        🚚 Supply Chain Delay Prediction
      </h1>

      <p style={{ maxWidth: "500px", color: "#aaa" }}>
        AI-powered system to predict shipment delays and improve logistics decisions.
      </p>

      <button
        onClick={() => navigate("/predict")}
        style={{
          marginTop: "20px",
          padding: "12px 24px",
          backgroundColor: "#FFD700",
          color: "#000",
          border: "none",
          borderRadius: "8px",
          cursor: "pointer",
          fontWeight: "bold",
        }}
      >
        🚀 Start Prediction
      </button>
    </div>
  );
}