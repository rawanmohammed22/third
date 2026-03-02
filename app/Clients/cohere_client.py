# app/clients/cohere_client.py
import cohere
import os

from typing import Optional

from typing import List, Dict

from dotenv import load_dotenv

# حمل .env من المسار الصحيح
load_dotenv(
    dotenv_path=os.path.join(
        os.path.dirname(__file__), '..', '..', 'database', '.env'
    )
)

class CohereClient:
    def __init__(self):
        api_key = os.getenv("COHERE_API_KEY")
        if not api_key:
            raise ValueError(
                "COHERE_API_KEY مش موجود في app/database/.env\n"
                "أضيفي سطر: COHERE_API_KEY=pk_xxxxxxxxxxxxxxxxxxxx"
            )

        self.client = cohere.ClientV2(api_key=api_key)

    def chat(
        self,
        message: str,
        model: str = "command-r-plus-08-2024",
        temperature: float = 0.7,
        max_tokens: int = 500,
    ) -> str:

        """
        ترسل رسالة واحدة وترجع الرد.
        """


        try:
            # الطريقة الصحيحة في V2: استخدم messages list
            messages = [{"role": "user", "content": message}]

            response = self.client.chat(
                messages=messages,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            return response.message.content[0].text.strip()  # ← الرد بيجي كده في V2

        except cohere.errors.APIError as e:
            raise RuntimeError(f"خطأ API من Cohere: {e.message}")
        except cohere.errors.BadRequestError as e:
            raise RuntimeError(f"طلب غير صحيح: {e.message}")

            return response.message.content[0].text.strip()

        except Exception as e:
            raise RuntimeError(f"خطأ عام في Cohere: {str(e)}")

    def analyze_cv(self, cv_text: str) -> str:
        """
        بتاخد نص الـ CV وترجع تحليل مفصّل.
        مخصصة للـ CV analysis بـ prompt احترافي وإعدادات مختلفة.
        """
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


def get_cohere_client() -> CohereClient:
    return CohereClient()