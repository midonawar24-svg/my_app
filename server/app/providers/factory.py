from .base import AIProvider
from .echo_provider import EchoProvider
from .fake_provider import FakeProvider

PROVIDERS = {
    "echo": EchoProvider,
    "fake": FakeProvider,
}

def get_provider(name: str) -> AIProvider:
    provider_cls = PROVIDERS.get(name.lower(), EchoProvider)
    return provider_cls()
