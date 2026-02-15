---
name: ats-fetcher
description: |
  Fast API-based job fetcher for ATS platforms with public JSON endpoints.
  # TRIGGER SCENARIOS
  - Fetching jobs from companies using Greenhouse, Lever, or Ashby ATS
  - When a company's ats field is "greenhouse", "lever", or "ashby"
  Uses direct HTTP requests (no browser needed). Faster and cheaper than browser agents.
---

# ATS Fetcher

Fetches job listings from public ATS JSON APIs. No browser needed — uses simple HTTP requests.

## Supported Platforms

| ATS | Endpoint Pattern | Script |
|-----|-----------------|--------|
| Greenhouse | `https://boards.greenhouse.io/{ats_id}/jobs.json` | `scripts/greenhouse.py` |
| Lever | `https://api.lever.co/v0/postings/{ats_id}` | `scripts/lever.py` |
| Ashby | Via Ashby API | `scripts/ashby.py` (future) |

## Usage

```bash
# Fetch Greenhouse jobs for a company
python3 scripts/greenhouse.py --company figma --role "Product Manager"

# Fetch Lever jobs for a company
python3 scripts/lever.py --company flyzipline --role "Product Manager"
```

## Filtering Logic

After fetching all jobs from the API:
1. Filter by title containing any of: "Product Manager", "PM", "Head of Product", "Director of Product"
2. Exclude titles containing: "Engineering Manager", "Project Manager"
3. Return structured JSON matching the standard output format

## Output Format

```json
[
  {
    "title": "Senior Product Manager",
    "company": "Figma",
    "location": "San Francisco, CA",
    "url": "https://boards.greenhouse.io/figma/jobs/12345",
    "posted_date": "2026-02-14",
    "description_snippet": "...",
    "department": "Product",
    "source": "greenhouse"
  }
]
```
