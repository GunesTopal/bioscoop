class Zaal():
    def __init__(self, ID_Zalen, DrieD_Zalen_beschikbaar, Plaatsen):
        self.ID_Zalen = ID_Zalen
        self.DrieD_Zalen_beschikbaar = DrieD_Zalen_beschikbaar
        self.Plaatsen = Plaatsen

    def __str__(self):
        return f"Zaal nummer {self.ID_Zalen} met {self.Plaatsen} plaatsen."
