from .base import AIProvider
from .echo_provider import EchoProvider

PROVIDERS = {
    "echo": EchoProvider,
}

def get_provider(name: str) -> AIProvider:
    """
    يرجع instance حسب الاسم.
    لو الاسم غير معروف، يستخدم Echo افتراضياً.
    """
    provider_cls = PROVIDERS.get(name.lower(), EchoProvider)
    return provider_cls()
