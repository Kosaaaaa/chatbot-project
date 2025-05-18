from polyfactory.factories.pydantic_factory import ModelFactory
from polyfactory.pytest_plugin import register_fixture

from app.config import Settings


@register_fixture
class SettingsFactory(ModelFactory[Settings]): ...
