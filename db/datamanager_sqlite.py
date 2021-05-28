from db.database import dbconn
from models.clsFilm import Film
from models.clsVerkoop import Verkoop
from models.clsVertoning import Vertoning
from models.clsZaal import Zaal


class DataManagerSQLite():

    def get_movies(self):
        with dbconn() as cur:
            cur.execute("SELECT * FROM Film")
            rijen = cur.fetchall()
            return [rijen]

    def get_dier_by_id(self, id):
        with dbconn() as cur:
            cur.execute("SELECT * FROM dieren WHERE id = ?", [id])
            rij = cur.fetchone()
            return Dier.from_dict(rij) if rij else None

    def get_asielen(self):
        with dbconn() as cur:
            cur.execute("SELECT * FROM asielen")
            asiel_rijen = cur.fetchall()

            asielen = []
            for asiel_rij in asiel_rijen: 
                cur.execute("SELECT * FROM dieren WHERE asiel_id = ?", [asiel_rij["id"]])
                dieren_rijen = cur.fetchall()
                dieren = [Dier.from_dict(dieren_rij) for dieren_rij in dieren_rijen]
                asielen.append(Asiel(asiel_rij["naam"], asiel_rij["plaats"], dieren, asiel_rij["id"]))
        
            return asielen

    def insert_dier(self, dier):
        with dbconn() as cur:
            cur.execute("INSERT INTO dieren (naam, soort, geslacht, opname_datum, asiel_id) VALUES (?, ?, ?, ?, ?)",
                        [dier.naam, dier.soort, dier.geslacht, dier.opname_datum, dier.asiel_id]
            )


    

    
