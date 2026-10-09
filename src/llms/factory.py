from langchain_openai import ChatOpenAI

from src.config.settings import get_settings
from src.llms.gateway import get_llm_gateway


def get_analysis_llm() -> ChatOpenAI:
    settings = get_settings()
    return get_llm_gateway().get_model(
        model_name=settings.analysis_model,
        temperature=0.0,
    )


def get_reasoning_llm() -> ChatOpenAI:
    settings = get_settings()
    return get_llm_gateway().get_model(
        model_name=settings.reasoning_model,
        temperature=0.0,
    )


def get_fallback_llm() -> ChatOpenAI:
    settings = get_settings()
    return get_llm_gateway().get_model(
        model_name=settings.fallback_model,
        temperature=0.0,
    )