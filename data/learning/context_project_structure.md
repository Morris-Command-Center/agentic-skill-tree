# Project Structure for Agents

## Why Structure Matters
Agents navigate your codebase by searching and reading files. Poor structure = more turns = more tokens = worse results.

A well-structured project lets Claude:
- Find things on the first try
- Understand relationships between files
- Make changes without breaking things

---

## Principles

### 1. Predictable Naming
If Claude can guess where something is, it doesn't need to search.

**Bad:**
```
src/
  utils.ts          # What kind of utils?
  helpers.ts        # How is this different from utils?
  stuff.ts          # ???
  misc/
    things.ts
```

**Good:**
```
src/
  lib/
    validation.ts   # Zod schemas
    formatting.ts   # Date/number formatters
    api-client.ts   # HTTP client wrapper
```

### 2. Colocate Related Files
Keep things that change together near each other.

**Bad:**
```
components/
  UserCard.tsx
  ProductCard.tsx
tests/
  components/
    UserCard.test.tsx
    ProductCard.test.tsx
styles/
  UserCard.css
  ProductCard.css
```

**Good:**
```
components/
  UserCard/
    UserCard.tsx
    UserCard.test.tsx
    UserCard.css
    index.ts
  ProductCard/
    ProductCard.tsx
    ProductCard.test.tsx
    ProductCard.css
    index.ts
```

### 3. Flat Over Nested
Deep nesting makes searching harder.

**Bad:**
```
src/features/user/components/profile/sections/header/Avatar.tsx
```

**Good:**
```
src/components/user/ProfileAvatar.tsx
```

### 4. Index Files for Public APIs
Control what's exported from a directory.

```typescript
// components/index.ts
export { UserCard } from './UserCard';
export { ProductCard } from './ProductCard';
// Don't export internal helpers
```

---

## Common Patterns

### Feature-Based (Recommended for larger apps)
```
src/
  features/
    auth/
      components/
      hooks/
      api.ts
      types.ts
    dashboard/
      components/
      hooks/
      api.ts
      types.ts
  shared/
    components/
    hooks/
    lib/
```

### Layer-Based (Simpler apps)
```
src/
  components/
  hooks/
  lib/
  pages/
  types/
```

### Domain-Driven
```
src/
  domain/
    user/
    product/
    order/
  infrastructure/
    database/
    api/
  presentation/
    web/
    api/
```

---

## What Claude Looks For

When Claude needs to find something, it typically:

1. **Globs for patterns**: `**/*.test.ts`, `**/user*.ts`
2. **Greps for content**: `function validateUser`, `class UserService`
3. **Reads package.json/config files** to understand the stack

Make these searches efficient:
- Consistent file naming (`.test.ts` not sometimes `.spec.ts`)
- Searchable function/class names
- Config in root or standard locations

---

## Anti-Patterns

### The Junk Drawer
```
src/
  utils/
    index.ts  # 2000 lines of random functions
```
**Fix:** Split by purpose: `validation.ts`, `formatting.ts`, etc.

### The Deep Nest
```
src/app/modules/core/shared/common/utils/helpers/string/format.ts
```
**Fix:** Flatten. `src/lib/string-format.ts`

### The Inconsistent Pattern
```
src/
  UserComponent.tsx
  product-component.tsx
  ORDER_COMPONENT.tsx
```
**Fix:** Pick one convention. Stick to it.

### The Hidden Dependency
```typescript
// Importing from deep internal paths
import { thing } from '../../components/Card/internal/helpers';
```
**Fix:** Export from index files. `import { thing } from '@/components/Card';`

---

## Quick Wins

1. **Add a structure section to CLAUDE.md** - Tell Claude where things are
2. **Use consistent naming** - `*.test.ts` everywhere, not mixed with `.spec.ts`
3. **Flatten unnecessary nesting** - If a folder has one file, reconsider
4. **Colocate tests** - Next to source, not in separate tree
5. **Index files** - Control public APIs

---

## Exercise

Look at one of your projects:
1. Can you guess where the tests are without searching?
2. Is there a "utils" junk drawer?
3. Are naming conventions consistent?
4. Could you flatten any deep nesting?
