from functools import wraps
from requests import get
from flask import g, request, redirect, session

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def lookup(input):
    # parse input into searchale string
    temp = input.split()
    query = "+".join(temp)

    # Search books by title
    response = get(f"https://www.googleapis.com/books/v1/volumes?q={query}")
    response.raise_for_status()
    data = response.json()

    results = []
    for item in data["items"]:
        # Dictionary to parse JSON result into
        volume = {
            "volumeId": None,
            "cover": None,
            "title": None,
            "authors": ["None",],
            "publishedDate": None
        }
        # Test if key exist in JSON record for current volume
        if "id" in item:
            volume.update({"volumeId": item["id"]})
        if "imageLinks" in item["volumeInfo"]:
            volume.update({"cover": item["volumeInfo"]["imageLinks"]["smallThumbnail"]})
        if "title" in item["volumeInfo"]:
            volume.update({"title": item["volumeInfo"]["title"]})
        if "authors" in item["volumeInfo"]:
            volume.update({"authors": item["volumeInfo"]["authors"]})
        if "publishedDate" in item["volumeInfo"]:
            volume.update({"publishedDate": item["volumeInfo"]["publishedDate"]})
        # Append current volume record to results list
        results.append(volume)
    return results
