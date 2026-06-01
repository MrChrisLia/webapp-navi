"""OpenAI-compatible chat completions provider.

Works with any backend exposing a /chat/completions-style API, including many
local model gateways and agent runtimes.
"""
from __future__ import annotations

import json
from typing import Any

import httpx

from hermes_api.config import settings
from hermes_api.providers.base import LLMProvider


class OpenAICompatibleProvider(LLMProvider):
    def __init__(self) -> None:
        self.base_url = (settings.base_url or "").strip().rstrip("/")
        self.model = (settings.model or "").strip()
        self.api_key = (settings.api_key or "").strip()
        self.timeout = 20.0

    def complete(self, prompt: str) -> str:
        if not self.base_url or not self.model:
            return (
                "LLM summary unavailable: configure HERMES_BASE_URL and HERMES_MODEL "
                "for openai_compatible provider."
            )
        try:
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You summarize web security endpoint behavior in one concise sentence.",
                    },
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.1,
            }
            response = self._post_json(self._chat_url(), payload)
            text = _extract_message_text(response)
            if text:
                return text.strip()
            return "LLM summary unavailable: empty response content from provider."
        except Exception as exc:
            return f"LLM summary unavailable: provider call failed ({exc})."

    def _chat_url(self) -> str:
        # If caller already supplied /chat/completions, use it directly.
        if self.base_url.endswith("/chat/completions"):
            return self.base_url
        return f"{self.base_url}/chat/completions"

    def _post_json(self, url: str, payload: dict[str, Any]) -> dict[str, Any]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        with httpx.Client(timeout=self.timeout) as client:
            r = client.post(url, headers=headers, content=json.dumps(payload))
            r.raise_for_status()
            return r.json()


def _extract_message_text(body: dict[str, Any]) -> str:
    choices = body.get("choices")
    if not isinstance(choices, list) or not choices:
        return ""
    first = choices[0]
    if not isinstance(first, dict):
        return ""
    message = first.get("message")
    if not isinstance(message, dict):
        return ""
    content = message.get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        # Some providers return multi-part content blocks.
        parts: list[str] = []
        for item in content:
            if isinstance(item, dict):
                t = item.get("text")
                if isinstance(t, str):
                    parts.append(t)
        return "\n".join(parts)
    return ""

