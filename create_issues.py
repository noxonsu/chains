import json
import os
import requests
import sys
from datetime import datetime, timedelta

def load_existing_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return []

def create_github_issue(token, title, body):
    url = "https://api.github.com/repos/noxonsu/chains/issues"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {
        "title": title,
        "body": body
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        print(f"Successfully created Issue {title}")
    else:
        print(f"Failed to create issue {title}")
        print(response.json())

def check_existing_issue(token, title):
    url = f"https://api.github.com/repos/noxonsu/chains/issues?state=all"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        issues = response.json()
        for issue in issues:
            if issue["title"] == title:
                return True
    return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <GitHub_Token>")
        sys.exit(1)

    github_token = sys.argv[1]
    existing_data = load_existing_data("sites.json")

    # Get the current date and time
    now = datetime.now()

    for item in existing_data:
        block_number = item.get("blockNumber", None)
        date_add_str = item.get("dateAdd", None)
        
        if date_add_str:
            date_add = datetime.strptime(date_add_str, '%Y-%m-%d')
            days_diff = (now - date_add).days
        else:
            days_diff = None

        if block_number is not None and isinstance(block_number, int) and block_number < 100 and (days_diff is None or days_diff <= 2):
            chain_id = item.get("chainId", "Unknown")
            ticker = item.get("ticker", "Unknown")
            title = f"ADD {chain_id} {ticker}"

            if not check_existing_issue(github_token, title):
                body = json.dumps(item, indent=4)
                create_github_issue(github_token, title, body)
