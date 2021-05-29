

class Film():
    def __init__(self, ID_Film, Titel, Duur, DrieD_beschikbaar, KNT, IMDB_ID, Poster_link, Beschrijving):
        self._ID_Film = ID_Film
        self._Titel = Titel
        self.Duur = Duur
        self.DrieD_beschikbaar = DrieD_beschikbaar
        self.KNT = KNT
        self.IMDB_ID = IMDB_ID
        self.Poster_link = Poster_link
        self.Beschrijving = Beschrijving

    def __str__(self):
        return f"{self._Titel}"
    
    @property
    def ID_Film(self):
        return self._ID_Film

