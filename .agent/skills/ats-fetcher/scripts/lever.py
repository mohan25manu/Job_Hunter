#!/usr/bin/env python3
"""
Lever ATS Job Fetcher

Fetches job listings from Lever's public API.
Usage: python3 lever.py --company flyzipline --role "Product Manager"
"""

import argparse
import json
import sys
import urllib.request
import urllib.error


def fetch_lever_jobs(company_id: str, role_filter: str = "Product Manager") -> list:
    """Fetch jobs from Lever public API and filter for PM roles."""
    url = f"https://api.lever.co/v0/postings/{company_id}"
    
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "JobPilot/1.0"})
        with urllib.request.urlopen(req, timeout=15) as response:
            jobs = json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"Error fetching {company_id}: HTTP {e.code}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"Error fetching {company_id}: {e}", file=sys.stderr)
        return []

    # PM title keywords
    pm_keywords = [
        "product manager", "head of product", "director of product",
        "vp of product", "chief product officer", "group product manager",
        "staff product manager", "principal product manager"
    ]
    
    exclude_keywords = [
        "project manager", "program manager", "engineering manager",
        "production manager", "property manager"
    ]
    
    filtered = []
    for job in jobs:
        title = job.get("text", "").lower()
        
        is_pm = any(kw in title for kw in pm_keywords)
        is_excluded = any(kw in title for kw in exclude_keywords)
        
        if role_filter:
            is_pm = is_pm or role_filter.lower() in title
        
        if is_pm and not is_excluded:
            categories = job.get("categories", {})
            location = categories.get("location", job.get("workplaceType", "Unknown"))
            
            filtered.append({
                "title": job.get("text", ""),
                "company": company_id,
                "location": location,
                "url": job.get("hostedUrl", ""),
                "posted_date": "",  # Lever doesn't expose post date in list
                "description_snippet": job.get("descriptionPlain", "")[:300],
                "department": categories.get("team", ""),
                "source": "lever",
                "job_id": job.get("id", "")
            })
    
    return filtered


def main():
    parser = argparse.ArgumentParser(description="Fetch PM jobs from Lever")
    parser.add_argument("--company", required=True, help="Lever company ID")
    parser.add_argument("--role", default="Product Manager", help="Role to filter for")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()
    
    jobs = fetch_lever_jobs(args.company, args.role)
    
    if args.json:
        print(json.dumps(jobs, indent=2))
    else:
        print(f"Found {len(jobs)} PM jobs at {args.company}:")
        for j in jobs:
            print(f"  • {j['title']} — {j['location']}")
            print(f"    {j['url']}")


if __name__ == "__main__":
    main()
