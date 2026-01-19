import sqlite3
import json
from pathlib import Path
from datetime import datetime
from typing import Optional

from .models import (
    SkillProgress, SkillLevel, Confidence,
    ChallengeCompletion, UserProgress
)

DB_PATH = Path(__file__).parent.parent / "progress.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database tables"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS skill_progress (
            skill_id TEXT PRIMARY KEY,
            current_xp INTEGER DEFAULT 0,
            level TEXT DEFAULT 'locked',
            confidence TEXT DEFAULT 'red',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS challenge_completions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            challenge_id TEXT NOT NULL,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            xp_earned INTEGER NOT NULL,
            notes TEXT DEFAULT '',
            self_rating INTEGER NOT NULL,
            confidence TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS achievements (
            achievement_id TEXT PRIMARY KEY,
            unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def get_skill_progress(skill_id: str) -> Optional[SkillProgress]:
    """Get progress for a specific skill"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM skill_progress WHERE skill_id = ?",
        (skill_id,)
    )
    row = cursor.fetchone()
    conn.close()

    if row:
        return SkillProgress(
            skill_id=row["skill_id"],
            current_xp=row["current_xp"],
            level=SkillLevel(row["level"]),
            confidence=Confidence(row["confidence"])
        )
    return None


def get_all_skill_progress() -> dict[str, SkillProgress]:
    """Get progress for all skills"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM skill_progress")
    rows = cursor.fetchall()
    conn.close()

    return {
        row["skill_id"]: SkillProgress(
            skill_id=row["skill_id"],
            current_xp=row["current_xp"],
            level=SkillLevel(row["level"]),
            confidence=Confidence(row["confidence"])
        )
        for row in rows
    }


def update_skill_progress(progress: SkillProgress):
    """Update or create skill progress"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO skill_progress (skill_id, current_xp, level, confidence, updated_at)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(skill_id) DO UPDATE SET
            current_xp = excluded.current_xp,
            level = excluded.level,
            confidence = excluded.confidence,
            updated_at = excluded.updated_at
    """, (
        progress.skill_id,
        progress.current_xp,
        progress.level.value,
        progress.confidence.value,
        datetime.now()
    ))

    conn.commit()
    conn.close()


def add_challenge_completion(completion: ChallengeCompletion) -> int:
    """Record a challenge completion"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO challenge_completions
        (challenge_id, completed_at, xp_earned, notes, self_rating, confidence)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        completion.challenge_id,
        completion.completed_at,
        completion.xp_earned,
        completion.notes,
        completion.self_rating,
        completion.confidence.value if completion.confidence else None
    ))

    completion_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return completion_id


def get_challenge_completions(challenge_id: Optional[str] = None) -> list[ChallengeCompletion]:
    """Get challenge completions, optionally filtered by challenge"""
    conn = get_connection()
    cursor = conn.cursor()

    if challenge_id:
        cursor.execute(
            "SELECT * FROM challenge_completions WHERE challenge_id = ? ORDER BY completed_at DESC",
            (challenge_id,)
        )
    else:
        cursor.execute(
            "SELECT * FROM challenge_completions ORDER BY completed_at DESC"
        )

    rows = cursor.fetchall()
    conn.close()

    return [
        ChallengeCompletion(
            id=row["id"],
            challenge_id=row["challenge_id"],
            completed_at=datetime.fromisoformat(row["completed_at"]),
            xp_earned=row["xp_earned"],
            notes=row["notes"],
            self_rating=row["self_rating"],
            confidence=Confidence(row["confidence"]) if row["confidence"] else None
        )
        for row in rows
    ]


def get_total_xp() -> int:
    """Get total XP earned"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COALESCE(SUM(xp_earned), 0) as total FROM challenge_completions")
    result = cursor.fetchone()
    conn.close()

    return result["total"]


def get_user_progress() -> UserProgress:
    """Get complete user progress"""
    skills = get_all_skill_progress()
    completions = get_challenge_completions()

    return UserProgress(
        skills=skills,
        total_xp=get_total_xp(),
        challenges_completed=len(completions)
    )


def unlock_achievement(achievement_id: str):
    """Record an unlocked achievement"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO achievements (achievement_id, unlocked_at)
        VALUES (?, ?)
    """, (achievement_id, datetime.now()))

    conn.commit()
    conn.close()


def get_unlocked_achievements() -> list[str]:
    """Get list of unlocked achievement IDs"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT achievement_id FROM achievements")
    rows = cursor.fetchall()
    conn.close()

    return [row["achievement_id"] for row in rows]


# Initialize database on module load
init_db()
