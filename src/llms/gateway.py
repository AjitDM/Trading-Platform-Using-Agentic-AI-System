from functools import lru_cache

from langchain_openai import ChatOpenAI

from src.config.settings import get_settings


class LLMGateway:
    def __init__(self) -> None:
        self.settings = get_settings()

    def get_model(
        self,
        model_name: str | None = None,
        temperature: float = 0.0,
        timeout: int = 120,
    ) -> ChatOpenAI:
        return ChatOpenAI(
            model=model_name or self.settings.analysis_model,
            temperature=temperature,
            api_key=self.settings.llm_gateway_api_key,
            base_url=f"{self.settings.llm_gateway_url.rstrip('/')}/v1",
            timeout=timeout,
            max_retries=2,
        )


@lru_cache
def get_llm_gateway() -> LLMGateway:
    return LLMGateway()