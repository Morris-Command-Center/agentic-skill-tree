import yaml
from pathlib import Path
from typing import Optional

from .models import Skill, SkillBranch, Challenge

DATA_DIR = Path(__file__).parent.parent / "data"


def load_skills() -> list[SkillBranch]:
    """Load skill tree from YAML"""
    skills_path = DATA_DIR / "skills.yaml"

    with open(skills_path) as f:
        data = yaml.safe_load(f)

    branches = []
    for branch_data in data.get("branches", []):
        skills = [
            Skill(
                id=s["id"],
                name=s["name"],
                description=s["description"],
                branch=branch_data["id"],
                prerequisites=s.get("prerequisites", []),
                xp_required=s.get("xp_required", 100),
                tips=s.get("tips", [])
            )
            for s in branch_data.get("skills", [])
        ]

        branch = SkillBranch(
            id=branch_data["id"],
            name=branch_data["name"],
            description=branch_data["description"],
            color=branch_data["color"],
            skills=skills
        )
        branches.append(branch)

    return branches


def load_challenges() -> list[Challenge]:
    """Load challenges from YAML"""
    challenges_path = DATA_DIR / "challenges.yaml"

    with open(challenges_path) as f:
        data = yaml.safe_load(f)

    return [
        Challenge(
            id=c["id"],
            name=c["name"],
            description=c["description"],
            skill_ids=c["skill_ids"],
            xp_reward=c["xp_reward"],
            difficulty=c["difficulty"],
            constraints=c.get("constraints", []),
            success_criteria=c["success_criteria"]
        )
        for c in data.get("challenges", [])
    ]


def get_skill_by_id(skill_id: str) -> Optional[Skill]:
    """Find a skill by ID"""
    for branch in load_skills():
        for skill in branch.skills:
            if skill.id == skill_id:
                return skill
    return None


def get_challenge_by_id(challenge_id: str) -> Optional[Challenge]:
    """Find a challenge by ID"""
    for challenge in load_challenges():
        if challenge.id == challenge_id:
            return challenge
    return None


def get_skills_for_branch(branch_id: str) -> list[Skill]:
    """Get all skills in a branch"""
    for branch in load_skills():
        if branch.id == branch_id:
            return branch.skills
    return []


def get_challenges_for_skill(skill_id: str) -> list[Challenge]:
    """Get all challenges that train a specific skill"""
    return [
        c for c in load_challenges()
        if skill_id in c.skill_ids
    ]
