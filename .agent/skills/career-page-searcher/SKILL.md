---
name: career-page-searcher
description: |
  Browser-based company career page navigator.
  # TRIGGER SCENARIOS
  - Navigating a company's careers page to find open PM roles
  - Companies using Workday, iCIMS, Taleo, or custom career pages
  - Any career page without a public JSON API
  Uses browser_subagent to visit the page, find relevant listings, and extract details.
---

# Career Page Searcher

Visits any company's careers page using browser_subagent, searches for Product Manager roles, and extracts listings.

## Workflow

```
1. Navigate to the company's careers_url (from companies.yaml)
2. Wait for page to load (3-5 seconds)
3. Look for a search/filter bar — enter "Product Manager" if available
4. If no search bar, browse department filters (look for "Product", "PM")
5. Scan visible listings for PM-related titles
6. For each relevant listing:
   - Extract: title, location, link, department, posted date (if visible)
   - Click into the listing if needed for full details
   - Extract description snippet (first 300 chars)
7. Return JSON array of all found PM roles
```

## Navigation Patterns

See [references/navigation-patterns.md](references/navigation-patterns.md) for common career page layouts.

## Adaptive Behavior

- If the careers page uses pagination, follow up to 3 pages
- If the page requires JavaScript rendering, wait for dynamic content
- If a jobs page has a "Product" department filter, use it
- If there are no filters, scan all visible listings for PM keywords
- Handle pop-ups (cookie banners, newsletter signups) by dismissing them

## Output Format

Same JSON format as linkedin-searcher:
```json
[
  {
    "title": "Product Manager, Platform",
    "company": "Google",
    "location": "Mountain View, CA",
    "url": "https://careers.google.com/jobs/...",
    "posted_date": "2 days ago",
    "description_snippet": "...",
    "source": "career_page"
  }
]
```
