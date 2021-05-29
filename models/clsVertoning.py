class Vertoning():
    def __init__(self, ID_Vertoning, ID_Film, Datum, Moment, ID_Zaal):
        self.ID_Vertoning = ID_Vertoning
        self._ID_Film = ID_Film
        self.Datum = Datum
        self.Moment = Moment
        self.ID_Zaal = ID_Zaal

    @property
    def ID_Film(self):
        return self._ID_Film

    def __str__(self):
        return f"Vertoning nummer: {self.ID_Vertoning}"
