from config import ALGOLEAGUE_COOKIE
import requests


def get_algoleague_problem_tags_and_ids():
    """
    Returns a list of tag names in the AlgoLeague API along with their IDs.
    """
    url = "https://admin.algoleague.com/api/app/tag"
    params = {"tagType": "Parent", "skipCount": 0, "maxResultCount": 100}
    headers = {
        "Cookie": ALGOLEAGUE_COOKIE,
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        tags = {item["name"]: item["id"] for item in data.get("items", [])}
        return tags

    except requests.RequestException as e:
        print(f"Error fetching tags: {e}")
        return {}


print(get_algoleague_problem_tags_and_ids())
