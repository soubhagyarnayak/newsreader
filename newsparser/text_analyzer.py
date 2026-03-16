from llm_client import ClaudeLLMClient, LLMClient


class TextAnalyzer:
    def __init__(self, llm_client: LLMClient = None):
        self.llm = llm_client or ClaudeLLMClient()

    def get_summary(self, text):
        return self.llm.complete(
            f"Summarize this article in 2-3 sentences:\n\n{text}"
        )

    def get_keywords(self, text):
        return self.llm.complete(
            f"List 5 keywords from this article, comma-separated, no explanation:\n\n{text}"
        )
