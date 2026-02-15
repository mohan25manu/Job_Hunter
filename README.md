# 🎯 JobPilot — AI-Powered Job Hunting Agent

An intelligent, self-improving job search agent built on the [Antigravity](https://antigravity.dev) agent skills pattern. Scans LinkedIn, company career pages, and ATS boards for Product Manager roles, scores them using LLM-based relevancy analysis, and publishes curated results to Notion.

## ✨ Features

- **7 Modular Agent Skills** — Each capability is a self-contained skill (search, score, publish, learn)
- **Multi-Source Job Discovery** — LinkedIn (browser agent), Greenhouse/Lever (API), any career page (browser agent)
- **LLM-Powered Scoring** — Evaluates jobs against your resume, preferences, and learned patterns
- **Self-Improving** — Learns from your Notion feedback (✅/❌ + written comments) to score better over time
- **Anti-Detection** — Human-like browsing behavior for LinkedIn with random delays and natural scrolling
- **Notion Integration** — Full Job Pipeline DB with match scores, reasons, gaps, and action recommendations

## 🏗️ Architecture

```
.agent/skills/
├── orchestrator/            → Task breaker & dispatcher
├── linkedin-searcher/       → Browser agent with anti-detection
├── career-page-searcher/    → Navigates any career page
├── ats-fetcher/             → Greenhouse/Lever JSON APIs
├── relevancy-scorer/        → LLM scoring with self-learning
├── notion-publisher/        → Notion DB management
└── feedback-learner/        → Reads Notion feedback → improves scoring
```

## 🚀 Quick Start

### 1. Clone & Configure

```bash
git clone https://github.com/yourusername/jobpilot.git
cd jobpilot

# Set up your secrets
cp .env.example .env
cp config/settings.yaml.example config/settings.yaml
# Edit both files with your Notion token and DB IDs
```

### 2. Add Your Resume

Drop your resume (PDF) into `config/resume/`. The scorer will use it for relevancy matching.

### 3. Run a Scan

```bash
# Quick scan — API-based companies only (fast)
# Use /quick-check workflow in Antigravity

# Full scan — all sources + LinkedIn
# Use /full-scan workflow in Antigravity

# Learn from your Notion feedback
# Use /learn-from-feedback workflow in Antigravity
```

## 🔧 Configuration

| File | Purpose |
|------|---------|
| `.env` | API tokens (gitignored) |
| `config/settings.yaml` | Schedule, search filters, thresholds (gitignored) |
| `config/companies.yaml` | Target companies with ATS type detection |
| `config/profile.yaml` | Your PM profile, skills, preferences |
| `config/job-fit-guide.md` | What makes a great job match for you |

## 📊 Scoring Dimensions

| Dimension | Weight |
|-----------|:------:|
| Role Fit | 30% |
| Skills Match | 25% |
| Seniority | 15% |
| Domain | 10% |
| Location | 10% |
| Learned Preferences | 10% |

## 🧠 Self-Improvement Loop

```
Jobs Found → Score → Push to Notion → User Reviews (✅/❌ + comments)
    ↑                                          ↓
    └── feedback-learner reads reviews ← ← ← ←┘
        └── Updates user-learnings.md
            └── Next scoring run is smarter
```

## 📄 License

MIT
