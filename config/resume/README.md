# Resume Directory

Place your resume file here (PDF, DOCX, or TXT format).

The system will read this file to:
1. Extract your professional summary, skills, and domains
2. Auto-populate `config/profile.yaml` with relevant details
3. Use the content for LLM-based relevancy scoring against job descriptions

## Supported Formats
- `.pdf` — Recommended
- `.docx` — Supported
- `.txt` — Plain text version

## What Happens After You Place Your Resume
When you next run JobPilot, the `relevancy-scorer` skill will:
- Parse your resume
- Extract key skills, experience, and domains
- Update your profile for better job matching
