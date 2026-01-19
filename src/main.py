from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, PlainTextResponse
from pathlib import Path
from pydantic import BaseModel
from typing import Optional

from .models import (
    SkillBranch, Challenge, SkillProgress, SkillLevel,
    Confidence, ChallengeCompletion, UserProgress
)
from .data_loader import (
    load_skills, load_challenges, get_skill_by_id,
    get_challenge_by_id, get_challenges_for_skill
)
from . import database as db

app = FastAPI(
    title="Agentic Skill Tree",
    description="Gamified progression for mastering agentic coding",
    version="0.1.0"
)

STATIC_DIR = Path(__file__).parent.parent / "static"
LEARNING_DIR = Path(__file__).parent.parent / "data" / "learning"


# Request/Response models
class CompleteChallenge(BaseModel):
    challenge_id: str
    notes: str = ""
    self_rating: int  # 1-5
    confidence: Optional[Confidence] = None


class UpdateSkillConfidence(BaseModel):
    skill_id: str
    confidence: Confidence


# API Routes
@app.get("/api/skills", response_model=list[SkillBranch])
def get_skills():
    """Get the complete skill tree"""
    return load_skills()


@app.get("/api/challenges", response_model=list[Challenge])
def get_challenges():
    """Get all available challenges"""
    return load_challenges()


@app.get("/api/challenges/{skill_id}", response_model=list[Challenge])
def get_challenges_by_skill(skill_id: str):
    """Get challenges for a specific skill"""
    challenges = get_challenges_for_skill(skill_id)
    if not challenges:
        # Check if skill exists
        if not get_skill_by_id(skill_id):
            raise HTTPException(status_code=404, detail="Skill not found")
    return challenges


@app.get("/api/progress", response_model=UserProgress)
def get_progress():
    """Get user's overall progress"""
    return db.get_user_progress()


@app.get("/api/progress/{skill_id}", response_model=Optional[SkillProgress])
def get_skill_progress(skill_id: str):
    """Get progress for a specific skill"""
    skill = get_skill_by_id(skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    progress = db.get_skill_progress(skill_id)
    if not progress:
        # Return default progress for new skill
        progress = SkillProgress(skill_id=skill_id)
    return progress


@app.post("/api/complete")
def complete_challenge(data: CompleteChallenge):
    """Record a challenge completion"""
    challenge = get_challenge_by_id(data.challenge_id)
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")

    # Create completion record
    completion = ChallengeCompletion(
        challenge_id=data.challenge_id,
        xp_earned=challenge.xp_reward,
        notes=data.notes,
        self_rating=data.self_rating,
        confidence=data.confidence
    )

    completion_id = db.add_challenge_completion(completion)

    # Update skill progress for each skill the challenge trains
    for skill_id in challenge.skill_ids:
        progress = db.get_skill_progress(skill_id)
        if not progress:
            progress = SkillProgress(skill_id=skill_id)

        # Add XP
        progress.current_xp += challenge.xp_reward

        # Check for level up
        skill = get_skill_by_id(skill_id)
        if skill and progress.current_xp >= skill.xp_required:
            if progress.level == SkillLevel.LOCKED:
                progress.level = SkillLevel.AVAILABLE
            elif progress.level == SkillLevel.AVAILABLE:
                progress.level = SkillLevel.IN_PROGRESS
            elif progress.level == SkillLevel.IN_PROGRESS:
                progress.level = SkillLevel.COMPLETED

        # Update confidence if provided
        if data.confidence:
            progress.confidence = data.confidence

        db.update_skill_progress(progress)

    return {
        "success": True,
        "completion_id": completion_id,
        "xp_earned": challenge.xp_reward
    }


@app.post("/api/confidence")
def update_confidence(data: UpdateSkillConfidence):
    """Update self-assessed confidence for a skill"""
    skill = get_skill_by_id(data.skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    progress = db.get_skill_progress(data.skill_id)
    if not progress:
        progress = SkillProgress(skill_id=data.skill_id)

    progress.confidence = data.confidence
    db.update_skill_progress(progress)

    return {"success": True}


@app.get("/api/completions")
def get_completions(challenge_id: Optional[str] = None):
    """Get challenge completion history"""
    return db.get_challenge_completions(challenge_id)


@app.get("/api/learn/{skill_id}", response_class=PlainTextResponse)
def get_learning_content(skill_id: str):
    """Get learning content for a skill"""
    skill = get_skill_by_id(skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    learning_file = LEARNING_DIR / f"{skill_id}.md"
    if not learning_file.exists():
        raise HTTPException(status_code=404, detail="Learning content not yet available")

    return learning_file.read_text(encoding="utf-8")


@app.get("/api/stats")
def get_stats():
    """Get summary statistics"""
    progress = db.get_user_progress()
    branches = load_skills()

    # Calculate per-branch stats
    branch_stats = {}
    for branch in branches:
        branch_xp = sum(
            progress.skills.get(s.id, SkillProgress(skill_id=s.id)).current_xp
            for s in branch.skills
        )
        completed = sum(
            1 for s in branch.skills
            if progress.skills.get(s.id, SkillProgress(skill_id=s.id)).level == SkillLevel.COMPLETED
        )
        branch_stats[branch.id] = {
            "name": branch.name,
            "total_skills": len(branch.skills),
            "completed_skills": completed,
            "total_xp": branch_xp
        }

    return {
        "total_xp": progress.total_xp,
        "challenges_completed": progress.challenges_completed,
        "branches": branch_stats
    }


# Static files and frontend
@app.get("/")
def serve_dashboard():
    """Serve the main dashboard"""
    return FileResponse(STATIC_DIR / "index.html")


# Mount static files last
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
