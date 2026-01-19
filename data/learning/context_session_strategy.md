# Session Strategy

## The Core Question
When should you:
- Continue the current session?
- Compact and continue?
- Start completely fresh?

Getting this wrong wastes tokens or loses important context.

---

## Decision Framework

### Continue Current Session When:
- Working on the same feature/bug
- Building on decisions made earlier
- Claude has context you'd have to re-explain
- Under 70% context usage

### Compact and Continue When:
- Same project, but pivoting to different area
- Conversation is long but you need some history
- Context is 70-85% full
- You want to preserve key decisions but lose the noise

### Start Fresh When:
- Completely different project
- Unrelated task (research vs coding vs debugging)
- Context is polluted with wrong approaches
- You've been going in circles
- New day, new work

---

## The Handoff Document Pattern

For complex multi-session work, create a handoff document.

### When to Use
- Feature spans multiple sessions
- You need to pause and resume later
- Multiple people working on same thing

### What to Include
```markdown
# Feature: User Authentication

## Status
- [x] JWT implementation
- [x] Login endpoint
- [ ] Refresh token flow
- [ ] Logout

## Key Decisions
- Using RS256 for JWT signing
- Tokens expire in 15 minutes
- Refresh tokens stored in httpOnly cookies

## Current Blockers
- Need to decide on Redis vs PostgreSQL for session storage

## Next Steps
1. Implement refresh token endpoint
2. Add logout that invalidates refresh token
3. Write integration tests

## Files Modified
- src/features/auth/jwt.ts
- src/features/auth/login.ts
- prisma/schema.prisma (added RefreshToken model)
```

### How to Use
1. At end of session: "Create a handoff document for this work"
2. Save it (or let Claude save it)
3. Next session: "Read the handoff doc at docs/auth-handoff.md and continue"

---

## Session Types

### The Exploration Session
**Goal:** Understand something
**Pattern:** Lots of reading, searching, questions
**When to end:** When you have answers
**Compact:** Rarely needed (short sessions)

### The Implementation Session
**Goal:** Build something
**Pattern:** Read → Plan → Code → Test → Iterate
**When to end:** Feature complete or stuck
**Compact:** At 70% or when switching sub-tasks

### The Debugging Session
**Goal:** Fix something
**Pattern:** Reproduce → Investigate → Hypothesize → Test → Fix
**When to end:** Bug fixed or need fresh eyes
**Compact:** When investigation is done, before fixing

### The Refactoring Session
**Goal:** Improve existing code
**Pattern:** Understand → Plan → Change → Verify
**When to end:** Refactor complete
**Compact:** Between major changes

---

## Anti-Patterns

### The Marathon Session
8-hour session with 200 turns. Context is garbage by the end.

**Fix:** Take breaks. Start fresh after lunch.

### The Context Hoarder
Never compacts because "what if I need that?"

**Fix:** Trust the compaction. Key info survives.

### The Fresh Start Addict
New session every 15 minutes because "clean slate."

**Fix:** Let context build. It helps.

### The Wrong Session Type
Exploring in an implementation session. Debugging during refactoring.

**Fix:** Recognize the mode you're in. Switch sessions if needed.

---

## Practical Tips

### Morning Routine
1. Start fresh session
2. State your goal for the day
3. Reference any handoff docs

### Before Lunch
1. Check context usage
2. Compact or note where you are
3. Consider if afternoon is same task

### End of Day
1. Create handoff if work continues tomorrow
2. Note any decisions made
3. Don't leave mid-bug

### When Stuck
If you've been going in circles for 30+ minutes:
1. Stop
2. Write down what you've tried
3. Start fresh session
4. Explain the problem cleanly

Fresh context often breaks logjams.

---

## Quick Reference

| Situation | Action |
|-----------|--------|
| Same feature, <70% context | Continue |
| Same feature, >70% context | Compact |
| Different feature, same project | Consider fresh |
| Different project | Fresh session |
| Going in circles | Fresh + clean problem statement |
| Multi-day work | Handoff document |
| After a break | Read context, decide fresh vs continue |

---

## Exercise

For your next week of Claude Code usage:
1. Note when you start/end sessions
2. Track why you made that choice
3. Notice when you wish you had more/less context
4. Experiment with handoff documents
