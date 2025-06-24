import { useState } from "react";
import axios from "axios";

function App() {
  const [interests, setInterests] = useState("");
  const [budget, setBudget] = useState("");
  const [recommendations, setRecommendations] = useState("");

  const getRecommendations = async () => {
    const res = await axios.post("http://127.0.0.1:8000/recommend", {
      interests: interests.split(","),
      budget: parseFloat(budget)
    });
    setRecommendations(res.data.recommendations);
  };

  return (
    <div style={{ padding: 20, maxWidth: 600, margin: "auto" }}>
      <h1>Product Recommender</h1>
      <input
        value={interests}
        onChange={(e) => setInterests(e.target.value)}
        placeholder="Enter interests (e.g., sport, tech)"
        style={{ display: "block", marginBottom: 10, width: "100%" }}
      />
      <input
        value={budget}
        onChange={(e) => setBudget(e.target.value)}
        placeholder="Enter budget"
        type="number"
        style={{ display: "block", marginBottom: 10, width: "100%" }}
      />
      <button onClick={getRecommendations}>Get Recommendations</button>

      {recommendations && (
        <pre style={{ marginTop: 20, background: "#f4f4f4", padding: 10 }}>
          {recommendations}
        </pre>
      )}
    </div>
  );
}

export default App;
