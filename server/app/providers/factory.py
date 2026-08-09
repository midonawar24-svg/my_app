from .base import AIProvider
from .echo_provider import EchoProvider
from .fake_provider import FakeProvider
from .local_provider import LocalAIProvider
from .real_provider import RealAIProvider


PROVIDERS: dict[str, type[AIProvider]] = {
    "echo": EchoProvider,
    "fake": FakeProvider,
    "real": RealAIProvider,
    "local": LocalAIProvider,
}


def get_provider(name: str) -> AIProvider:
    provider_name = name.strip().lower()

    provider_cls = PROVIDERS.get(provider_name)

    if provider_cls is None:
        raise ValueError(
            f"Unknown AI provider: {name}. "
            f"Available providers: {', '.join(sorted(PROVIDERS))}"
        )

    return provider_cls()
