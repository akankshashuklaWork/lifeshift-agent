# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Safety callbacks for LifeShift."""

from __future__ import annotations

import re

from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.genai import types

_SENSITIVE_PATTERNS = [
    (re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), "[REDACTED_SSN]"),
    (re.compile(r"\b\d{16}\b"), "[REDACTED_CARD]"),
    (re.compile(r"\b\d{9}\b"), "[REDACTED_ID]"),
]


def _redact_text(text: str) -> str:
    redacted = text
    for pattern, replacement in _SENSITIVE_PATTERNS:
        redacted = pattern.sub(replacement, redacted)
    return redacted


async def redact_sensitive_user_input(
    callback_context: CallbackContext,
    llm_request: LlmRequest,
) -> LlmResponse | None:
    """Redact likely SSN or payment identifiers before the model sees user text."""
    del callback_context  # reserved for future session-aware policies
    if not llm_request.contents:
        return None

    for content in llm_request.contents:
        if content.role != "user" or not content.parts:
            continue
        for part in content.parts:
            if part.text:
                part.text = _redact_text(part.text)
    return None


async def remind_no_professional_advice(
    callback_context: CallbackContext,
    llm_response: LlmResponse,
) -> LlmResponse | None:
    """Append a safety reminder when financial or medical topics appear."""
    del callback_context
    if not llm_response.content or not llm_response.content.parts:
        return None

    combined = " ".join(part.text or "" for part in llm_response.content.parts).lower()
    triggers = ("budget", "medical", "healthcare", "tax", "legal", "invest")
    if not any(word in combined for word in triggers):
        return None

    reminder = (
        "\n\n_Reminder: LifeShift provides planning support only. "
        "Confirm financial, legal, and medical decisions with qualified professionals._"
    )
    llm_response.content.parts.append(types.Part(text=reminder))
    return llm_response
