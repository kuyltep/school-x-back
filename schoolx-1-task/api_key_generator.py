from cryptography.hazmat.primitives import hashes, hmac

from src.app.config import configs


def encrypt_key(key: str) -> str:
  h = hmac.HMAC(configs.secret_key.get_secret_value().encode(), hashes.SHA256())
  h.update(key.encode())
  return h.finalize().hex()


print(encrypt_key("your api key here"))
