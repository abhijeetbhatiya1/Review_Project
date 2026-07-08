"""
The backend: a small FastAPI service that analyzes ONE customer review.

Run it with:
    uv run fastapi dev api.py

Then the Streamlit app (app.py) will call this service for every review.
"""

from fastapi import FastAPI
from pydantic import BaseModel
import ollama

"""llama3.2:3b is used for this project"""
model = "llama3.2:3b"

app = FastAPI()


# What the caller must SEND us
class Review(BaseModel):
    text: str

# What AI Model gives back, and what we SEND to the caller.
# We keep it small on purpose -> fewer tokens used.
class Analysis(BaseModel):
    label: str   # "positive", "negative", or "neutral"
    score: int   # 1 (very bad) to 5 (very good)
    theme: str   # one word: what the review is mainly about (e.g. "delivery")

@app.get('/')
def home():
    return {"message":"Welcome to the Review analysis project."}

@app.post('/analyze', response_model=Analysis)
def analyze(review: Review):
    prompt = (
        "Analyze this customer review."
        "label must be 'positive', 'negative', or 'neutral'."
        "score must be a number from 1 (very bad) to 5 (very good)."
        "theme must be ONE lowercase word for the main topic "
        "(for example: delivery, taste, price, service, quality)."
        f"Review: {review.text}"
    )

    response = ollama.chat(
        model=model,
        messages=[
            {"role":"user", "content":prompt}
        ],
        format = Analysis.model_json_schema(),
        options={"temperature":0}
    )

    raw_content = response['message']['content']
    parsed_content = Analysis.model_validate_json(raw_content)

    return parsed_content