---
name: linkedin-searcher
description: |
  Browser-based LinkedIn job search agent with human-like behavior.
  # TRIGGER SCENARIOS
  - Searching LinkedIn for Product Manager or similar roles
  - Discovering PM jobs from companies not in the target list
  - Broad job market scanning on LinkedIn
  Uses browser_subagent with anti-detection (random delays, natural scrolling).
---

# LinkedIn Searcher

Navigates LinkedIn job search using browser_subagent, mimicking human browsing behavior to avoid detection.

## Anti-Detection Rules (CRITICAL)

**Every browser interaction MUST follow these rules:**

1. **Random delays** between actions: 1-4 seconds (randomized, never constant)
2. **Natural scrolling**: Scroll gradually, pause to "read", never jump instantly
3. **Human-like clicks**: Wait 0.5-2s before clicking, don't click in rapid succession
4. **Reading pauses**: Pause 2-5 seconds when a job description loads (simulating reading)
5. **Randomized order**: If possible, vary the interaction sequence
6. **Page limit**: Maximum 3 pages of results per search session

## Search Workflow

```
1. Navigate to linkedin.com/jobs
2. Wait 2-4 seconds (random), scroll down slowly
3. Type search query: "{target_role}" (from profile.yaml)
4. Wait 1-3 seconds, apply filters:
   - Date Posted: Past 24 hours
   - Remote/Location: as configured
5. For each visible job listing (up to 25 per page):
   - Pause 1-2 seconds between jobs
   - Scroll to the job card naturally
   - Extract: title, company, location, link, posted date
   - If description is visible, extract key details
6. Paginate (up to max_pages from settings.yaml)
7. Return JSON array of all extracted jobs
```

## Output Format

Return a JSON array:
```json
[
  {
    "title": "Senior Product Manager",
    "company": "Stripe",
    "location": "Remote",
    "url": "https://linkedin.com/jobs/view/...",
    "posted_date": "1 day ago",
    "description_snippet": "First 200 chars of description...",
    "source": "linkedin"
  }
]
```

## Search Strategies

See [references/search-strategies.md](references/search-strategies.md) for query templates and filter combinations.
