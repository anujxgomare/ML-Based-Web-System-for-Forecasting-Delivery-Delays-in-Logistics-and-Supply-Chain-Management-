import { useState } from "react";
import axios from "axios";

function Predict() {
  const [result, setResult] = useState(null);

  const handleSubmit = async () => {
    const res = await axios.post("http://127.0.0.1:8000/predict", {
      distance: 120,
      carrier: "DHL",
      weather: "Rainy"
    });

    setResult(res.data);
  };

  return (
    <div style={{ background: "#0B0B0B", color: "#FFD700", height: "100vh", textAlign: "center", paddingTop: "50px" }}>
      <h2>Prediction Page</h2>

      <button onClick={handleSubmit}>
        Predict
      </button>

      {result && (
        <div>
          <p>{result.prediction === 1 ? "Delay" : "On Time"}</p>
          <p>{(result.probability * 100).toFixed(2)}%</p>
        </div>
      )}
    </div>
  );
}

export default Predict;