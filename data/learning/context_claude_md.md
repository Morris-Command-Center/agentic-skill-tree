# CLAUDE.md Basics

## What Is It?
CLAUDE.md is a file in your project root that gives Claude context about your project. It's read automatically at the start of every session.

## Why It Matters
Without it, Claude starts every session blind. With a good CLAUDE.md, Claude:
- Knows your tech stack without asking
- Understands your project structure
- Follows your coding conventions
- Runs the right commands

## The Golden Rule
**Keep it under 500 tokens.** Every token in CLAUDE.md is loaded every turn. Bloated CLAUDE.md = wasted context = worse results.

---

## What To Include

### Must Have
```markdown
# Project Name

Brief one-liner about what this is.

## Quick Start
npm install && npm run dev

## Tech Stack
- Next.js 14 (App Router)
- TypeScript
- Prisma + PostgreSQL

## Key Commands
- `npm test` - run tests
- `npm run build` - production build
```

### Good To Have
```markdown
## Project Structure
- src/app/ - Next.js pages
- src/lib/ - shared utilities
- prisma/ - database schema

## Conventions
- Use named exports
- Tests go next to source files (*.test.ts)
```

### Don't Include
- Tutorials or explanations of standard tools
- Lengthy documentation
- Things Claude can figure out from the code
- Copy-pasted README content

---

## Good Example vs Bad Example

### Bad CLAUDE.md (800+ tokens)
```markdown
# My Project

This is a web application built with Next.js. Next.js is a React framework
that enables server-side rendering and static site generation...

## Getting Started

First, make sure you have Node.js installed. You can download it from
nodejs.org. We recommend using nvm to manage Node versions...

## Available Scripts

In the project directory, you can run:

### `npm start`
Runs the app in development mode. Open http://localhost:3000 to view it...

### `npm test`
Launches the test runner in interactive watch mode. See the section about
running tests for more information...
```

**Problems:**
- Explains what Next.js is (Claude knows)
- Includes Node.js installation instructions
- Copy-pasted from create-react-app README

### Good CLAUDE.md (150 tokens)
```markdown
# TaskFlow

ADHD-friendly task management app.

## Commands
- `npm run dev` - start dev server (port 3000)
- `npm test` - jest tests
- `npm run db:push` - push prisma schema

## Stack
Next.js 14 (App Router), TypeScript, Prisma, PostgreSQL

## Conventions
- Server components by default, 'use client' only when needed
- Zod for all validation
- Tests: *.test.ts next to source
```

**Why it works:**
- Project-specific info only
- Commands Claude will actually need
- Conventions that differ from defaults

---

## Common Mistakes

1. **Too long** - If it's over 500 tokens, you're wasting context
2. **Generic content** - Don't explain what npm is
3. **Stale info** - Update when your stack changes
4. **Missing commands** - Claude will guess wrong
5. **No structure hints** - Where do tests go? Components?

---

## Quick Checklist

Before saving your CLAUDE.md:
- [ ] Under 500 tokens?
- [ ] Would a senior dev need this info?
- [ ] Are the commands correct and current?
- [ ] Did you remove generic explanations?
- [ ] Is the structure section actually helpful?

---

## Exercise

Pick one of your projects and audit its CLAUDE.md:
1. Count the tokens (paste into Claude and ask)
2. Remove anything generic
3. Add any missing commands
4. Verify the commands actually work
