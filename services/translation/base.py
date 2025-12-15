from abc import ABC, abstractmethod


class BaseTranslatorService(ABC):
    """
    翻译服务基类
    """

    @abstractmethod
    def translate(self, text: str, target_language: str = "zh", source_language: str = "auto") -> str:
        """
        翻译文本
        :param text: 待翻译文本
        :param target_language: 目标语言
        :param source_language: 源语言，'auto' 表示自动检测
        :return: 翻译结果
        """
        pass
