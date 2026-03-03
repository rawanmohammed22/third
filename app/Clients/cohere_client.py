# app/clients/cohere_client.py
import cohere
import os
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv(
    dotenv_path=os.path.join(
        os.path.dirname(__file__), '..', '..', 'database', '.env'
    )
)

class CohereClient:
    def __init__(self):
        api_key = os.getenv("COHERE_API_KEY")
        if not api_key:
            raise ValueError("COHERE_API_KEY مش موجود في app/database/.env")

        self.client = cohere.ClientV2(api_key=api_key)

    def chat(
        self,
        message: str,
        model: str = "command-r-plus-08-2024",
        temperature: float = 0.7,
        max_tokens: int = 500,
    ) -> str:
        try:
            response = self.client.chat(
                messages=[{"role": "user", "content": message}],
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.message.content[0].text.strip()
        except Exception as e:
            raise RuntimeError(f"خطأ في Cohere: {str(e)}")

    def embed(self, text: str) -> list[float]:
        try:
            response = self.client.embed(
                texts=[text],
                model="embed-multilingual-v3.0",
                input_type="search_document"
            )
            return response.embeddings.float[0]
        except Exception as e:
            raise RuntimeError(f"خطأ في Embedding: {str(e)}")

    def analyze_cv(self, cv_text: str) -> str:
        prompt = f"""
You are a senior career coach and HR specialist with 10+ years of experience 
reviewing CVs across multiple industries.

Analyze the following CV thoroughly and provide structured, actionable feedback:

---
{cv_text}
---

Provide your analysis in the following format:

### 1. STRENGTHS 💪
- Highlight strong points, impressive skills, and notable achievements
- Mention anything that makes this candidate stand out

### 2. WEAKNESSES ⚠️
- Identify gaps, missing sections, or weak areas
- Point out anything that might hurt the candidate's chances

### 3. SUGGESTIONS 💡
- Give specific, actionable recommendations for each weakness
- Suggest in-demand skills to add based on current market trends
- Recommend formatting or structural improvements if needed

### 4. OVERALL SCORE 🎯
- Score out of 10 with justification

Be honest, specific, and constructive. Focus on helping the candidate improve.
        """
        try:
            response = self.client.chat(
                messages=[{"role": "user", "content": prompt}],
                model="command-r-plus-08-2024",
                temperature=0.3,
                max_tokens=2000,
            )
            return response.message.content[0].text.strip()
        except Exception as e:
            raise RuntimeError(f"خطأ في CV Analysis: {str(e)}")

    def analyze_video(self, script: str) -> str:
        prompt = f"""
You are an expert content analyst and video strategist.

Analyze the following video transcript and provide:

### 1. SUMMARY 📝
- Brief summary of the video content (3-5 sentences)

### 2. KEY TOPICS 🎯
- List the main topics covered in the video

### 3. SUGGESTIONS 💡
- Suggest 5 related topics or videos the viewer might be interested in
- Suggest improvements if this is educational content

### 4. TARGET AUDIENCE 👥
- Who is this video for?

### 5. CONTENT QUALITY ⭐
- Rate the content quality out of 10 with justification

Transcript:
{script}
        """
        try:
            response = self.client.chat(
                messages=[{"role": "user", "content": prompt}],
                model="command-r-plus-08-2024",
                temperature=0.3,
                max_tokens=2000,
            )
            return response.message.content[0].text.strip()
        except Exception as e:
            raise RuntimeError(f"خطأ في Video Analysis: {str(e)}")


def get_cohere_client() -> CohereClient:
    return CohereClient()