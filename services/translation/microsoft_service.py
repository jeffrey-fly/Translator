import os
import uuid
import requests
from typing import Optional
from .base import BaseTranslatorService

from abc import ABC, abstractmethod

class MicrosoftTranslatorService(BaseTranslatorService):
    """
    Microsoft Translator API 实现
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        region: Optional[str] = None,
        timeout: float = 5.0,
    ):
        """
        :param api_key: Azure Translator Key
        :param region: Azure region，如 'eastasia'
        :param timeout: HTTP 超时时间
        """
        self.api_key = api_key or os.getenv("AZURE_TRANSLATOR_KEY")
        self.region = region or os.getenv("AZURE_TRANSLATOR_REGION", "eastasia")
        self.timeout = timeout

        if not self.api_key:
            raise ValueError("Azure Translator API key is required")

        self.endpoint = "https://api.cognitive.microsofttranslator.com/translate"

    # ---------- 公共接口 ----------

    def translate(
        self,
        text: str,
        target_language: str = "zh",
        source_language: str = "auto"
    ) -> str:
        if not text.strip():
            return ""

        params = {
            "api-version": "3.0",
            "to": self._normalize_language(target_language),
        }

        if source_language != "auto":
            params["from"] = self._normalize_language(source_language)

        headers = {
            "Ocp-Apim-Subscription-Key": self.api_key,
            "Ocp-Apim-Subscription-Region": self.region,
            "Content-Type": "application/json",
            "X-ClientTraceId": str(uuid.uuid4()),
        }

        body = [{"text": text}]

        try:
            resp = requests.post(
                self.endpoint,
                params=params,
                headers=headers,
                json=body,
                timeout=self.timeout,
            )
            resp.raise_for_status()
            data = resp.json()

            return data[0]["translations"][0]["text"]

        except Exception as e:
            # ⚠️ 工程建议：这里不要 print，交给上层 logger
            # logger.exception("MicrosoftTranslatorService failed")
            return text  # 或 raise，看你系统风格

    # ---------- 内部工具 ----------

    def _normalize_language(self, lang: str) -> str:
        """
        统一语言代码，避免上层传值不一致
        """
        lang = lang.lower()

        if lang in ("zh", "zh-cn", "zh-hans"):
            return "zh-Hans"
        if lang in ("zh-tw", "zh-hant"):
            return "zh-Hant"

        return lang
