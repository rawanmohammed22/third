# app/clients/cohere_client.py
import cohere
import os
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv(
    dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', 'database', '.env')
)

class CohereClient:
    def __init__(self):
        api_key = os.getenv("COHERE_API_KEY")
        if not api_key:
            raise ValueError("COHERE_API_KEY مش موجود في app/database/.env")

        self.client = cohere.ClientV2(api_key=api_key)

    def chat(
        self,
        messages: List[Dict[str, str]],
        model: str = "command-r-plus-08-2024",
        temperature: float = 0.7,
        max_tokens: int = 500,
    ) -> str:
        """
        ترسل قايمة رسائل كاملة (history + الرسالة الجديدة) وترجع الرد.
        """
        try:
            response = self.client.chat(
                messages=messages,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.message.content[0].text.strip()

        except Exception as e:
            raise RuntimeError(f"خطأ في Cohere: {str(e)}")


def get_cohere_client() -> CohereClient:
    return CohereClient()