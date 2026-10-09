from src.llms.gateway import get_llm_gateway


def get_gemini_model():
    return get_llm_gateway().get_model("analysis-model", temperature=0.0)