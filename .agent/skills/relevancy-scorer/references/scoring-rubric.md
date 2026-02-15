# Scoring Rubric

## Dimensions and Weights

### 1. Role Fit (30%)
- Does the job title match user's target roles?
- Are the responsibilities aligned with PM work (strategy, roadmap, execution)?
- Is it a true PM role or disguised project/program management?
- Score: 0 (completely wrong role) → 100 (perfect title + responsibilities match)

### 2. Skills Match (25%)
- Does the job require skills the user has?
- Are "must-have" vs "nice-to-have" requirements met?
- Technical skills alignment (SQL, data analysis, APIs, etc.)
- Soft skills alignment (stakeholder management, cross-functional leadership)
- Score: 0 (no overlap) → 100 (user meets or exceeds every requirement)

### 3. Seniority Fit (15%)
- Does the experience level match user's years of experience?
- Is the title seniority appropriate? (IC5/IC6/Manager/Director)
- Does the scope match user's career trajectory?
- Score: 0 (wildly mismatched) → 100 (perfect seniority alignment)

### 4. Domain Relevance (10%)
- Does the company's industry match user's domain experience?
- Is the product area interesting/relevant?
- Boost if matches user-learnings.md preferred domains
- Penalize if matches rejected domains
- Score: 0 (completely irrelevant domain) → 100 (exact domain match)

### 5. Location/Remote (10%)
- Does the work arrangement match preferences?
- Remote-first companies get a bonus if user prefers remote
- On-site only gets penalized if user wants remote
- Score: 0 (incompatible arrangement) → 100 (perfect match)

### 6. Learned Preferences (10%)
- Boost: matches patterns from approved jobs in user-learnings.md
- Penalize: matches patterns from rejected jobs
- Weight user's explicit comments heavily
- Score: 0 (matches all rejection patterns) → 100 (matches all approval patterns)

## Final Score Calculation

```
final_score = (role_fit × 0.30) + (skills_match × 0.25) + (seniority × 0.15) +
              (domain × 0.10) + (location × 0.10) + (learned_prefs × 0.10)
```

## Verdict Mapping

| Score Range | Verdict | Action |
|-------------|---------|--------|
| 80-100 | strong_match | apply_now |
| 60-79 | good_match | review |
| 40-59 | worth_reviewing | review |
| 20-39 | weak_match | skip |
| 0-19 | no_match | skip |
