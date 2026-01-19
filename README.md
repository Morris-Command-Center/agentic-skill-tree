# Agentic Coding Skill Tree

A gamified progression system for mastering agentic coding workflows with Claude Code.

## Concept

Track your skills, complete challenges, and watch your skill tree light up as you level up your agentic coding abilities.

## Skill Branches

- **Context Engineering** - CLAUDE.md, project structure, context management
- **Prompt Design** - Task framing, constraints, output control
- **Tool Selection** - Read/Grep/Glob, when to use agents, parallel calls
- **Agent Orchestration** - Task decomposition, background agents, handoffs
- **Debugging** - Recognizing failures, recovery strategies, prevention

## Quick Start

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn src.main:app --reload

# Open http://localhost:8000
```

## Structure

```
├── src/
│   ├── main.py        # FastAPI app
│   ├── models.py      # Data models
│   ├── database.py    # SQLite operations
│   └── routes.py      # API routes
├── data/
│   ├── skills.yaml    # Skill tree definitions
│   └── challenges.yaml # Challenge definitions
├── static/
│   └── index.html     # Dashboard
└── progress.db        # SQLite database (gitignored)
```
