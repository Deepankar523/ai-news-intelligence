import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def analyze_article(title: str, content: str) -> dict:
    prompt = f"""
You are a news analyst. Analyze the following news article and return ONLY a JSON object with no extra text or markdown.

Article Title: {title}
Article Content: {content}

Return exactly this JSON structure:
{{
  "summary": "2-3 sentence summary of the article",
  "sentiment": "Positive or Negative or Neutral",
  "sentiment_score": a float between -1.0 (very negative) and 1.0 (very positive),
  "keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"]
}}
"""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()

        # Strip markdown code fences if present
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]

        return json.loads(text)

    except Exception as e:
        return {
            "summary": "Could not analyze this article.",
            "sentiment": "Neutral",
            "sentiment_score": 0.0,
            "keywords": []
        }