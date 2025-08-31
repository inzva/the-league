import requests


def get_team_info(team_id):
    """
    Returns team information from AlgoLeague API
    """
    url = f"https://api.algoleague.com/api/app/app-user-team/{team_id}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching team info: {e}")
        return None
