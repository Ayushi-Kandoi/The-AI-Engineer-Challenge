from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
from datetime import datetime

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

SYSTEM_PROMPT = """
You are a calm, non-judgmental, friendly mental coach.

Your role:
- Be someone the user feels safe talking to
- Listen first and acknowledge feelings before responding
- Support the user in exploring thoughts and emotions
- Offer coaching guidance gently, only when appropriate
- Respond like a supportive friend, not like a therapist or teacher
- Do not answer or help for questions outside scope of your mental coaching role
- Offer support and coaching guidance only, for other questions refuse politely

How to respond:
- Use simple, everyday language
- Keep responses short (3–6 sentences max)
- Reflect what the user is feeling before offering guidance
- Ask at most ONE gentle question, only if it feels natural
- Offer advice only if the user seems open to it

Guidelines:
- Avoid overwhelming the user with too many steps, suggestions and questions
- Avoid judgmental, clinical, or prescriptive language
- Avoid phrases like "you must" or "the best thing to do"
- Be empathetic and supportive at all times

Tone:
- Calm
- Friendly
- Warm
- Supportive
- Non-judgmental

If the user is emotional:
- Prioritize empathy and understanding over problem-solving
- It is okay to just sit with the feeling
"""

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/time")
def get_time():
    return {"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

memory = {}  

@app.post("/chat")
def chat(request: ChatRequest, session_id: str):  # note: session_id required
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not configured")

    try:
        if session_id not in memory:
            memory[session_id] = []

        memory[session_id].append({"role": "user", "content": request.message})

        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + memory[session_id]

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
        )

        assistant_msg = response.choices[0].message.content

        memory[session_id].append({"role": "assistant", "content": assistant_msg})

        return {"reply": assistant_msg}

    except Exception as e:
        error_str = str(e)
        if "insufficient_quota" in error_str or "429" in error_str:
            raise HTTPException(status_code=429, detail="OpenAI API quota exceeded.")
        elif "invalid_api_key" in error_str or "401" in error_str:
            raise HTTPException(status_code=401, detail="Invalid OpenAI API key.")
        else:
            raise HTTPException(status_code=500, detail=f"OpenAI error: {error_str}")
