# Notion Job Pipeline — Database Schema

## Properties

| Property | Notion Type | Description | Values/Format |
|----------|-------------|-------------|---------------|
| **Job Title** | Title | Role name | Text |
| **Company** | Select | Company from target list | Auto-populated from companies |
| **Match Score** | Number | Relevancy score (0-100) | Integer, format: number |
| **Verdict** | Select | Match quality label | `strong_match`, `good_match`, `worth_reviewing`, `weak_match`, `no_match` |
| **Location** | Rich Text | City, state, or "Remote" | Text |
| **Apply Link** | URL | Direct application URL | URL |
| **Match Reasons** | Rich Text | Why this job fits the profile | Multi-line text |
| **Gaps** | Rich Text | Skills/experience gaps | Multi-line text |
| **Source** | Select | Where the job was found | `linkedin`, `greenhouse`, `lever`, `career_page` |
| **Date Found** | Date | When the agent discovered it | ISO date |
| **Posted Date** | Date | When the job was posted | ISO date (if available) |
| **Status** | Select | User's review status | `🆕 New`, `👀 Reviewed`, `✅ Applied`, `❌ Rejected`, `⏸️ Saved` |
| **User Comment** | Rich Text | **User's reason for approval/rejection** | Free text — read by feedback-learner |
| **Description Snippet** | Rich Text | First 300 chars of JD | Text |
| **Department** | Select | Team/department | e.g., "Product", "Engineering" |
| **Action** | Select | Recommended action | `apply_now`, `review`, `skip` |

## Relation

- **Job Pipeline ↔ Target Companies**: Linked via "Job Pipeline" relation in the Target Companies DB

## Views (Suggested)

1. **All Jobs** — Default table view, sorted by Date Found desc
2. **Strong Matches** — Filtered: Verdict = strong_match or good_match
3. **Needs Review** — Filtered: Status = 🆕 New
4. **Applied** — Filtered: Status = ✅ Applied
5. **By Company** — Grouped by Company
