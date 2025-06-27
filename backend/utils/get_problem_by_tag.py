from config import ALGOLEAGUE_COOKIE
import requests

def get_problems_by_tag_id(tag_id):
    """
    Fetches a list of problem IDs for a given tag ID from the AlgoLeague API.
    """
    url = "https://admin.algoleague.com/api/app/problem/authorized-problems"
    params = {
        "filter": "",
        "tagIds[0]": tag_id,
        "difficulty": "",
        "status": "",
        "ownerUserId": "",
        "doIsMy": "false",
        "doIsMyCoSetter": "false",
        "skipCount": 0,
        "maxResultCount": 10000,
        "sorting": "creationTime desc",
        "combineWith": "Or"
    }
    headers = {
        "Cookie": ALGOLEAGUE_COOKIE,
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        return [item["id"] for item in data.get("items", [])]
        
    except requests.RequestException as e:
        print(f"Error fetching problems for tag {tag_id}: {e}")
        return []