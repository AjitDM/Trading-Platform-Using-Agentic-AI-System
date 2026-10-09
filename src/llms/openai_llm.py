from src.llms.gateway import get_llm_gateway


def get_openai_model():
    return get_llm_gateway().get_model("reasoning-model", temperature=0.0)