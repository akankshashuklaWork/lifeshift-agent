# ruff: noqa
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

import os
from pathlib import Path

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

from app.callbacks import redact_sensitive_user_input, remind_no_professional_advice
from app.skills_loader import build_skill_toolset
from app.tools import (
    build_checklist,
    estimate_budget,
    generate_transition_plan,
    get_timeline_milestones,
)

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_APP_DIR = Path(__file__).resolve().parent


def _configure_genai_auth() -> None:
    """Prefer Google AI Studio API key; fall back to Vertex AI if absent."""
    load_dotenv(_PROJECT_ROOT / ".env")
    load_dotenv(_APP_DIR / ".env")

    use_vertex = os.environ.get("GOOGLE_GENAI_USE_VERTEXAI", "").lower() == "true"
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

    if api_key and api_key.startswith("AQ."):
        use_vertex = True

    if api_key:
        os.environ.setdefault("GEMINI_API_KEY", api_key)

    if use_vertex:
        os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
        import google.auth
        try:
            _, project_id = google.auth.default()
            os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
        except Exception:
            pass
        os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "us-central1")
    else:
        os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"



_configure_genai_auth()

_MODEL = Gemini(
    model=os.environ.get("GEMINI_MODEL", "gemini-2.0-flash"),
    retry_options=types.HttpRetryOptions(attempts=5),
)

_skill_toolset = build_skill_toolset()

planner_agent = Agent(
    name="planner_agent",
    model=_MODEL,
    description="Creates phased transition plans and milestone timelines.",
    instruction=(
        "You are LifeShift's planning specialist. Clarify the user's transition "
        "type, timeline, and constraints. Use generate_transition_plan and "
        "get_timeline_milestones to produce structured, realistic plans. "
        "Keep advice practical and empathetic."
    ),
    tools=[generate_transition_plan, get_timeline_milestones],
    output_key="plan_context",
)

budget_agent = Agent(
    name="budget_agent",
    model=_MODEL,
    description="Estimates transition budgets and financial buffers.",
    instruction=(
        "You are LifeShift's budget advisor. Gather household size and location "
        "context, then call estimate_budget. Explain ranges clearly, highlight "
        "contingency needs, and never present estimates as guaranteed costs."
    ),
    tools=[estimate_budget],
    output_key="budget_context",
)

checklist_agent = Agent(
    name="checklist_agent",
    model=_MODEL,
    description="Builds actionable checklists by transition phase.",
    instruction=(
        "You are LifeShift's checklist specialist. Determine the transition type "
        "and whether the user is in preparation, transition, or stabilization. "
        "Use build_checklist and help the user prioritize the top three tasks."
    ),
    tools=[build_checklist],
    output_key="checklist_context",
)

root_agent = Agent(
    name="lifeshift_concierge",
    model=_MODEL,
    description=(
        "Personal concierge for major life transitions such as career changes, "
        "moves, new parenthood, and retirement."
    ),
    instruction=(
        "You are LifeShift, a warm and organized personal concierge for major "
        "life transitions (career change, relocation, new parent, retirement).\n\n"
        "Your job:\n"
        "1. Understand the user's situation with 1-2 clarifying questions when needed.\n"
        "2. Use agent skills for specialized playbooks: call list_skills, then "
        "load_skill for the best match (relocation-playbook, career-transition, "
        "new-parent-readiness, retirement-planning). Load referenced files with "
        "load_skill_resource when the skill instructs you to.\n"
        "3. Call planning tools: generate_transition_plan, estimate_budget, "
        "build_checklist, get_timeline_milestones.\n"
        "4. Only transfer to planner_agent, budget_agent, or checklist_agent "
        "when the user explicitly wants a deep dive with that specialist.\n"
        "5. Synthesize a clear response with sections: Situation, Plan, Budget, "
        "Next 3 Actions.\n"
        "6. Remember context within the conversation and stay encouraging.\n"
        "7. Never provide medical, legal, or investment advice — recommend "
        "professional help when appropriate.\n\n"
        "If the user shares sensitive identifiers, they are redacted automatically."
    ),
    tools=[
        _skill_toolset,
        generate_transition_plan,
        estimate_budget,
        build_checklist,
        get_timeline_milestones,
    ],
    sub_agents=[planner_agent, budget_agent, checklist_agent],
    before_model_callback=redact_sensitive_user_input,
    after_model_callback=remind_no_professional_advice,
)

app = App(
    root_agent=root_agent,
    name="app",
)
