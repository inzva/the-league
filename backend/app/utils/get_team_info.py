import requests
from app.schemas.team import Team
from pydantic import ValidationError


def get_team_info(team_id):
    """
    Returns team information from AlgoLeague API
    """
    url = f"https://api.algoleague.com/api/app/app-user-team/{team_id}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        try:
            vaidated_data = Team.model_validate(data)
            return vaidated_data
        except ValidationError as e:
            print(f"get_team_info validation error: {e}")
            return None
    except requests.RequestException as e:
        print(f"Error fetching team info: {e}")
        return None
