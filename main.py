from flask import Flask, request, jsonify
from flask_cors import CORS
from together import Together
import json

app = Flask(__name__)
CORS(app)

# Load product catalog
with open("products.json") as f:
    products = json.load(f)

# Store preferences and history
user_preferences = {}
browsing_history = []

# Together API client (Meta-LLaMA)
client = Together(api_key="c3258504c91d05e34ddd4582bce9557df8a336b1c2ad21be004974c77e1e1089")

@app.route("/preferences", methods=["POST"])
def set_preferences():
    global user_preferences
    user_preferences = request.json
    return jsonify({"message": "Preferences saved."})

@app.route("/history", methods=["POST"])
def set_history():
    global browsing_history
    browsing_history.clear()
    browsing_history.extend(request.json.get("product_ids", []))
    return jsonify({"message": "Browsing history updated."})

@app.route("/recommend", methods=["GET"])
def recommend():
    if not user_preferences or not browsing_history:
        return jsonify({"error": "Missing preferences or history."}), 400

    viewed = [p for p in products if p["id"] in browsing_history]
    viewed_names = ", ".join(p["name"] for p in viewed) or "None"

    catalog_summary = "\n".join(
        [f"{p['name']} – ₹{p['price']} – {p['category']}" for p in products]
    )

    prompt = f"""
User Preferences:
- Interests: {', '.join(user_preferences.get('interests', []))}
- Budget: ₹{user_preferences.get('budget')}

Browsing History: {viewed_names}

Product Catalog:
{catalog_summary}

Based on the above, recommend 3 products with this format:
Product Name – ₹Price – Category
Reason: short explanation
"""

    response = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3-8B-Instruct-Reference",
        messages=[
            {"role": "system", "content": "You are an eCommerce product recommendation engine."},
            {"role": "user", "content": prompt},
        ]
    )

    return jsonify({"recommendations": response.choices[0].message.content})

if __name__ == "__main__":
    app.run(debug=True)
