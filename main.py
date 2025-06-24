from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from together import Together
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


client = Together(api_key="c3258504c91d05e34ddd4582bce9557df8a336b1c2ad21be004974c77e1e1089")

with open("products.json") as f:
    products = json.load(f)

class UserPreferences(BaseModel):
    interests: list[str]
    budget: float

@app.post("/recommend")
def recommend(preferences: UserPreferences):
    prompt = (
        f"User likes: { ', '.join(preferences.interests)}, "
        f"Budget: ${preferences.budget}. "
        f"Recommend 3 products from this list: {json.dumps(products)}"
    )

    response = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3-8B-Instruct-Reference",  # Or "gpt-3.5-turbo" or other OpenAI-compatible models
        messages=[{"role": "system", "content": "GIVE ONLY ONE RECOMENDATION"},{"role": "user", "content":  prompt}],
    )

    return {"recommendations": response.choices[0].message.content}