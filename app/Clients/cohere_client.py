# app/clients/cohere_client.py
import cohere
import os
from typing import Optional
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
        except Exception as e:
            raise RuntimeError(f"خطأ عام في Cohere: {str(e)}")


def get_cohere_client() -> CohereClient:
    return CohereClient()