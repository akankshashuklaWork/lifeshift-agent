---
name: new-parent-readiness
description: |
  Use when the user is expecting a baby or recently became a parent. Covers
  leave planning, pediatric setup, home preparation, and budget categories
  for LifeShift family transition plans.
license: Apache-2.0
metadata:
  author: lifeshift-agent
  version: "1.0"
---

# New Parent Readiness Playbook

Apply for pregnancy, newborn preparation, parental leave, or first-year planning.

## Workflow

1. Confirm **due date or baby age**, **location**, and **support network**.
2. Call `generate_transition_plan` with `transition_type="new_parent"`.
3. Call `estimate_budget` with current household size.
4. Call `build_checklist` for phase `preparation` or `transition` as appropriate.

## Response structure

- **Situation** — timeline and household context
- **Trimester or month-by-month plan**
- **Budget categories** — medical, gear, childcare, leave buffer
- **Next 3 actions** — highest-impact tasks this week

## Mandatory reference

Load `references/new_parent_checklist.md` before finalizing.

## Guardrails

- Medical decisions require a healthcare provider — LifeShift only helps with planning.
- Childcare costs vary widely; present ranges, not guarantees.
