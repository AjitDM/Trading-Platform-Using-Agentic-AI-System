from langchain_core.messages import HumanMessage

from src.llms.factory import get_analysis_llm


def blog_node(topic: str) -> dict:
    prompt = (
        "Write a concise educational blog outline about the following topic. "
        "Do not provide financial advice. Topic: "
        f"{topic}"
    )

    response = get_analysis_llm().invoke([HumanMessage(content=prompt)])

    return {
        "topic": topic,
        "content": response.content,
    }