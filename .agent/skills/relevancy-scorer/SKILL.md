---
name: relevancy-scorer
description: |
  LLM-powered job relevancy scoring with self-improving preferences.
  # TRIGGER SCENARIOS
  - Scoring a batch of raw job listings against user profile
  - Evaluating job-person fit using resume, preferences, and learned patterns
  Self-improving: reads user-learnings.md which evolves from feedback.
---

# Relevancy Scorer

Evaluates job listings against the user profile using LLM analysis. Reads both the static profile and the evolving user-learnings.md for personalized scoring.

## Scoring Workflow

1. Load `config/profile.yaml` for user profile and preferences
2. Load `config/resume/` for resume content (if available)
3. Load `references/user-learnings.md` for learned preferences
4. For each job in the batch:
   - Send job description + user profile + learnings to LLM
   - Get back structured score and analysis
5. Return scored jobs list

## Scoring Rubric

See [references/scoring-rubric.md](references/scoring-rubric.md) for the detailed scoring dimensions.

| Dimension | Weight | What It Measures |
|-----------|--------|-----------------|
| Role Fit | 30% | Title, responsibilities match target role |
| Skills Match | 25% | Required skills vs user's skills |
| Seniority | 15% | Experience level alignment |
| Domain | 10% | Industry/domain match |
| Location/Remote | 10% | Work arrangement match |
| Learned Preferences | 10% | Patterns from user-learnings.md |

## LLM Prompt Template

```
You are evaluating a job against a candidate profile.

CANDIDATE PROFILE:
{profile_yaml}

LEARNED PREFERENCES:
{user_learnings_md}

JOB:
Title: {title}
Company: {company}
Location: {location}
Description: {description}

Return JSON:
{
  "score": 0-100,
  "verdict": "strong_match" | "good_match" | "worth_reviewing" | "weak_match" | "no_match",
  "reasons": ["Why this is a good/bad fit", "..."],
  "gaps": ["What's missing", "..."],
  "action": "apply_now" | "review" | "skip"
}
```

## User Learnings Integration

The file `references/user-learnings.md` is read EVERY scoring run. It contains patterns learned from the user's Notion feedback. This file starts empty and evolves over time via the `feedback-learner` skill.
