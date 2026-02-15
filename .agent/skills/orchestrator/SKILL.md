---
name: orchestrator
description: |
  Master job search coordinator for JobPilot.
  # TRIGGER SCENARIOS
  - User requests a job scan, job search, or job refresh
  - User says "find jobs", "scan companies", "check for new roles"
  - Any multi-step job hunting workflow needs coordination
  Breaks tasks into subtasks and routes to specialized skills:
  linkedin-searcher, career-page-searcher, ats-fetcher, relevancy-scorer, notion-publisher.
---

# Orchestrator

Coordinates the entire job search pipeline by reading company configs and dispatching to the right skill.

## Workflow

1. **Load Config**: Read `config/companies.yaml` for target companies and `config/profile.yaml` for user preferences
2. **Route Companies**: For each company, route based on `ats` field:
   - `ats: greenhouse` or `ats: lever` or `ats: ashby` → `ats-fetcher` skill
   - `ats: workday` or `ats: custom` or any other → `career-page-searcher` skill
3. **Search LinkedIn**: Dispatch `linkedin-searcher` for broad PM role discovery
4. **Dedup**: Check all collected jobs against `data/jobs.db` — skip already-seen jobs
5. **Score**: Pass new jobs to `relevancy-scorer` skill
6. **Publish**: Pass scored jobs (above threshold) to `notion-publisher` skill

## Task Decomposition Rules

- Company counts are NEVER hardcoded — always read dynamically from `companies.yaml`
- Each company routes based on its `ats` field, not assumptions
- LinkedIn is always searched as a separate task regardless of company list
- A company can be added or removed from `companies.yaml` at any time

## Skill Routing

See [references/skill-routing.md](references/skill-routing.md) for detailed routing logic.

## Deduplication

Before scoring, check `data/jobs.db` for existing entries by matching:
- Job title + company name + location (fuzzy match)
- Direct URL match
Only new/unseen jobs proceed to scoring.

## Error Handling

- If a skill fails for one company, log the error and continue with remaining companies
- Never let one failed source block the entire pipeline
- Report summary at end: "Scanned X companies, found Y new jobs, Z scored above threshold"
