#!/usr/bin/env python3
"""
Notion Job Pipeline DB Creator

Creates the Job Pipeline database in Notion with the correct schema.
Usage: python3 create_db.py --token <token> --parent-page-id <id>
"""

import argparse
import json
import sys
import urllib.request
import urllib.error


def create_job_pipeline_db(token: str, parent_page_id: str) -> str:
    """Create the Job Pipeline database in Notion. Returns the new DB ID."""
    
    url = "https://api.notion.com/v1/databases"
    
    payload = {
        "parent": {"type": "page_id", "page_id": parent_page_id},
        "title": [{"type": "text", "text": {"content": "Job Pipeline"}}],
        "properties": {
            "Job Title": {"title": {}},
            "Company": {
                "select": {
                    "options": []  # Auto-populated as jobs are added
                }
            },
            "Match Score": {"number": {"format": "number"}},
            "Verdict": {
                "select": {
                    "options": [
                        {"name": "strong_match", "color": "green"},
                        {"name": "good_match", "color": "blue"},
                        {"name": "worth_reviewing", "color": "yellow"},
                        {"name": "weak_match", "color": "orange"},
                        {"name": "no_match", "color": "red"}
                    ]
                }
            },
            "Location": {"rich_text": {}},
            "Apply Link": {"url": {}},
            "Match Reasons": {"rich_text": {}},
            "Gaps": {"rich_text": {}},
            "Source": {
                "select": {
                    "options": [
                        {"name": "linkedin", "color": "blue"},
                        {"name": "greenhouse", "color": "green"},
                        {"name": "lever", "color": "purple"},
                        {"name": "career_page", "color": "orange"}
                    ]
                }
            },
            "Date Found": {"date": {}},
            "Posted Date": {"date": {}},
            "Status": {
                "select": {
                    "options": [
                        {"name": "🆕 New", "color": "blue"},
                        {"name": "👀 Reviewed", "color": "yellow"},
                        {"name": "✅ Applied", "color": "green"},
                        {"name": "❌ Rejected", "color": "red"},
                        {"name": "⏸️ Saved", "color": "gray"}
                    ]
                }
            },
            "User Comment": {"rich_text": {}},
            "Description Snippet": {"rich_text": {}},
            "Department": {"select": {"options": []}},
            "Action": {
                "select": {
                    "options": [
                        {"name": "apply_now", "color": "green"},
                        {"name": "review", "color": "yellow"},
                        {"name": "skip", "color": "red"}
                    ]
                }
            }
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
            db_id = result.get("id", "")
            print(f"✅ Created Job Pipeline DB: {db_id}")
            print(f"   URL: {result.get('url', '')}")
            return db_id
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"❌ Error creating DB: HTTP {e.code}", file=sys.stderr)
        print(f"   {error_body}", file=sys.stderr)
        return ""


def main():
    parser = argparse.ArgumentParser(description="Create Notion Job Pipeline DB")
    parser.add_argument("--token", required=True, help="Notion API token")
    parser.add_argument("--parent-page-id", required=True, help="Parent page ID")
    args = parser.parse_args()
    
    db_id = create_job_pipeline_db(args.token, args.parent_page_id)
    if db_id:
        print(f"\n📋 Add this to config/settings.yaml:")
        print(f"   job_pipeline_db_id: \"{db_id}\"")


if __name__ == "__main__":
    main()
