"""Provider interface. The rest of Hermes only depends on this."""


class LLMProvider:
    def complete(self, prompt: str) -> str:
        raise NotImplementedError
