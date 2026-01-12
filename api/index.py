from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI()

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/chat")  # 👈 simpler & safer
def chat(request: ChatRequest):
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not configured")

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a supportive mental coach."},
                {"role": "user", "content": request.message},
            ],
        )
        return {"reply": response.choices[0].message.content}

    except Exception as e:
        error_str = str(e)

        if "insufficient_quota" in error_str or "429" in error_str:
            raise HTTPException(status_code=429, detail="OpenAI API quota exceeded.")
        elif "invalid_api_key" in error_str or "401" in error_str:
            raise HTTPException(status_code=401, detail="Invalid OpenAI API key.")
        else:
            raise HTTPException(status_code=500, detail=f"OpenAI error: {error_str}")
