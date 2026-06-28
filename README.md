# LifeShift Agent

**LifeShift** is a personal concierge agent for major life transitions — built for the
[Kaggle AI Agents: Intensive Vibe Coding Capstone Project](https://www.kaggle.com/competitions/vibecoding-agents-capstone-project/overview)
under the **Concierge Agents** track.

It helps users navigate **career changes**, **relocations**, **new parenthood**, and **retirement** with phased plans, budget estimates, checklists, and milestone timelines.

---

## What this app does

LifeShift is an **AI planning concierge**. When you describe a life change, the agent:

1. **Understands your situation** — timeline, household, location, constraints (via Gemini).
2. **Calls structured planning tools** — phased plans, budget ranges, checklists, and milestones from `app/tools.py`.
3. **Loads domain playbooks** — ADK Agent Skills in `skills/` guide tool use and response structure.
4. **Synthesizes a conversational answer** — Situation, Plan, Budget, and Next 3 Actions.

### Supported transition types

| Type | Example user intent |
|------|---------------------|
| Relocation | Moving to a new city with family and a deadline |
| Career change | Switching roles or industries |
| New parent | Preparing for a baby (checklist + budget) |
| Retirement | Phasing income, healthcare, and lifestyle |

### Architecture

```
User message
    ↓
Gemini (lifeshift_concierge) + agent instructions
    ↓
├── Custom tools (app/tools.py)     → plans, budgets, checklists
├── Agent skills (skills/)          → markdown playbooks + references
└── Sub-agents                      → planner, budget, checklist specialists
    ↓
Formatted response in the LifeShift UI
```

### ADK features demonstrated

| Feature | Implementation |
|---------|----------------|
| Multi-agent orchestration | Concierge + planner, budget, checklist specialists |
| Agent skills | 4 playbooks in `skills/` via `SkillToolset` |
| Custom tools | `generate_transition_plan`, `estimate_budget`, `build_checklist`, `get_timeline_milestones` |
| Security guardrails | PII redaction + professional-advice reminders |
| Custom UI | Glassmorphic chat at `/lifeshift/` |
| Evaluation | `tests/eval/datasets/basic-dataset.json` |

---

## Limitations

LifeShift does **not** use live external data (no housing APIs, school databases, or financial feeds). Plans and budgets come from hand-authored logic in `app/tools.py` and markdown playbooks in `skills/`. Gemini may mention real places from general model knowledge, but numbers are **illustrative ranges**, not verified quotes.

LifeShift provides **planning support only** — not medical, legal, or financial advice.

---

## Quick start

### Requirements

- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [agents-cli](https://github.com/google/adk-python) (`uv tool install google-agents-cli`)
- [Google AI Studio API key](https://aistudio.google.com/apikey) OR Google Cloud/Vertex AI credentials (including `AQ.` formatted key)

### Setup

```bash
git clone https://github.com/akankshashuklaWork/lifeshift-agent.git
cd lifeshift-agent
cp .env.example .env
# Add your GEMINI_API_KEY to .env
agents-cli install
```

### Run

```bash
./scripts/run_lifeshift_ui.sh
```

Open **http://127.0.0.1:8080/lifeshift/** and describe a life transition. Pick a scenario card to prefill a template, edit it, then send.

### Evaluate (optional)

```bash
agents-cli eval generate
agents-cli eval grade
```

---

## Project structure

```
lifeshift-agent/
├── app/                  # ADK agent, tools, callbacks, FastAPI app
├── frontend/             # Glassmorphic chat UI
├── skills/               # ADK Agent Skills (relocation, career, new parent, retirement)
├── scripts/              # run_lifeshift_ui.sh
└── tests/eval/           # Eval dataset and config
```

---

## Future work

- Integrate real data (cost-of-living, housing, schools) for location-aware budgets
- Persist plans and checklists across sessions
- City-specific budget multipliers and calendar/PDF export
- Expand eval datasets and deploy to Cloud Run / Agent Engine

---

## License

Apache 2.0
