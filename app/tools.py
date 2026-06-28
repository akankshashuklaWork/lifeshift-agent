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

"""LifeShift concierge tools for major life transition planning."""

from __future__ import annotations

import datetime
from typing import Literal

TransitionType = Literal[
    "career_change",
    "relocation",
    "new_parent",
    "retirement",
    "other",
]

Phase = Literal["preparation", "transition", "stabilization"]

_TRANSITION_LABELS = {
    "career_change": "Career transition",
    "relocation": "Relocation",
    "new_parent": "New parent journey",
    "retirement": "Retirement planning",
    "other": "Life transition",
}

_PLAN_PHASES = {
    "career_change": [
        ("Weeks 1-2", "Clarify goals, audit skills, update resume and LinkedIn"),
        ("Weeks 3-4", "Network, apply selectively, schedule informational interviews"),
        ("Weeks 5-8", "Interview prep, negotiate offers, plan resignation handoff"),
        ("Weeks 9-12", "Onboard, set 90-day success metrics, build new routines"),
    ],
    "relocation": [
        ("Weeks 1-2", "Define budget, shortlist cities, research neighborhoods"),
        ("Weeks 3-4", "Visit top locations, compare housing and schools"),
        ("Weeks 5-8", "Secure housing, plan move logistics, transfer utilities"),
        ("Weeks 9-12", "Settle in, build local network, update legal documents"),
    ],
    "new_parent": [
        ("Weeks 1-4", "Confirm care plan, budget for leave, notify employer"),
        ("Weeks 5-8", "Prepare home, finalize pediatrician, pack hospital bag"),
        ("Weeks 9-12", "Establish feeding/sleep routines, delegate chores, rest"),
        ("Months 4-6", "Childcare transition, revisit finances, protect couple time"),
    ],
    "retirement": [
        ("Months 1-2", "Audit savings, estimate monthly spend, review healthcare"),
        ("Months 3-4", "Model income streams, consult advisor, stress-test budget"),
        ("Months 5-6", "Plan lifestyle rhythm, social connections, volunteer goals"),
        ("Months 7-12", "Execute rollover steps, update beneficiaries, trial budget"),
    ],
    "other": [
        ("Phase 1", "Define success criteria and non-negotiables"),
        ("Phase 2", "Break the change into weekly actions"),
        ("Phase 3", "Execute highest-impact tasks first"),
        ("Phase 4", "Review progress and adjust the plan"),
    ],
}

_CHECKLIST_ITEMS: dict[str, dict[str, list[str]]] = {
    "career_change": {
        "preparation": [
            "List target roles and industries",
            "Refresh resume and portfolio",
            "Identify 10 people to reconnect with",
            "Set weekly application and networking targets",
        ],
        "transition": [
            "Prepare STAR stories for interviews",
            "Research salary bands for target roles",
            "Plan notice period and knowledge transfer",
        ],
        "stabilization": [
            "Define 30-60-90 day goals for new role",
            "Schedule manager alignment check-in",
            "Rebuild personal routines around new schedule",
        ],
    },
    "relocation": {
        "preparation": [
            "Create relocation budget spreadsheet",
            "Compare cost of living across top cities",
            "Check visa or license requirements if applicable",
        ],
        "transition": [
            "Book movers or shipping for key items",
            "Update address with bank, employer, and IRS",
            "Set up utilities and internet before arrival",
        ],
        "stabilization": [
            "Find primary care and local services",
            "Join one community group or hobby club",
            "Review budget after first month in new city",
        ],
    },
    "new_parent": {
        "preparation": [
            "Confirm parental leave benefits and dates",
            "Choose pediatrician and hospital preference",
            "Build a support roster (family, friends, neighbors)",
        ],
        "transition": [
            "Stock essentials for first two weeks at home",
            "Prepare freezer meals and chore schedule",
            "Install car seat and finalize birth plan",
        ],
        "stabilization": [
            "Protect sleep windows for primary caregiver",
            "Schedule pediatric follow-ups",
            "Revisit budget for childcare and supplies",
        ],
    },
    "retirement": {
        "preparation": [
            "Consolidate account list and beneficiary forms",
            "Estimate healthcare costs before Medicare",
            "Discuss retirement vision with partner or family",
        ],
        "transition": [
            "Model withdrawal order for tax efficiency",
            "Plan part-time or consulting bridge if needed",
            "Set a target retirement date range",
        ],
        "stabilization": [
            "Create a weekly structure for purpose and health",
            "Test retirement spending for 3 months if possible",
            "Review estate documents with a professional",
        ],
    },
    "other": {
        "preparation": [
            "Write down why this change matters",
            "List risks and constraints",
        ],
        "transition": [
            "Pick the top 3 actions for this week",
            "Assign owners and deadlines",
        ],
        "stabilization": ["Review what worked", "Adjust the plan for the next month"],
    },
}

_BUDGET_BASE_USD = {
    "career_change": {
        "coaching_or_courses": (500, 2500),
        "interview_travel": (200, 1500),
        "wardrobe_refresh": (150, 800),
        "income_gap_buffer": (2000, 8000),
    },
    "relocation": {
        "moving_services": (1500, 8000),
        "deposits_and_fees": (3000, 12000),
        "travel_to_scout": (500, 2500),
        "setup_and_furniture": (1000, 5000),
    },
    "new_parent": {
        "medical_and_birth": (1000, 8000),
        "gear_and_nursery": (800, 3500),
        "childcare_deposit": (0, 3000),
        "parental_leave_buffer": (3000, 15000),
    },
    "retirement": {
        "financial_planning": (500, 3000),
        "healthcare_bridge": (4000, 12000),
        "home_modifications": (0, 10000),
        "lifestyle_transition": (1000, 5000),
    },
    "other": {
        "planning_and_advice": (200, 1500),
        "one_time_costs": (500, 5000),
        "contingency_buffer": (1000, 5000),
    },
}


def _normalize_transition_type(transition_type: str) -> TransitionType:
    normalized = transition_type.strip().lower().replace(" ", "_").replace("-", "_")
    aliases = {
        "career": "career_change",
        "job_change": "career_change",
        "move": "relocation",
        "moving": "relocation",
        "baby": "new_parent",
        "parent": "new_parent",
        "retire": "retirement",
    }
    normalized = aliases.get(normalized, normalized)
    if normalized in _TRANSITION_LABELS:
        return normalized  # type: ignore[return-value]
    return "other"


def generate_transition_plan(
    transition_type: str,
    timeline_weeks: int,
    constraints: str,
) -> dict:
    """Create a phased transition plan tailored to the user's situation.

    Args:
        transition_type: Type of life change (career_change, relocation,
            new_parent, retirement, or other).
        timeline_weeks: Target planning horizon in weeks (typically 8-24).
        constraints: User constraints such as budget, family, location, or deadlines.

    Returns:
        A structured plan with phases, focus areas, and next steps.
    """
    kind = _normalize_transition_type(transition_type)
    label = _TRANSITION_LABELS[kind]
    phases = _PLAN_PHASES[kind]
    horizon = max(4, min(timeline_weeks, 52))

    return {
        "transition_type": kind,
        "transition_label": label,
        "timeline_weeks": horizon,
        "constraints_considered": constraints.strip() or "None specified",
        "phases": [
            {
                "phase": index + 1,
                "window": window,
                "focus": focus,
            }
            for index, (window, focus) in enumerate(phases)
        ],
        "immediate_next_steps": [
            f"Confirm your top priority for this {label.lower()}",
            "Share constraints with LifeShift so plans stay realistic",
            f"Use build_checklist for the preparation phase of {kind}",
        ],
        "disclaimer": (
            "Estimates are planning aids only. Confirm legal, medical, and "
            "financial decisions with qualified professionals."
        ),
    }


def estimate_budget(
    transition_type: str,
    household_size: int,
    location: str,
) -> dict:
    """Estimate rough budget ranges for a life transition.

    Args:
        transition_type: Type of life change (career_change, relocation,
            new_parent, retirement, or other).
        household_size: Number of people in the household (1-8).
        location: City or region for cost context (used for narrative only).

    Returns:
        Category-level budget ranges in USD and planning notes.
    """
    kind = _normalize_transition_type(transition_type)
    size_factor = 1.0 + max(0, min(household_size, 8) - 1) * 0.12
    location_note = location.strip() or "unspecified location"

    categories = []
    total_low = 0
    total_high = 0
    for name, (low, high) in _BUDGET_BASE_USD[kind].items():
        adj_low = int(low * size_factor)
        adj_high = int(high * size_factor)
        total_low += adj_low
        total_high += adj_high
        categories.append(
            {
                "category": name.replace("_", " ").title(),
                "low_usd": adj_low,
                "high_usd": adj_high,
            }
        )

    return {
        "transition_type": kind,
        "household_size": household_size,
        "location_context": location_note,
        "categories": categories,
        "total_range_usd": {"low": total_low, "high": total_high},
        "planning_tips": [
            "Keep a 10-15% contingency line item",
            "Separate one-time costs from monthly burn",
            "Revisit the estimate after your first planning call",
        ],
        "disclaimer": "Illustrative ranges only — not financial advice.",
    }


def build_checklist(
    transition_type: str,
    phase: str,
) -> dict:
    """Return an actionable checklist for a transition phase.

    Args:
        transition_type: Type of life change (career_change, relocation,
            new_parent, retirement, or other).
        phase: Planning phase — preparation, transition, or stabilization.

    Returns:
        Checklist items grouped by phase with completion guidance.
    """
    kind = _normalize_transition_type(transition_type)
    normalized_phase = phase.strip().lower()
    if normalized_phase not in {"preparation", "transition", "stabilization"}:
        normalized_phase = "preparation"

    items = _CHECKLIST_ITEMS[kind].get(normalized_phase, [])
    return {
        "transition_type": kind,
        "phase": normalized_phase,
        "items": [{"task": item, "status": "pending"} for item in items],
        "tip": "Ask LifeShift to reprioritize tasks based on your deadline.",
    }


def get_timeline_milestones(
    transition_type: str,
    start_date: str,
) -> dict:
    """Build dated milestones from a transition start date.

    Args:
        transition_type: Type of life change (career_change, relocation,
            new_parent, retirement, or other).
        start_date: Start date in YYYY-MM-DD format.

    Returns:
        Milestone list with suggested target dates.
    """
    kind = _normalize_transition_type(transition_type)
    try:
        start = datetime.date.fromisoformat(start_date.strip())
    except ValueError:
        start = datetime.date.today()

    offsets_weeks = [2, 4, 8, 12]
    phases = _PLAN_PHASES[kind]
    milestones = []
    for index, (window, focus) in enumerate(phases):
        weeks = offsets_weeks[min(index, len(offsets_weeks) - 1)]
        target = start + datetime.timedelta(weeks=weeks)
        milestones.append(
            {
                "milestone": window,
                "target_date": target.isoformat(),
                "focus": focus,
            }
        )

    return {
        "transition_type": kind,
        "start_date": start.isoformat(),
        "milestones": milestones,
    }
