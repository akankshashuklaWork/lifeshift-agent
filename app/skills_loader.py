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

"""Load LifeShift ADK skills from the project skills/ directory."""

from __future__ import annotations

from pathlib import Path

from google.adk.skills import load_skill_from_dir
from google.adk.skills.models import Skill
from google.adk.tools.skill_toolset import SkillToolset

_SKILLS_ROOT = Path(__file__).resolve().parent.parent / "skills"


def load_lifeshift_skills() -> list[Skill]:
    """Load every skill folder that contains a SKILL.md file."""
    if not _SKILLS_ROOT.is_dir():
        return []

    skills: list[Skill] = []
    for skill_dir in sorted(_SKILLS_ROOT.iterdir()):
        if skill_dir.is_dir() and (skill_dir / "SKILL.md").is_file():
            skills.append(load_skill_from_dir(skill_dir))
    return skills


def build_skill_toolset() -> SkillToolset:
    """Create the SkillToolset wired into the LifeShift concierge."""
    return SkillToolset(skills=load_lifeshift_skills())
