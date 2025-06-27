from config import ALGOLEAGUE_COOKIE
import random
import requests

def get_unsolved_random_problem(available_problems, player_usernames):
    if not available_problems:
        return None

    team_players = set()
    for players in player_usernames.values():
        team_players.update(players)

    candidates = available_problems.copy()
    submission_url = ("https://admin.algoleague.com/api/app/problem-submission-results"
                      "?status[0]=Accepted&allSubmissions=true&skipCount=0&maxResultCount=10000")
    url = "https://admin.algoleague.com/api/app/problem/authorized-problems"
    params = {"status[0]": "Accepted", 
              "allSubmissions": "true", 
              "skipCount": 0, 
              "maxResultCount": 10000}
    headers = {"Cookie": ALGOLEAGUE_COOKIE}

    while candidates:
        problem_id = random.choice(candidates)
        params["problemId"] = problem_id
        try:
            response = requests.get(submission_url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            submissions = data.get("items", [])
            if not any(sub.get("userName") in team_players for sub in submissions):
                return problem_id
            else:
                candidates.remove(problem_id)
        except requests.RequestException as e:
            print(f"Error checking problem {problem_id}: {e}")
            candidates.remove(problem_id)
    return None