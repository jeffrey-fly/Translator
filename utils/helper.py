from utils.constants import KEYRING_SERVICE_TRANSLATOR
import keyring

class KeyStore:
    """封装 Keyring 读写"""
    SERVICE_NAME = KEYRING_SERVICE_TRANSLATOR

    @staticmethod
    def set_key(key_name: str, value: str):
        keyring.set_password(KeyStore.SERVICE_NAME, key_name, value)

    @staticmethod
    def get_key(key_name: str) -> str | None:
        return keyring.get_password(KeyStore.SERVICE_NAME, key_name)