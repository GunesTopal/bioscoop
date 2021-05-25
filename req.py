import requests
import json

search="Forrest Gump"
api_key="2ef341ebc70520dd7390936da45f314e"


ENDPOINT=f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={search}"
data=requests.get(ENDPOINT).json()

for i in data["results"]:
    print(i["overview"])
    break
