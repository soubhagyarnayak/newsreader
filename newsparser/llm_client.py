from abc import ABC, abstractmethod

import anthropic


class LLMClient(ABC):
    @abstractmethod
    def complete(self, prompt: str) -> str:
        pass


class ClaudeLLMClient(LLMClient):
    def __init__(self, model="claude-opus-4-6", max_tokens=512):
        self.client = anthropic.Anthropic()
        self.model = model
        self.max_tokens = max_tokens

    def complete(self, prompt: str) -> str:
        message = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
