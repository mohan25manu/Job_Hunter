# JobPilot

An AI-powered job hunting system built on Antigravity agent skills.

## What It Does

Scans LinkedIn, company career pages, and ATS boards for Product Manager roles,
scores them against user profile using LLM-based relevancy analysis, and publishes
curated results to a Notion database. Self-improves by learning from user feedback.

## Project Layout

| Directory | Purpose |
|-----------|---------|
| `config/` | User profile, target companies, API keys, settings |
| `config/resume/` | User's resume file(s) for profile extraction |
| `.agent/skills/` | Modular agent skills (see below) |
| `.agent/workflows/` | Pre-defined task workflows |
| `data/` | SQLite database for deduplication and job history |

## Agent Skills

| Skill | Type | Purpose |
|-------|------|---------|
| `orchestrator` | workflow | Breaks tasks, reads companies config, dispatches to search/score/publish skills |
| `linkedin-searcher` | tool | Browser agent for LinkedIn job search with anti-detection |
| `career-page-searcher` | tool | Browser agent for any company career page |
| `ats-fetcher` | tool | Direct API for Greenhouse/Lever/Ashby JSON endpoints |
| `relevancy-scorer` | tool | LLM-based job scoring using profile + learned preferences |
| `notion-publisher` | tool | Creates/manages Notion job tracker DB and pushes scored jobs |
| `feedback-learner` | knowledge | Reads user feedback (status + comments) from Notion, deduplicates learnings |

## How a Run Works

1. User triggers a scan (manual or scheduled)
2. `orchestrator` reads `config/companies.yaml`, routes each company to the right search skill
3. `linkedin-searcher` searches LinkedIn for PM roles (with human-like behavior)
4. `career-page-searcher` navigates custom career pages
5. `ats-fetcher` calls public JSON APIs (Greenhouse/Lever) for companies that have them
6. All results are deduplicated against `data/jobs.db` (7-day window — jobs seen 7+ days ago are refreshed)
7. `relevancy-scorer` scores each new job using user profile + `user-learnings.md`
8. `notion-publisher` pushes high-scoring jobs to the Notion Job Pipeline DB

## Key Data Sources

- **Notion Target Companies DB**: `2d8e7ff25f4180209169d408961ec86d` (28 companies)
- **Notion Parent Page**: `2d6e7ff25f418097a85df8ccbabe4ae0` (2026 workspace)

## LLM

Uses Claude (via Antigravity) for relevancy scoring — no separate API key needed.
For automated/scheduled runs, can optionally use OpenAI GPT-4o-mini.
