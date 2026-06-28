---
name: retirement-planning
description: |
  Use when the user is planning retirement or a major work-to-leisure transition.
  Guides timeline milestones, financial readiness categories, and lifestyle
  planning for LifeShift retirement transitions.
license: Apache-2.0
metadata:
  author: lifeshift-agent
  version: "1.0"
---

# Retirement Planning Playbook

Apply when the user mentions retiring, leaving the workforce, or financial independence.

## Workflow

1. Clarify **target retirement window**, **age**, and **dependents**.
2. Call `generate_transition_plan` with `transition_type="retirement"`.
3. Call `get_timeline_milestones` from today or their target date.
4. Call `estimate_budget` for healthcare bridge and lifestyle transition costs.

## Response structure

- **Situation** — timeline and goals for retirement
- **6–12 month milestone plan**
- **Budget categories** — healthcare, housing, lifestyle, contingency
- **Next 3 actions** — non-financial-advice planning steps only

## Mandatory reference

Load `references/retirement_milestones.md` before finalizing.

## Guardrails

- LifeShift does not provide investment or tax advice.
- Recommend a fiduciary financial advisor for withdrawal strategy and estate planning.
