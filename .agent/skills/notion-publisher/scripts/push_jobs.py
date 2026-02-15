#!/usr/bin/env python3
"""
Notion Job Publisher

Pushes scored job listings to the Job Pipeline Notion database.
Usage: python3 push_jobs.py --token <token> --db-id <db_id> --jobs <jobs.json>
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
from datetime import datetime


def push_job_to_notion(token: str, db_id: str, job: dict) -> bool:
    """Push a single scored job to the Notion Job Pipeline DB."""
    
    url = "https://api.notion.com/v1/pages"
    
    # Build properties
    properties = {
        "Job Title": {
            "title": [{"text": {"content": job.get("title", "Unknown")}}]
        },
        "Company": {
            "select": {"name": job.get("company", "Unknown")}
        },
        "Match Score": {
            "number": job.get("score", 0)
        },
        "Verdict": {
            "select": {"name": job.get("verdict", "worth_reviewing")}
        },
        "Location": {
            "rich_text": [{"text": {"content": job.get("location", "")}}]
        },
        "Apply Link": {
            "url": job.get("url", None)
        },
        "Source": {
            "select": {"name": job.get("source", "career_page")}
        },
        "Date Found": {
            "date": {"start": datetime.now().strftime("%Y-%m-%d")}
        },
        "Status": {
            "select": {"name": "🆕 New"}
        },
        "Action": {
            "select": {"name": job.get("action", "review")}
        }
    }
    
    # Add optional rich text fields
    if job.get("reasons"):
        reasons_text = "\n".join(f"• {r}" for r in job["reasons"])
        properties["Match Reasons"] = {
            "rich_text": [{"text": {"content": reasons_text[:2000]}}]
        }
    
    if job.get("gaps"):
        gaps_text = "\n".join(f"• {g}" for g in job["gaps"])
        properties["Gaps"] = {
            "rich_text": [{"text": {"content": gaps_text[:2000]}}]
        }
    
    if job.get("description_snippet"):
        properties["Description Snippet"] = {
            "rich_text": [{"text": {"content": job["description_snippet"][:2000]}}]
        }
    
    if job.get("posted_date"):
        try:
            properties["Posted Date"] = {"date": {"start": job["posted_date"][:10]}}
        except (ValueError, IndexError):
            pass
    
    if job.get("department"):
        properties["Department"] = {"select": {"name": job["department"]}}
    
    payload = {
        "parent": {"database_id": db_id},
        "properties": properties
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            return True
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"Error pushing {job.get('title', '?')}: {e.code} - {error_body}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="Push jobs to Notion")
    parser.add_argument("--token", required=True, help="Notion API token")
    parser.add_argument("--db-id", required=True, help="Job Pipeline DB ID")
    parser.add_argument("--jobs", required=True, help="Path to scored jobs JSON file")
    args = parser.parse_args()
    
    with open(args.jobs) as f:
        jobs = json.load(f)
    
    success = 0
    for job in jobs:
        if push_job_to_notion(args.token, args.db_id, job):
            success += 1
            print(f"  ✅ {job.get('title', '?')} at {job.get('company', '?')}")
        else:
            print(f"  ❌ Failed: {job.get('title', '?')}")
    
    print(f"\nPushed {success}/{len(jobs)} jobs to Notion")


if __name__ == "__main__":
    main()
