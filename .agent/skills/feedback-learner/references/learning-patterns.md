# Feedback Learning Patterns

## How Patterns Are Detected

### From Approved Jobs (✅ Applied)
The system looks for commonalities across approved jobs:
- Company characteristics (stage, size, industry)
- Role type (IC vs management, strategy vs execution)
- Technology/domain mentions
- Team structure clues
- Growth signals (funding, headcount growth)

### From Rejected Jobs (❌ Rejected)
The system identifies red flags from rejected jobs:
- Mismatched seniority (too junior/too senior)
- Undesirable domains
- Excessive travel/on-site requirements
- Roles that are PM in title but not in practice

### From User Comments (Richest Signal)
User's written comments are weighted highest because they explicitly state reasoning:
- "Too operations-heavy" → Create rule: penalize ops-focused roles
- "Love the company but role is junior" → Company is interesting at senior level
- "Perfect AI + PM fit" → Boost AI-domain PM roles significantly

## Deduplication Strategy

1. **Exact match**: Skip if an identical learning already exists
2. **Semantic match (>80% overlap)**: Keep the more specific version
3. **Contradiction**: Newer insight overrides older one
4. **Merge opportunity**: Combine related learnings into one
5. **Max entries**: Keep ≤20 per section to maintain context efficiency
