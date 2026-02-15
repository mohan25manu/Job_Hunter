---
description: Quick check of top priority companies only (fast scan)
---

1. Read `config/companies.yaml` — filter for companies with `ats: greenhouse` or `ats: lever` only (API-accessible, fast)
2. Read `config/profile.yaml` for target roles
3. Run ats-fetcher scripts for each API-accessible company:
   - Greenhouse: `python3 .agent/skills/ats-fetcher/scripts/greenhouse.py --company {ats_id} --role "Product Manager" --json`
   - Lever: `python3 .agent/skills/ats-fetcher/scripts/lever.py --company {ats_id} --role "Product Manager" --json`
// turbo
4. Deduplicate results against previously seen jobs
5. Score new jobs with relevancy-scorer
6. Push high-scoring jobs to Notion
7. Print summary
