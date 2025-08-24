from config import ALGOLEAGUE_COOKIE
from datetime import datetime
import requests
import time


def get_recent_solver_team(problem_id, player_usernames):
    """
    Returns the team of the most recent solver for a given problem ID from the AlgoLeague API.
    """
    url = "https://admin.algoleague.com/api/app/problem/authorized-problems"
    headers = {
        "Cookie": ALGOLEAGUE_COOKIE,
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

    current_time = time.time()

    for item in data.get("items", []):
        end_date_str = item.get("endDate")
        if not end_date_str:
            continue
        try:
            end_dt = datetime.fromisoformat(end_date_str.replace("Z", "+00:00"))
        except ValueError:
            continue
        end_timestamp = end_dt.timestamp()
        if current_time - end_timestamp <= 3600:
            solver_username = item.get("userName")
            for team_key, usernames in player_usernames.items():
                if solver_username in usernames:
                    return team_key
    return None
