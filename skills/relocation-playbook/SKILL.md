---
name: relocation-playbook
description: |
  Use when the user is moving to a new city or country. Provides a structured
  relocation workflow, timeline checkpoints, and budget categories to cover
  in every LifeShift relocation plan.
license: Apache-2.0
metadata:
  author: lifeshift-agent
  version: "1.0"
---

# Relocation Playbook

Apply this skill whenever the user mentions moving, relocating, or changing cities.

## Workflow

1. Confirm **destination**, **move date**, **household size**, and **budget**.
2. Call `generate_transition_plan` with `transition_type="relocation"`.
3. Call `estimate_budget` with household size and destination city.
4. Call `get_timeline_milestones` from today's date or their target start date.
5. Call `build_checklist` for phase `preparation`, then highlight top 3 tasks.

## Response structure

Always include these sections:

- **Situation** — who is moving and by when
- **12-week plan** — phased actions from the playbook
- **Budget ranges** — moving, housing, setup, contingency
- **Next 3 actions** — concrete tasks for this week

## Mandatory reference

Before finalizing advice, load `references/relocation_timeline.md` via
`load_skill_resource` for the standard 12-week checkpoint list.

## Guardrails

- Remind users that school districts, visas, and lease terms need local verification.
- Never guarantee rent prices or job market outcomes.
