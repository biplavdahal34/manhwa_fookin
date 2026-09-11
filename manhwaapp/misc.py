import requests


def latest_list(limit=8):
    url = "https://api.mangadex.org"
    
    r = requests.get(
    f"{url}/manga",
    params={"order[createdAt]": "desc",
        "limit": limit,
        "includes[]": ["cover_art"],
        "contentRating[]": ["safe", "suggestive", "erotica"]}
    )

    if r.status_code == 200:
        response = r.json()['data']
        return {"api_ok" :True, "response": response}
    return {"api_ok":False, "response_json": None}

def popular_list(limit=8):
    url = "https://api.mangadex.org"
    
    r = requests.get(
    f"{url}/manga",
    params={"order[followedCount]": "desc",
        "limit": limit,
        "includes[]": ["cover_art"],
        "contentRating[]": ["safe", "suggestive", "erotica"]}
    )

    if r.status_code == 200:
        response = r.json()['data']
        return {"api_ok" :True, "response": response}
    return {"api_ok":False, "response_json": None}


def get_manhwa(manhwa_name):
    url = "https://api.mangadex.org"
    
    r = requests.get(
    f"{url}/manga",
    params={
    "title": manhwa_name,
    "includes[]" : ["cover_art"],
    "order[relevance]": "desc",
    }
    )

    if r.status_code == 200:
        response = r.json()['data']
        return {"api_ok" :True, "response": response}
    return {"api_ok":False, "response_json": None}