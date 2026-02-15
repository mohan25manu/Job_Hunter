---
name: feedback-learner
description: |
  Self-improvement engine that learns from user feedback in Notion.
  # TRIGGER SCENARIOS
  - User has reviewed/rated jobs in the Notion Job Pipeline DB
  - Periodic learning updates to improve scoring accuracy
  - User says "learn from my feedback" or "update preferences"
  Reads both status (✅/❌) AND written comments from Notion.
  Deduplicates learnings to keep the file lean.
---

# Feedback Learner

Reads user feedback (status changes + written comments) from the Notion Job Pipeline DB, distills patterns, and updates the relevancy-scorer's `user-learnings.md`.

## Learning Workflow

1. **Fetch**: Read Job Pipeline DB from Notion, filter for jobs with status "✅ Applied" or "❌ Rejected"
2. **Extract**: For each reviewed job, pull:
   - Job title, company, description
   - User's status (applied/rejected)
   - **User's written comment** from the "User Comment" field — this is the richest signal
3. **Analyze**: Send to LLM with existing learnings for pattern analysis
4. **Deduplicate**: LLM must compare new insights against existing `user-learnings.md` entries
   - Do NOT create duplicate or near-duplicate entries
   - Merge similar patterns into consolidated statements
   - Remove contradicted old learnings if user preferences have shifted
5. **Update**: Write refined `user-learnings.md` back to `relevancy-scorer/references/`

## LLM Analysis Prompt

```
You are analyzing a job seeker's feedback to learn their preferences.

EXISTING LEARNINGS:
{current_user_learnings_md}

RECENTLY REVIEWED JOBS:

Approved (✅ Applied):
{approved_jobs_with_comments}

Rejected (❌ Rejected):
{rejected_jobs_with_comments}

Instructions:
1. Identify NEW patterns from the recent reviews
2. Pay special attention to user's WRITTEN COMMENTS — they explain WHY
3. Compare against existing learnings — do NOT create duplicates
4. If a new pattern contradicts an old one, update the old entry
5. Merge similar patterns into consolidated statements
6. Keep entries concise and actionable

Return the COMPLETE updated user-learnings.md file content.
```

## User Comment Examples

The system specifically reads the "User Comment" property from Notion:
- "Too operations-heavy, I want strategy roles" → Learn: avoid ops-focused PM roles
- "Love this company culture but role is too junior" → Learn: this company is interesting, but needs senior roles
- "Exactly what I'm looking for — AI + PM intersection" → Learn: prioritize AI-domain PM roles

## Deduplication Rules

- Same insight expressed differently → Keep the more specific version
- Contradicting old and new → Keep the newer one (user preferences evolve)
- Threshold: If >80% semantic overlap with existing entry, skip
- Maximum entries per section: ~20 (to keep context window lean)

## Output

Updates the file at: `.agent/skills/relevancy-scorer/references/user-learnings.md`
