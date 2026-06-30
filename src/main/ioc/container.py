"""Lightweight dependency container for the refactored project structure."""

from dataclasses import dataclass, field
from types import SimpleNamespace


@dataclass
class Container:
    """Small container used by the app factory and presentation layer."""

    wiring_config: SimpleNamespace = field(
        default_factory=lambda: SimpleNamespace(modules=["src.presentation.controllers.auth"])
    )

    def wire(self, modules: list[str] | None = None) -> None:
        """Compatibility hook for DI wiring."""
        if modules is not None:
            self.wiring_config.modules = modules

    def get(self, name: str):
        """Return a simple service placeholder by name."""
        return None


