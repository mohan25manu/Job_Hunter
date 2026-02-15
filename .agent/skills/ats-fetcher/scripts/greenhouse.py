#!/usr/bin/env python3
"""
Greenhouse ATS Job Fetcher

Fetches job listings from Greenhouse's public JSON API.
Usage: python3 greenhouse.py --company figma --role "Product Manager"
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
from datetime import datetime


def fetch_greenhouse_jobs(company_id: str, role_filter: str = "Product Manager") -> list:
    """Fetch jobs from Greenhouse JSON API and filter for PM roles."""
    url = f"https://boards-api.greenhouse.io/v1/boards/{company_id}/jobs"
    
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "JobPilot/1.0"})
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"Error fetching {company_id}: HTTP {e.code}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"Error fetching {company_id}: {e}", file=sys.stderr)
        return []

    jobs = data.get("jobs", [])
    
    # PM title keywords to match
    pm_keywords = [
        "product manager", "head of product", "director of product",
        "vp of product", "chief product officer", "group product manager",
        "staff product manager", "principal product manager"
    ]
    
    # Keywords to exclude (not PM roles)
    exclude_keywords = [
        "project manager", "program manager", "engineering manager",
        "production manager", "property manager"
    ]
    
    filtered = []
    for job in jobs:
        title = job.get("title", "").lower()
        
        # Check if title matches PM keywords
        is_pm = any(kw in title for kw in pm_keywords)
        is_excluded = any(kw in title for kw in exclude_keywords)
        
        # Also match if role_filter is in title
        if role_filter:
            is_pm = is_pm or role_filter.lower() in title
        
        if is_pm and not is_excluded:
            location = job.get("location", {}).get("name", "Unknown")
            updated_at = job.get("updated_at", "")
            
            filtered.append({
                "title": job.get("title", ""),
                "company": company_id,
                "location": location,
                "url": job.get("absolute_url", ""),
                "posted_date": updated_at[:10] if updated_at else "",
                "description_snippet": "",  # Greenhouse list doesn't include full desc
                "department": ", ".join(d.get("name", "") for d in job.get("departments", [])),
                "source": "greenhouse",
                "job_id": str(job.get("id", ""))
            })
    
    return filtered


def main():
    parser = argparse.ArgumentParser(description="Fetch PM jobs from Greenhouse")
    parser.add_argument("--company", required=True, help="Greenhouse company ID (e.g., figma)")
    parser.add_argument("--role", default="Product Manager", help="Role to filter for")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()
    
    jobs = fetch_greenhouse_jobs(args.company, args.role)
    
    if args.json:
        print(json.dumps(jobs, indent=2))
    else:
        print(f"Found {len(jobs)} PM jobs at {args.company}:")
        for j in jobs:
            print(f"  • {j['title']} — {j['location']} ({j['posted_date']})")
            print(f"    {j['url']}")


if __name__ == "__main__":
    main()
