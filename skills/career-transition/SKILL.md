---
name: career-transition
description: |
  Use when the user is changing careers, switching industries, or preparing
  for a new job search. Guides resume positioning, networking cadence, and
  interview preparation for LifeShift career-change plans.
license: Apache-2.0
metadata:
  author: lifeshift-agent
  version: "1.0"
---

# Career Transition Playbook

Apply when the user mentions career change, new industry, job search, or resignation.

## Workflow

1. Clarify **current role**, **target role**, **timeline**, and **financial runway**.
2. Call `generate_transition_plan` with `transition_type="career_change"`.
3. Call `build_checklist` for phase `preparation`.
4. If budget or runway matters, call `estimate_budget` with household size 1–2.

## Response structure

- **Situation** — from → to, and urgency
- **90-day plan** — learn, network, apply, interview, transition
- **Skill gaps** — 2–3 capabilities to build or demonstrate
- **Next 3 actions** — tasks for the next 7 days

## Mandatory reference

Load `references/career_transition_checklist.md` before giving final advice.

## Guardrails

- Do not guarantee job offers or salary figures.
- Recommend speaking with a career coach or financial advisor for major pivots.
