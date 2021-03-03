from functools import wraps
from requests import get
from flask import request, redirect, session

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def googleBooksSearch(input):
    # parse input into searchale string
    temp = input.split()
    query = "+".join(temp)

    # Search books by title
    response = get(f"https://www.googleapis.com/books/v1/volumes?q={query}&printType=books")
    response.raise_for_status()
    data = response.json()

    results = []
    for item in data["items"]:
        # Dictionary to parse JSON result into
        volume = {
            "volumeId": None,
            "cover": None,
            "title": None,
            "authors": None,
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

def googleBooksRetreive(volumeID):
    data = get(f"https://www.googleapis.com/books/v1/volumes/{volumeID}")
    data.raise_for_status()
    response = data.json()

    # Dictionary to store volume information
    volume = {
        "googleBooksId": volumeID,
        "title": None,
        "subtitle": None,
        "cover": None,
        "authors": None,
        "publisher": None,
        "publishedDate": None,
        "ISBN": None,
        "pageCount": None,
        "description": None
    }

    # Checks for keys in response data
    if "title" in response["volumeInfo"]:
        volume.update({"title": response["volumeInfo"]["title"]})
    if "subtitle" in response["volumeInfo"]:
        volume.update({"subtitle": response["volumeInfo"]["subtitle"]})
    if "smallThumbnail" in response["volumeInfo"]["imageLinks"]:
        volume.update({"cover": response["volumeInfo"]["imageLinks"]["smallThumbnail"]})
    if "authors" in response["volumeInfo"]:
        volume.update({"authors": response["volumeInfo"]["authors"]})
    if "publisher" in response["volumeInfo"]:
        volume.update({"publisher": response["volumeInfo"]["publisher"]})
    if "publishedDate" in response["volumeInfo"]:
        volume.update({"publishedDate": response["volumeInfo"]["publishedDate"]})
    if "industryIdentifiers" in response["volumeInfo"]:
        volume.update({"ISBN": response["volumeInfo"]["industryIdentifiers"][0]["identifier"]})
    if "pageCount" in response["volumeInfo"]:
        volume.update({"pageCount": response["volumeInfo"]["pageCount"]})
    if "description" in response["volumeInfo"]:
        volume.update({"description": response["volumeInfo"]["description"]})

    # Return volume info
    return volume

