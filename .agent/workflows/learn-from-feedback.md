---
description: Read user feedback from Notion and improve job scoring accuracy
---

1. Read `config/settings.yaml` for Notion token and Job Pipeline DB ID
2. Run the feedback-learner skill:
   - Query Notion for jobs with status "✅ Applied" or "❌ Rejected"
   - Extract both the status AND the "User Comment" field for each reviewed job
   - Also extract job title, company, and description for context
3. Read current learnings from `.agent/skills/relevancy-scorer/references/user-learnings.md`
4. Analyze patterns using LLM:
   - Identify new preference patterns from approved vs rejected jobs
   - Pay special attention to user's written comments (richest signal)
   - Compare against existing learnings — do NOT create duplicates
   - Merge similar patterns, update contradicted ones
5. Update `.agent/skills/relevancy-scorer/references/user-learnings.md` with refined learnings
6. Print summary: "Analyzed X reviewed jobs, learned Y new patterns, updated Z existing ones"
