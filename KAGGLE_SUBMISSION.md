# Kaggle Capstone Submission — LifeShift Agent

Use this document when creating your writeup at:
https://www.kaggle.com/competitions/vibecoding-agents-capstone-project/writeups

**Track:** Concierge Agents  
**GitHub:** https://github.com/akankshashuklaWork/lifeshift-agent

---

## Writeup fields (copy-paste)

### Title
```
LifeShift: Your AI Concierge for Major Life Transitions
```

### Subtitle
```
A Google ADK multi-agent planner that turns life changes into phased plans, budgets, and next steps
```

### Short description (~250 words — for the writeup preview)
```
Major life transitions — relocating with a family, changing careers, preparing for a baby, or planning retirement — are overwhelming because they span finances, logistics, and timing all at once. Most people don't know where to start.

LifeShift is a personal concierge agent built with Google ADK that helps users navigate these changes in one conversation. Tell LifeShift your situation, and it returns a structured response: your situation summary, a phased transition plan, budget ranges, and your next three actions.

The agent combines Gemini with four custom planning tools (generate_transition_plan, estimate_budget, build_checklist, get_timeline_milestones), four ADK Agent Skills with domain playbooks (relocation, career change, new parent, retirement), and a multi-agent architecture with planner, budget, and checklist specialists. Security callbacks redact sensitive identifiers and remind users that LifeShift provides planning support only — not medical, legal, or financial advice.

I built a glassmorphic chat UI so the experience feels like talking to a concierge, not a debug console. An evaluation dataset with four test cases covers each transition type.

LifeShift is a planning prototype — budgets are illustrative ranges from structured tools, not live market data. But it demonstrates how ADK orchestration, skills, and tools can deliver actionable guidance for real personal decisions.

Built for the Kaggle AI Agents: Intensive Vibe Coding Capstone — Concierge Agents track.
```

---

## Full writeup body (paste into the main writeup editor)

### The problem

Life transitions are high-stakes and fragmented. Someone relocating in 12 weeks with two kids needs a timeline, a budget, school research, and a task list — but generic chatbots give vague advice, and spreadsheets don't talk back.

**LifeShift** acts as a personal concierge: one conversation → a structured plan you can act on this week.

---

### What LifeShift does

Users describe a transition in natural language. LifeShift:

1. Clarifies timeline, household, and constraints
2. Calls planning tools to generate phased plans and budget ranges
3. Loads domain skills (relocation playbook, career transition guide, etc.)
4. Returns a structured answer: **Situation · Plan · Budget · Next 3 Actions**

**Supported transitions:** relocation, career change, new parenthood, retirement.

**Example prompt:**
> "I'm relocating to Austin in 12 weeks with two kids. Help me plan and budget."

---

### Architecture

```
User → LifeShift UI → Gemini (lifeshift_concierge)
                          ├── Custom tools (app/tools.py)
                          ├── Agent skills (skills/)
                          └── Sub-agents (planner, budget, checklist)
                          → Structured response
```

| Component | Purpose |
|-----------|---------|
| `lifeshift_concierge` | Root agent — orchestrates tools and skills |
| `planner_agent` | Deep-dive transition planning |
| `budget_agent` | Budget estimation specialist |
| `checklist_agent` | Phase-specific task lists |
| `SkillToolset` | 4 markdown playbooks with reference docs |
| `callbacks.py` | PII redaction + professional-advice disclaimer |

---

### ADK features demonstrated

1. **Multi-agent orchestration** — concierge + 3 specialists via `sub_agents`
2. **Custom tools / function calling** — 4 structured planning tools
3. **Agent skills** — `SKILL.md` playbooks loaded via `SkillToolset`
4. **Security callbacks** — redact SSN/card patterns; append planning disclaimer
5. **Evaluation** — dataset with 4 cases (intro, relocation, career, new parent)
6. **Custom UI** — glassmorphic chat at `/lifeshift/` (bonus polish)

---

### Demo flow (what to show in video)

1. Open http://127.0.0.1:8080/lifeshift/
2. Click **Relocation** scenario card
3. Edit the template (city, weeks, household)
4. Send → show structured plan with phases, budget table, next actions
5. Briefly mention: built with Google ADK, multi-agent, tools, skills

---

### Limitations (honest)

- No live external data (housing, schools, cost-of-living APIs)
- Budget ranges are illustrative, scaled by household size — not city-specific quotes
- In-memory sessions only — no persistent user profiles
- Planning support only — not professional financial, legal, or medical advice

---

### Future work

- Integrate cost-of-living and housing APIs for location-aware budgets
- Persist plans across sessions
- Export milestones to calendar/PDF
- Deploy to Cloud Run / Agent Engine

---

### How to run

```bash
git clone https://github.com/akankshashuklaWork/lifeshift-agent.git
cd lifeshift-agent
cp .env.example .env   # add GEMINI_API_KEY
agents-cli install
./scripts/run_lifeshift_ui.sh
# Open http://127.0.0.1:8080/lifeshift/
```

**Code:** https://github.com/akankshashuklaWork/lifeshift-agent

---

## Thumbnail ideas

Pick one concept for your cover image (Canva, Figma, or screenshot):

- LifeShift UI with a relocation plan visible
- Dark glassmorphic chat + tagline: "Plan life's biggest changes"
- Simple logo + "Concierge Agents · Google ADK · Kaggle Capstone"

Recommended size: 1200×675 or similar landscape ratio.

---

## Demo video script (~2 minutes)

Record your screen + optional voiceover. Upload to **YouTube (public)** and link in the Kaggle media gallery.

### 0:00–0:20 — Hook / Problem
**Say:**
> "Major life changes — moving cities, switching careers, having a baby, retiring — are overwhelming. You need a plan, a budget, and to know what to do this week. That's why I built LifeShift."

**Show:** Title slide or LifeShift welcome screen.

---

### 0:20–0:40 — What it is
**Say:**
> "LifeShift is a personal concierge agent built with Google's Agent Development Kit. You describe your transition, and it returns a phased plan, budget estimate, and your next three actions — all in one conversation."

**Show:** Welcome screen with the four scenario cards.

---

### 0:40–1:30 — Live demo
**Say:**
> "Let me show a relocation example. I'm moving to Austin in 12 weeks with two kids."

**Do:**
1. Click **Relocation** card (or type the prompt)
2. Edit city/timeline if using template
3. Send message
4. Wait for response
5. Scroll through: Situation → Plan phases → Budget table → Next 3 Actions

**Say while scrolling:**
> "LifeShift calls custom ADK tools for structured planning, loads domain skills like the relocation playbook, and synthesizes everything into a clear answer. Behind the scenes: multi-agent orchestration, four custom tools, agent skills, and safety guardrails that redact sensitive info and remind users this is planning support, not professional advice."

---

### 1:30–1:50 — Tech stack
**Say:**
> "It's built with Google ADK — Gemini, multi-agent sub-agents, SkillToolset, custom function tools, security callbacks, and an eval dataset. Code is on GitHub."

**Show:** Quick flash of GitHub repo OR architecture from README (optional, 5 sec).

---

### 1:50–2:00 — Close
**Say:**
> "LifeShift shows how a concierge agent can turn a stressful life transition into an actionable plan. Thanks for watching."

**Show:** GitHub URL on screen:
`github.com/akankshashuklaWork/lifeshift-agent`

---

## Recording tips

- Start server before recording: `./scripts/run_lifeshift_ui.sh`
- Use a clean browser window (no extra tabs)
- 1080p screen recording is enough
- Speak clearly; 2 minutes is the target (max 5 min allowed)
- Test the relocation prompt once before recording so the response is fast

---

## Submission checklist

- [ ] Create writeup at Kaggle → **New Writeup**
- [ ] Select track: **Concierge Agents**
- [ ] Paste title, subtitle, description, full body
- [ ] Upload thumbnail / cover image
- [ ] Record demo video → upload to YouTube (public)
- [ ] Add video link to Kaggle media gallery
- [ ] Add GitHub link: https://github.com/akankshashuklaWork/lifeshift-agent
- [ ] Submit before deadline (July 7, 2026)
