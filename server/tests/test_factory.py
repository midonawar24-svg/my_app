from app.providers.factory import get_provider
from app.providers.echo_provider import EchoProvider

def test_factory_returns_echo():
    provider = get_provider("echo")
    assert isinstance(provider, EchoProvider)

def test_factory_defaults_to_echo():
    provider = get_provider("unknown")
    assert isinstance(provider, EchoProvider)

def test_factory_case_insensitive():
    provider = get_provider("ECHO")
    assert isinstance(provider, EchoProvider)
