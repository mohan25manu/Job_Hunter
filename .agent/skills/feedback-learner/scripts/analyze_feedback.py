#!/usr/bin/env python3
"""
Feedback Analyzer

Reads user feedback from Notion Job Pipeline DB and extracts patterns.
Usage: python3 analyze_feedback.py --token <token> --db-id <db_id>
"""

import argparse
import json
import sys
import urllib.request
import urllib.error


def fetch_reviewed_jobs(token: str, db_id: str) -> dict:
    """Fetch jobs that have been reviewed (Applied or Rejected) from Notion."""
    
    url = f"https://api.notion.com/v1/databases/{db_id}/query"
    
    # Filter for reviewed jobs
    payload = {
        "filter": {
            "or": [
                {"property": "Status", "select": {"equals": "✅ Applied"}},
                {"property": "Status", "select": {"equals": "❌ Rejected"}}
            ]
        }
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
            result = json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"Error fetching reviewed jobs: {e.code}", file=sys.stderr)
        return {"approved": [], "rejected": []}
    
    approved = []
    rejected = []
    
    for page in result.get("results", []):
        props = page.get("properties", {})
        
        title_arr = props.get("Job Title", {}).get("title", [])
        title = title_arr[0].get("plain_text", "") if title_arr else ""
        
        company = (props.get("Company", {}).get("select") or {}).get("name", "")
        
        status = (props.get("Status", {}).get("select") or {}).get("name", "")
        
        comment_arr = props.get("User Comment", {}).get("rich_text", [])
        comment = comment_arr[0].get("plain_text", "") if comment_arr else ""
        
        desc_arr = props.get("Description Snippet", {}).get("rich_text", [])
        description = desc_arr[0].get("plain_text", "") if desc_arr else ""
        
        reasons_arr = props.get("Match Reasons", {}).get("rich_text", [])
        reasons = reasons_arr[0].get("plain_text", "") if reasons_arr else ""
        
        job_data = {
            "title": title,
            "company": company,
            "description": description,
            "reasons": reasons,
            "user_comment": comment
        }
        
        if "Applied" in status:
            approved.append(job_data)
        elif "Rejected" in status:
            rejected.append(job_data)
    
    return {"approved": approved, "rejected": rejected}


def main():
    parser = argparse.ArgumentParser(description="Analyze user feedback from Notion")
    parser.add_argument("--token", required=True, help="Notion API token")
    parser.add_argument("--db-id", required=True, help="Job Pipeline DB ID")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()
    
    feedback = fetch_reviewed_jobs(args.token, args.db_id)
    
    if args.json:
        print(json.dumps(feedback, indent=2))
    else:
        print(f"Approved jobs: {len(feedback['approved'])}")
        for j in feedback["approved"]:
            print(f"  ✅ {j['title']} at {j['company']}")
            if j["user_comment"]:
                print(f"     Comment: \"{j['user_comment']}\"")
        
        print(f"\nRejected jobs: {len(feedback['rejected'])}")
        for j in feedback["rejected"]:
            print(f"  ❌ {j['title']} at {j['company']}")
            if j["user_comment"]:
                print(f"     Comment: \"{j['user_comment']}\"")


if __name__ == "__main__":
    main()
