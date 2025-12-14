from google import genai
from google.genai import types

client = genai.Client()

def translate_text(text: str, target_language: str = "zh") -> str:
    """
    使用 Google AI 翻译文本
    """
    prompt = (
        f"Translate the English word '{text}' into {target_language}.\n"
        "For each possible meaning, categorize by part of speech (e.g., n, vt, vi, adj),\n"
        "provide all meanings in Chinese for that part of speech, and give at most 1 example sentence per part of speech.\n"
        "Each example sentence should show the original English sentence, a slash '/', then the Chinese translation.\n"
        "Output format:\n"
        "part_of_speech: meaning1; meaning2; ...\n"
        "Example: English sentence / Chinese translation\n"
        "Do not include any explanations in English."
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[prompt],
        config=types.GenerateContentConfig(
            temperature=0  # 保证输出稳定
        )
    )
    return response.text.strip()


if __name__ == "__main__":
    print(translate_text("Hello, how are you?", "zh"))
