import requests

KNOWN_JOKES = [
    "Купил мужик шляпу, а она ему как раз.",
    "Король никогда не ответит матом.",
    "Ученые изобрели кружку для левшей.",
    "Промежуток - это расстояние между утками, летящими клином.",
    "Где грань между тонким и плоским юмором?",
]

JOKES_API_BASE_URL = "https://v2.jokeapi.dev/joke/Programming,Pun"


def get_joke(joke_type: str | None = None) -> dict | None:
    url = JOKES_API_BASE_URL
    params = {
        "lang": "en",
        "blacklistFlags": "nsfw,religious,political,racist,sexist,explicit",
    }
    if joke_type:
        params["type"] = joke_type
    response = requests.get(url, params=params)

    if response.status_code != 200:
        return
    json_data: dict = response.json()
    if json_data.get("error"):
        return

    return json_data


def get_random_joke_text():
    json_data = get_joke("single")
    if not json_data:
        return "Error"

    return json_data["joke"]


def get_two_part_joke_texts():
    json_data = get_joke("twopart")

    if not json_data:
        return "Error"

    return json_data["setup"], json_data["delivery"]
