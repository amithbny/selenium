import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-cnn"
headers = {
    "Authorization": f"Bearer {os.getenv('HF_TOKEN')}",
}

def summarize(text, max_retries=3):
    payload = {
        "inputs": text,
        "parameters": {
            "min_length": 40,
            "max_length": 120
        }
    }

    for attempt in range(max_retries):
        try:
            print(f"⏳ LLM attempt {attempt + 1}...")
            response = requests.post(
                API_URL,
                headers=headers,
                json=payload,
                timeout=30   # IMPORTANT: prevents hanging
            )

            result = response.json()

            if "error" not in result:
                print("✅ Summary received")
                return result[0]["summary_text"]

            print("⚠️ LLM error:", result.get("error"))
            time.sleep(5)

        except requests.exceptions.RequestException as e:
            print("❌ Request failed:", e)
            time.sleep(5)

    return "⚠️ Summarization failed after multiple attempts."
