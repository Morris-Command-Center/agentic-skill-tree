# Agentic Skill Tree - Roadmap

## Phase 1: Learning Content (Current)
Add teaching content to each skill so users actually learn, not just track.

### Per-Skill Learning Content
- Concept explanation (why this matters)
- Good vs bad example transcripts
- Common mistakes to avoid
- Quick reference checklist

### Implementation
- `data/learning/` directory with markdown per skill
- `/api/learn/{skill_id}` endpoint
- "Learn" tab in skill detail sidebar
- Quiz/checkpoint before marking skill complete (optional)

---

## Phase 2: Real-Time Session Integration

Integrate with claude-monitoring to provide live feedback during sessions.

### Data Flow
```
Claude Code → JSONL logs → ccusage → Skill Tree API → Dashboard
```

### Features
- Real-time token burn rate display
- Turn counter
- Tool usage breakdown (which tools you're calling)
- Contextual tips based on current activity

### Implementation
- New `/api/sessions` endpoint to receive session data
- WebSocket or polling for live updates
- Integration with `post-session.sh` hook
- Session history view in dashboard

---

## Phase 3: Auto-Detection & Suggestions

Automatically detect when challenges are completed based on session patterns.

### Pattern Detection
- Token efficiency vs historical average
- Tool usage patterns (parallel calls, agent types)
- Turn count for task complexity
- Session duration

### Auto-Suggestions
- "That looked like 'One-Shot Wonder' - mark complete?"
- "You used 3 Explore agents in parallel - 'Multi-Agent Research'?"
- Efficiency scoring: "Completed in 45k tokens (top 20%)"

### Implementation
- Session pattern analyzer
- Challenge matcher (session → potential challenges)
- Notification system for suggestions
- Accept/reject flow for auto-completions

---

## Phase 4: Contextual Coaching

Real-time nudges and post-session review.

### Real-Time Nudges
- Token threshold warnings ("You're at 80k - consider /compact")
- Pattern alerts ("You've searched 5 times - maybe read the file?")
- Skill-relevant tips surfaced at the right moment

### Post-Session Review
- Transcript analysis
- "Turn 7 was inefficient - here's a better approach"
- Efficiency score breakdown
- Suggested skills to focus on

### Implementation
- Rules engine for nudge triggers
- Transcript parser for post-session analysis
- Review UI with annotated transcript view

---

## Phase 5: MCP Server Integration

The dream: Claude Code reports directly to skill tree.

### MCP Server Features
- Expose skill tree data to Claude Code
- Receive session events in real-time
- Allow Claude to query your skill levels
- Contextual tips injected into Claude's context

### Use Cases
- Claude knows your weak areas, adjusts guidance
- Auto-logs challenge completions as you work
- "You're practicing Tool Selection - here's a tip..."

### Implementation
- MCP server in Python (FastMCP or custom)
- Bidirectional: read skills, write progress
- Hook into Claude Code's MCP config

---

## Technical Debt / Nice-to-Haves

- [ ] Dark/light mode toggle
- [ ] Export progress to JSON
- [ ] Import progress from backup
- [ ] Mobile-responsive dashboard
- [ ] Streak tracking (consecutive days)
- [ ] Skill decay (fade if not practiced)
- [ ] Community challenges (shared transcripts)
