from src.llms.gateway import get_llm_gateway


def get_groq_model():
    return get_llm_gateway().get_model("fallback-model", temperature=0.0)