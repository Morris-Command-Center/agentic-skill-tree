from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class SkillLevel(str, Enum):
    LOCKED = "locked"
    AVAILABLE = "available"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Confidence(str, Enum):
    """Self-assessment confidence levels"""
    RED = "red"      # Just started, not ready to teach
    YELLOW = "yellow"  # Understand concepts, need more practice
    GREEN = "green"   # Can explain to others, have working examples


class Skill(BaseModel):
    """A single skill node in the tree"""
    id: str
    name: str
    description: str
    branch: str
    prerequisites: list[str] = Field(default_factory=list)
    xp_required: int = 100
    tips: list[str] = Field(default_factory=list)


class SkillBranch(BaseModel):
    """A branch of related skills"""
    id: str
    name: str
    description: str
    color: str
    skills: list[Skill] = Field(default_factory=list)


class Challenge(BaseModel):
    """A challenge to complete for XP"""
    id: str
    name: str
    description: str
    skill_ids: list[str]  # Skills this challenge trains
    xp_reward: int
    difficulty: str  # easy, medium, hard
    constraints: list[str] = Field(default_factory=list)
    success_criteria: str


class ChallengeCompletion(BaseModel):
    """Record of completing a challenge"""
    id: Optional[int] = None
    challenge_id: str
    completed_at: datetime = Field(default_factory=datetime.now)
    xp_earned: int
    notes: str = ""
    self_rating: int = Field(ge=1, le=5)  # 1-5 stars
    confidence: Optional[Confidence] = None


class SkillProgress(BaseModel):
    """Progress on a specific skill"""
    skill_id: str
    current_xp: int = 0
    level: SkillLevel = SkillLevel.LOCKED
    confidence: Confidence = Confidence.RED
    completions: list[ChallengeCompletion] = Field(default_factory=list)

    @property
    def is_unlocked(self) -> bool:
        return self.level != SkillLevel.LOCKED


class UserProgress(BaseModel):
    """Overall user progress"""
    skills: dict[str, SkillProgress] = Field(default_factory=dict)
    total_xp: int = 0
    challenges_completed: int = 0

    def get_skill_progress(self, skill_id: str) -> SkillProgress:
        if skill_id not in self.skills:
            self.skills[skill_id] = SkillProgress(skill_id=skill_id)
        return self.skills[skill_id]


class Achievement(BaseModel):
    """Unlockable achievement/badge"""
    id: str
    name: str
    description: str
    icon: str  # emoji or icon name
    criteria: str  # How to unlock (human readable)
    xp_bonus: int = 0
