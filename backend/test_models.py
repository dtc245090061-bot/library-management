import os
import httpx
from config import settings

API_KEY = settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY", "mock-key-for-test")
MODELS_TO_TRY = [
    "gemini-flash-latest",
    "gemini-pro-latest",
    "gemini-2.5-flash-lite",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemma-4-26b-a4b-it"
]

for model_name in MODELS_TO_TRY:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={API_KEY}"
    try:
        res = httpx.post(url, json={"contents": [{"parts": [{"text": "Hello"}]}]}, timeout=6.0)
        print(f"Model: {model_name} -> Status: {res.status_code}")
        if res.status_code == 200:
            print("FOUND WORKING MODEL:", model_name)
            break
        else:
            print("Error message:", res.text[:200])
    except Exception as e:
        print(f"Model: {model_name} -> Exception: {e}")
