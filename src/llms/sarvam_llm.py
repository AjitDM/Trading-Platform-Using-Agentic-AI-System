from src.llms.gateway import get_llm_gateway


def get_sarvam_model():
    return get_llm_gateway().get_model("sarvam-model", temperature=0.0)