class Verkoop():
    def __init__(self, Verkoop_ID, ID_Vertoning, Tickets_kids, Tickets_standaard, Prijs):
        self.Verkoop_ID = Verkoop_ID
        self.ID_Vertoning = ID_Vertoning
        self.Tickets_kids = Tickets_kids
        self.Tickets_standaard = Tickets_standaard
        self.Prijs = Prijs

    def __str__(self):
        return f"Verkoopnummer: {self.Verkoop_ID} = Prijstotaal: {self.Prijs}"
