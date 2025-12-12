
class BaseTranslationService:
    def translate(self, text: str, target_lang: str) -> str:
        raise NotImplementedError
