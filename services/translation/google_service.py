# translate.py
from google.genai import Client

# 初始化 Google AI 客户端
client = Client()


def translate_text(text: str, target_language: str = "zh") -> str:
    """
    使用 Google AI 翻译文本，返回纯翻译结果（无杂音）。

    Args:
        text (str): 需要翻译的文本
        target_language (str): 目标语言代码，如 "zh"、"en"、"ja"

    Returns:
        str: 翻译后的文本
    """
    prompt = (
        f"Translate the following text to {target_language} ONLY. "
        f"Output exactly the translated text, do NOT add explanations, comments, or extra words:\n{text}"
    )

    response = client.generate_text(
        model="text-bison-001",  # Google AI 文本模型
        prompt=prompt,
        temperature=0.0  # 确保输出确定性
    )

    # response.text 是返回的翻译内容
    return response.text.strip()
