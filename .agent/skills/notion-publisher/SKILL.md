---
name: notion-publisher
description: |
  Publishes scored job listings to a Notion database.
  # TRIGGER SCENARIOS
  - Pushing scored jobs to the Job Pipeline Notion DB
  - Creating the initial Job Pipeline database in Notion
  - Updating the Notion Target Companies table with careers URLs
  Manages the Notion DB schema, creates entries, and handles the Job Pipeline relation.
---

# Notion Publisher

Creates and manages the Job Pipeline database in Notion and pushes scored jobs to it.

## First Run — Database Creation

On first run (when `settings.yaml` has `job_pipeline_db_id: null`):

1. Create a new database "Job Pipeline" under the parent page
2. Set up the schema defined in [references/db-schema.md](references/db-schema.md)
3. Link it via "Job Pipeline" relation in the Target Companies DB
4. Store the new DB ID back in `settings.yaml`

Use `scripts/create_db.py` for database creation.

## Publishing Jobs

For each scored job above the threshold:

1. Check if the job already exists in Notion (by URL match)
2. Create a new page in Job Pipeline DB with all properties
3. Set status to "🆕 New"
4. Link to the company in Target Companies DB (if matched)

Use `scripts/push_jobs.py` for job publishing.

## Notion DB Schema

See [references/db-schema.md](references/db-schema.md) for full schema. Key properties:

| Property | Type | Description |
|----------|------|-------------|
| Job Title | Title | Role name |
| Company | Select | Company name |
| Match Score | Number | 0-100 from relevancy-scorer |
| Verdict | Select | strong_match / good_match / worth_reviewing |
| Location | Text | City or Remote |
| Apply Link | URL | Direct application URL |
| Match Reasons | Text | Why the job fits |
| Gaps | Text | What's missing |
| Source | Select | linkedin / greenhouse / career_page |
| Date Found | Date | When agent found it |
| Posted Date | Date | When job was posted |
| Status | Select | 🆕 New / 👀 Reviewed / ✅ Applied / ❌ Rejected |
| User Comment | Rich Text | **User writes rejection/approval reasons here** |

## API Configuration

- Token: from `config/settings.yaml`
- API Version: `2022-06-28`
- Parent page: from `settings.yaml` → `parent_page_id`
