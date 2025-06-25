import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

const API = "http://127.0.0.1:5000"; 

function App() {
  const [interests, setInterests] = useState("");
  const [budget, setBudget] = useState("");
  const [selectedProducts, setSelectedProducts] = useState([]);
  const [recommendations, setRecommendations] = useState("");
  const [loading, setLoading] = useState(false);

  const productCatalog = [
    { id: "prod001", name: "Running Shoes", category: "Footwear", price: 1299 },
    { id: "prod002", name: "Wireless Earbuds", category: "Electronics", price: 1999 },
    { id: "prod003", name: "Graphic T-Shirt", category: "Clothing", price: 699 },
  ];

  const toggleProduct = (id) => {
    setSelectedProducts((prev) =>
      prev.includes(id) ? prev.filter((p) => p !== id) : [...prev, id]
    );
  };

  const handleSubmit = async () => {
    setLoading(true);
    try {
      await axios.post(`${API}/preferences`, {
        interests: interests.split(",").map((s) => s.trim()),
        budget: parseFloat(budget),
      });

      await axios.post(`${API}/history`, {
        product_ids: selectedProducts,
      });

      const res = await axios.get(`${API}/recommend`);
      setRecommendations(res.data.recommendations);
    } catch (err) {
      console.error(err);
      setRecommendations("Something went wrong.");
    }
    setLoading(false);
  };

  return (
    <div className="App">
      <h1>AI Product Recommender</h1>
      <input
        type="text"
        placeholder="Your interests (comma separated)"
        value={interests}
        onChange={(e) => setInterests(e.target.value)}
      />
      <input
        type="number"
        placeholder="Your budget (₹)"
        value={budget}
        onChange={(e) => setBudget(e.target.value)}
      />
      <div className="product-list">
        {productCatalog.map((p) => (
          <div
            key={p.id}
            className={`product ${selectedProducts.includes(p.id) ? "selected" : ""}`}
            onClick={() => toggleProduct(p.id)}
          >
            {p.name} – ₹{p.price} ({p.category})
          </div>
        ))}
      </div>
      <button onClick={handleSubmit} disabled={loading}>
        {loading ? "Getting Recommendations..." : "Get Recommendations"}
      </button>
      <pre className="recommendations">{recommendations}</pre>
    </div>
  );
}

export default App;
