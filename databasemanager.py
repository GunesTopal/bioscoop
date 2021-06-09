from sql_list import sql_film_database, sql_zaal_database, sql_vertoning_database, sql_verkoop_database

def get_zaal_list():
    resultaat=[]
    for rij in sql_zaal_database():
        resultaat.append([rij.ID_Zalen, 'Ja' if rij.DrieD_Zalen_beschikbaar==1 else 'Nee', rij.Plaatsen])

    resultaat.sort(key=lambda x:x[0])
    return resultaat

def get_inventory_list():
    resultaat=[]
    for rij in sql_film_database():
        resultaat.append([rij._ID_Film, rij._Titel, rij.Duur, 'Ja' if rij.KNT==1 else 'Nee', rij.IMDB_ID, 'Ja' if rij.DrieD_beschikbaar==1 else 'Nee'])
    
    resultaat.sort(key=lambda x:x[1].lower())
    return resultaat

def get_vertoning_list(datum=None,film_id=None, zaal=None):
    resultaat=[]
    resultaat_datum=[]
    resultaat_film=[]
    resultaat_idorfilm=[]
    ttt=""
    resultaat_film=[(i._ID_Film,i._Titel) for i in sql_film_database()]

    for rij in sql_vertoning_database():
        for tt in resultaat_film:
            if tt[0]==rij._ID_Film:
                ttt=(tt[0],tt[1])
        resultaat.append([rij._ID_Vertoning, ttt, rij.Datum,  rij.Moment,'Ja' if rij.DrieD==1 else 'Nee', rij.ID_Zaal])
    
    if datum:
        resultaat_datum=[i for i in resultaat if i[2]==datum]
        resultaat=resultaat_datum

    if film_id:
        if type(film_id)==list:
            resultaat_idorfilm=[i  for x in film_id for i in resultaat if i[1][0] == x or x in i[1][1]] 
        elif type(film_id)==int:
            resultaat_idorfilm=[i for i in resultaat if i[1][0]==film_id and type(film_id)==int]
        elif type(film_id)==str:
            resultaat_idorfilm=[i for i in resultaat if film_id.lower() in i[1][1].lower() and type(film_id)==str]

        resultaat=resultaat_idorfilm

    if zaal:
        resultaat_zaal=[i for i in resultaat if i[5]==zaal]
        resultaat=resultaat_zaal

    resultaat.sort(key=lambda x:x[3])
    return resultaat 

def get_verkoop_list():
    resultaat=[]
    for rij in sql_verkoop_database():
        resultaat.append([rij.Verkoop_ID, rij.ID_Vertoning, rij.Tickets_kids, rij.Tickets_standaard, rij.Prijs])
    
    resultaat.sort(key=lambda x:x[0])
    return resultaat
