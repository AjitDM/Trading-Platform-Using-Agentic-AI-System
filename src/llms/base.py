from abc import ABC, abstractmethod
from typing import Any


class BaseLLMProvider(ABC):
    @abstractmethod
    def get_model(
        self,
        model_name: str | None = None,
        temperature: float = 0.0,
    ) -> Any:
        raise NotImplementedError