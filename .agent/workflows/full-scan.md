---
description: Full job scan across all sources — LinkedIn + all target companies
---

// turbo-all

1. Read `config/companies.yaml` to load all target companies
2. Read `config/profile.yaml` to load user profile and target roles
3. Read `config/settings.yaml` for API tokens and search settings
4. For each company with `ats: greenhouse` or `ats: lever`, run the `ats-fetcher` skill scripts:
   - `python3 .agent/skills/ats-fetcher/scripts/greenhouse.py --company {ats_id} --role "Product Manager" --json`
   - `python3 .agent/skills/ats-fetcher/scripts/lever.py --company {ats_id} --role "Product Manager" --json`
5. For each company with `ats: workday`, `ats: custom`, or any other type, use `career-page-searcher` skill via browser_subagent to navigate their careers_url and find PM roles
6. Use `linkedin-searcher` skill via browser_subagent to search LinkedIn for Product Manager roles (follow anti-detection rules from search-strategies.md)
7. Combine all results and deduplicate by matching job title + company + URL
8. For each new (unseen) job, use the `relevancy-scorer` skill to score against user profile
9. Push all jobs scoring above threshold (from settings.yaml `min_score_threshold`) to Notion using `notion-publisher` skill scripts:
   - `python3 .agent/skills/notion-publisher/scripts/push_jobs.py --token {notion_token} --db-id {job_pipeline_db_id} --jobs scored_jobs.json`
10. Print summary: "Scanned X companies, found Y new jobs, Z pushed to Notion"
