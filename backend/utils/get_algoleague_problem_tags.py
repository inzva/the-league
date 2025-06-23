import requests
cookie = "" # Replace with actual cookie value
def get_algoleague_problem_tags_and_ids():
    """
    Fetches a list of all tags from the Algoleague API.
    Returns a list of tag names.
    """
    url = "https://admin.algoleague.com/api/app/tag"
    params = {
        "tagType": "Parent",
        "skipCount": 0,
        "maxResultCount": 100
    }
    headers = {
        "Cookie": cookie
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        data = response.json()
        # Extract just the tag names from the items array
        tags = {item["name"] : item["id"] for item in data.get("items", [])}
        return tags
        
    except requests.RequestException as e:
        print(f"Error fetching tags: {e}")
        return {}
print(get_algoleague_problem_tags_and_ids())