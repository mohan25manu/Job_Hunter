# Skill Routing Logic

## ATS Type → Skill Mapping

| ATS Type in companies.yaml | Skill to Use | Method |
|----------------------------|-------------|--------|
| `greenhouse` | `ats-fetcher` | `scripts/greenhouse.py` — JSON API |
| `lever` | `ats-fetcher` | `scripts/lever.py` — JSON API |
| `ashby` | `ats-fetcher` | `scripts/ashby.py` — JSON API |
| `workday` | `career-page-searcher` | browser_subagent |
| `icims` | `career-page-searcher` | browser_subagent |
| `taleo` | `career-page-searcher` | browser_subagent |
| `custom` | `career-page-searcher` | browser_subagent |

## Special Routes

- **LinkedIn**: Always dispatched to `linkedin-searcher` regardless of companies
- **Unknown ATS**: Default to `career-page-searcher` (browser agent works anywhere)

## Routing Decision Flow

```
for company in companies.yaml:
    if company.ats in ["greenhouse", "lever", "ashby"]:
        → ats-fetcher(company.ats_id, company.ats)
    else:
        → career-page-searcher(company.careers_url)

always:
    → linkedin-searcher(target_roles from profile.yaml)
```
