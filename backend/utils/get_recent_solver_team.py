import time
import requests
from datetime import datetime

def get_recent_solver_team(problem_id, player_usernames):
    cookie = "" # Replace with actual cookie
    url = "https://admin.algoleague.com/api/app/problem/authorized-problems"
    headers = {
        "Cookie": cookie
    }
    params = {
        "problemId": problem_id,
        "status[0]": "Accepted",
        "allSubmissions": "true",
        "skipCount": 0,
        "maxResultCount": 10000,
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f"Error checking submissions for problem {problem_id}: {e}")
        return None

    # Check each accepted submission
    current_time = time.time()
    for item in data.get("items", []):
        # Use the accepted submission's endDate; it is expected in ISO 8601 format.
        end_date_str = item.get("endDate")
        if not end_date_str:
            continue
        try:
            end_dt = datetime.fromisoformat(end_date_str.replace("Z", "+00:00"))
        except ValueError:
            continue
        # Convert end_dt to timestamp.
        end_timestamp = end_dt.timestamp()
        # If solved within last one hour (3600 seconds)
        if current_time - end_timestamp <= 3600:
            solver_username = item.get("userName")
            # Determine the team for the solver
            for team_key, usernames in player_usernames.items():
                if solver_username in usernames:
                    return team_key
    return None