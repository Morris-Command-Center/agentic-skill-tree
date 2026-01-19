# Context Window Management

## What Is the Context Window?
The context window is Claude's "working memory" - everything it can see at once:
- System prompt
- CLAUDE.md and project files
- Conversation history
- Tool results

Current limit: ~200k tokens. Sounds like a lot, but it fills up fast.

## Why It Matters
When context fills up:
- Claude forgets earlier conversation
- Responses get worse (too much noise)
- You hit token limits and get cut off
- Sessions become expensive

---

## What Consumes Context

### Typical Breakdown
```
System prompt + tools:     ~15k tokens (fixed)
CLAUDE.md + memory files:  ~2k tokens (per project)
Conversation history:      Variable (biggest consumer)
Tool results:              Variable (file reads, searches)
```

### The Sneaky Consumers
- **Large file reads**: Reading a 2000-line file = thousands of tokens
- **Verbose tool output**: Grep results, directory listings
- **Repeated information**: Asking about the same file multiple times
- **Long conversations**: Every message stays in context

---

## Monitoring Your Usage

### In-Session
```
/context
```
Shows current breakdown. Use it regularly.

### Watch For
- Message tokens > 50% of total = time to compact
- Large tool results you're not using
- Repeated file reads

---

## Strategies

### 1. Be Specific in Requests
**Bad:** "Read the user module"
```
Claude reads 15 files, 8000 tokens consumed
```

**Good:** "Read src/features/user/api.ts, specifically the createUser function"
```
Claude reads relevant section, 200 tokens consumed
```

### 2. Use Targeted Searches
**Bad:** "Find all error handling"
```
Grep returns 200 matches, 5000 tokens
```

**Good:** "Find error handling in the auth module"
```
Grep returns 12 matches, 300 tokens
```

### 3. Compact Proactively
Don't wait until you hit limits. Compact when:
- You're switching to a different task
- Context is above 70%
- Conversation has gone on for 20+ turns
- You notice Claude forgetting earlier context

```
/compact
```

### 4. Start Fresh for New Tasks
If the new task is unrelated to the current conversation, start a new session instead of continuing.

**Same session good for:**
- Follow-up questions
- Iterating on the same feature
- Debugging something you just built

**New session better for:**
- Different feature entirely
- Different project
- Research vs implementation

### 5. Summarize Before Compacting
If you have important context that must survive compaction:
```
"Before we compact, the key decisions were:
1. Using JWT for auth
2. Storing sessions in Redis
3. The bug was in validateToken()"
```

Then compact. The summary stays, the noise goes.

---

## Common Mistakes

### The Kitchen Sink Read
```
"Read all the files in src/"
```
Never do this. Be specific.

### The Infinite Conversation
Same session for 3 hours across multiple unrelated tasks. Context becomes noise.

### Ignoring the Warning Signs
- Claude repeating questions you already answered
- "As I mentioned earlier..." but it didn't mention it
- Responses getting less coherent

These mean context is full of noise. Compact or restart.

### Over-Compacting
Compacting loses nuance. Don't do it every 5 turns. Find the balance.

---

## Quick Reference

| Context % | Action |
|-----------|--------|
| < 50% | Keep going |
| 50-70% | Consider compacting soon |
| 70-85% | Compact after current task |
| > 85% | Compact now |

---

## Exercise

During your next Claude Code session:
1. Run `/context` at the start
2. Run it again after 10 turns
3. Note what consumed the most tokens
4. Practice compacting at 70%
