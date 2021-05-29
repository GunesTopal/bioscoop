import requests
import json
from ansimarkup import ansiprint as print
from time import sleep

def vind_film_via_titel(titel_van_de_film):
    api_key="2ef341ebc70520dd7390936da45f314e"

    ENDPOINT=f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={titel_van_de_film}&language=nl"
    data=requests.get(ENDPOINT).json()
    filmid=data["results"][0]["id"]

    ENDPOINT=f"https://api.themoviedb.org/3/movie/{filmid}?api_key={api_key}&language=nl"
    data=requests.get(ENDPOINT).json()

    resultaat={}

    resultaat["Titel"]=data["title"]
    resultaat["Duur"]=data["runtime"]
    resultaat["KNT"]=data["adult"]
    resultaat["IMDB_ID"]=data["imdb_id"]
    resultaat["Poster_link"]=("https://image.tmdb.org/t/p/original"+data["poster_path"])
    resultaat["Beschrijving"]=data["overview"]

    return resultaat



def vind_film_via_imdb(imdb):
    api_key="2ef341ebc70520dd7390936da45f314e"

    ENDPOINT=f"https://api.themoviedb.org/3/find/{imdb}?api_key={api_key}&language=nl&external_source=imdb_id"
    data=requests.get(ENDPOINT).json()
    if not len(data['movie_results']):
        print("<red>Geen gegevens gevonden.</red>")
        sleep(2)
        return 0
    filmid=(data['movie_results'][0]['id'])

    ENDPOINT=f"https://api.themoviedb.org/3/movie/{filmid}?api_key={api_key}&language=nl"
    data=requests.get(ENDPOINT).json()

    resultaat={}

    resultaat["Titel"]=data["title"]
    resultaat["Duur"]=data["runtime"]
    resultaat["KNT"]=data["adult"]
    resultaat["IMDB_ID"]=data["imdb_id"]
    resultaat["Poster_link"]=("https://image.tmdb.org/t/p/original"+data["poster_path"])
    resultaat["Beschrijving"]=data["overview"]

    return resultaat
 
