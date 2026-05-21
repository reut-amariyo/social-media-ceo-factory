# ✅ Validator Agent — Gatekeeper

## What it does

The Validator is the quality control agent. It runs **two-phase validation** on every draft and either PASSES or FAILS them. Failed drafts get sent back to the Creator with specific feedback (up to 3 retries).

## Two-phase validation

### Phase 1: Hard Rules (Instant, Deterministic)

Fast regex/string checks that catch obvious violations:

| Check | What it catches |
|-------|----------------|
| **Platform length** | X post > 280 chars, LinkedIn too short |
| **Banned words** | Any word from your `banned_words` list |
| **Punctuation** | Em dashes (—), double dashes (--), curly quotes |
| **Condescension patterns** | "Here's what most people miss", "Let me explain" |
| **Numbered lists** | Lists with more than 3 items (violates Rule of 3) |
| **Missing platforms** | If X, LinkedIn, or Instagram draft is empty |

### Phase 2: Deep LLM Evaluation (Intelligent)

An LLM evaluates what only a human-like judge can:

| Score | What it measures |
|-------|-----------------|
| **The Authenticity Test** | Could ONLY you write this? (1-5) |
| **Eye-Level Tone** | No guru energy, no looking down? (1-5) |
| **Hook Strength** | Would someone stop scrolling? (1-5) |
| **Voice Accuracy** | Matches your writing patterns? (1-5) |
| **ICP Fit** | Does your target audience care? (1-5) |
| **Engagement Potential** | Will people comment/share? (1-5) |
| **Specificity** | Real numbers, real stories, not vague? (1-5) |

## Pass/Fail logic

- **PASS:** Average score ≥ 3.5 AND zero hard-rule violations
- **FAIL:** Returns specific, actionable feedback to the Creator

## Retry loop

```
Creator → Validator → FAIL → Creator (with feedback) → Validator → FAIL → Creator → Validator → PASS or give up
```

Max 3 attempts. After 3 failures, proceeds with the best available draft.

## How it uses your profile

- **`banned_words`** → Phase 1 hard-rule check
- **`tone`** → Phase 2 voice evaluation
- **`name`** → The Authenticity Test ("Could only [name] write this?")
