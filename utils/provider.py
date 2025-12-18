from typing import Optional

from utils.constants import (
    PROVIDER_OPENAI,
    PROVIDER_GOOGLE,
    PROVIDER_DEEPSEEK
)
from utils.helper import KeyStore


class Provider:
    """封装单个服务的信息"""
    def __init__(self, name: str, enabled: bool = False):
        self.name = name
        self.enabled = enabled
        self._key: Optional[str] = None

    @property
    def key(self) -> Optional[str]:
        if self._key is None:
            self._key = KeyStore.get_key(self.name)
        return self._key

    @key.setter
    def key(self, value: str):
        self._key = value
        KeyStore.set_key(self.name, value)

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def is_enabled(self) -> bool:
        return self.enabled

class ProviderManager:
    """统一管理所有 Provider"""
    def __init__(self):
        self.providers = {
            PROVIDER_OPENAI: Provider(PROVIDER_OPENAI),
            PROVIDER_GOOGLE: Provider(PROVIDER_GOOGLE),
            PROVIDER_DEEPSEEK: Provider(PROVIDER_DEEPSEEK)
        }

    def get_provider(self, name: str) -> Optional[Provider]:
        return self.providers.get(name)

    def set_enabled(self, name: str, enabled: bool):
        provider = self.get_provider(name)
        if provider:
            provider.enabled = enabled

    def set_key(self, name: str, key: str):
        provider = self.get_provider(name)
        if provider:
            provider.key = key

    def get_key(self, name: str) -> Optional[str]:
        provider = self.get_provider(name)
        return provider.key if provider else None

    def enabled_providers(self) -> list[str]:
        return [p.name for p in self.providers.values() if p.enabled]

provider_manager = ProviderManager()