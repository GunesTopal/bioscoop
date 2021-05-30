import sqlite3
from ansimarkup import ansiprint as print
import os
from time import sleep
from prettytable import PrettyTable, from_db_cursor
from sql_list import sql_film_database
from tools.movie_request import vind_film_via_imdb

# ------------------ CUSTOM FUNCTIONS ----------------
def clear_screen_logo():
    os.system('cls')
    print("<bg #00005f>CINEMAX ADMINISTRATOR</bg #00005f>")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def druk_verder():
    print()
    keuze=input("Druk op ENTER om verder te gaan...")
    clear_screen()
    sleep(.7)

def druk_neeja():
    print()
    print("Type:")
    print("<green>'j' om te bevestigen.</green>")
    print("<red>'n' om te annuleren.</red>")
    antwoord=""
    while True:
        keuze=input()
        if not keuze:
            antwoord= True
        elif not keuze[0].lower() in ['j','n']:
            continue
        elif keuze[0].lower() == 'j':
            antwoord= True
        elif keuze[0].lower() == 'n':
            antwoord= False
        break
    print("<fg #00FF8A>OK</fg #00FF8A>" if antwoord else "<fg #FF8400>Geannuleerd</fg #FF8400>")

    return antwoord



def getInteger(vraag):
    while True:
        try:
            getal = int( input( vraag ) )
        except ValueError:
            print( "Vul een getal in aub." )
            continue
        return getal

def presentatie_main(lijst):
    keuze_dict={}
    for getal in range (len(lijst)):
        if getal != len(lijst)-1:
            keuze_dict[getal+1]=lijst[getal]
            print(f"<green>{getal+1}:</green> {lijst[getal]}")
        else:
            keuze_dict[0]=lijst[getal]
            print(f"<red>{0}: </red>{lijst[getal]}")
    print()
    while True:
        keuze=getInteger("Maak uw keuze: ")
        if not keuze in list(keuze_dict.keys()):
            print(f"Kies een geldig getal uit de lijst:")
            continue
        break
    return keuze_dict[keuze]

def get_inventory_list():
    resultaat=[]
    for rij in sql_film_database():
        resultaat.append([rij._ID_Film, rij._Titel, rij.Duur, 'Ja' if rij.KNT==1 else 'Nee', rij.IMDB_ID])
    
    resultaat.sort(key=lambda x:x[1])
    return resultaat

def show_table(list):
    x=PrettyTable()
    x.field_names=["ID","Titel","Duur","KNT","IMDB"]
    x.add_rows(list)
    return x

def insert_film_database(titel, duur, knt, DrieD, IMDB_ID, Poster_link, Beschrijving):
    DrieD=True if DrieD=="Ja" else False

    knt=True if knt=='Ja' else False
    con=sqlite3.connect('data/Databank.db')
    cur=con.cursor()
    cur.execute('INSERT INTO Film (Titel,Duur,KNT,IMDB_ID,Poster_link,Beschrijving) VALUES (?,?,?,?,?,?)',(titel,duur,knt,IMDB_ID,Poster_link,Beschrijving))
    print(f"<green>De Film met titel '{titel}' werd aan de database toegevoegd!</green>")
    con.commit()
    con.close()
    druk_verder()

def delete_film_database(list):
    con=sqlite3.connect('data/Databank.db')
    cur=con.cursor()
    if len(list)==1:
        cur.execute(f'DELETE FROM Film WHERE ID_Film={list[0][0]}')
        print(f"<red>De Film met titel '{list[0][1]}' werd van de database verwijderd!</red>")
    else:
        for film in list:
            cur.execute(f'DELETE FROM Film WHERE ID_Film={film[0]}')
            print(f"<red>De Film met titel '{film[1]}' werd van de database verwijderd!</red>")
    con.commit()
    con.close()
    druk_verder()
    
# ------------------ FUNCTIONS SCENARIO ----------------
def menu_startpage():
    while True:
        clear_screen_logo()
        lijst=["Lijst films bewerken","Vertoningen bewerken","Tickets bewerken","Afsluiten"]
        keuze=(presentatie_main(lijst))
        if keuze==lijst[0]:
            menu_films_bewerken()
            
        elif keuze==lijst[1]:
            print("keuze 2 geselecteerd")
            sleep(1)

        elif keuze==lijst[2]:
            print("keuze 3 geselecteerd")
            sleep(1)

        elif keuze==lijst[3]:
            clear_screen()
            print("Programma wordt afgesloten. Bedankt en tot de volgende keer.")
            print("<black>- Günes Topal</black>")
            print("<yellow>versie: 1 - 2021/05/30</yellow>")
            print("<red>gunes.topal@gmail.com</red>")
            sleep(2)
            exit()
 
def menu_films_bewerken():
    while True:
        clear_screen()
        print("<bg #EE5900>FILMS</bg #EE5900>")
        lijst=["Inventaris", "Toevoegen", "Zoeken","Verwijderen", "Terug"]
        keuze=(presentatie_main(lijst))
        if keuze==lijst[0]:
            menu_inventaris()
            
        elif keuze==lijst[1]:
            menu_film_toevoegen()
            continue

        elif keuze==lijst[2]:
            clear_screen()
            print("<bg #00FCFF><black>ZOEKEN</black></bg #00FCFF>")
            menu_film_zoeken()
            druk_verder()
            continue
            

        elif keuze==lijst[3]:
            clear_screen()
            menu_film_verwijderen()
            continue
            

        elif keuze==lijst[4]:
            menu_startpage()
            

def menu_inventaris():
    clear_screen()
    print("<bg #006263>INVENTARIS</bg #006263>")
    print(show_table(get_inventory_list()))
    druk_verder()

def menu_film_toevoegen():
    while True:

        clear_screen()
        print("<bg #00FCFF><black>TOEVOEGEN</black></bg #00FCFF>")
        print("<b>IMDB ID van film:</b> ", end="")
        IMDB_ID=input("")
        if not IMDB_ID:
            return None

        elif not len(IMDB_ID) in [9,10] or not IMDB_ID[:2]=='tt':
            print(f"<red>{IMDB_ID} is geen geldige imdb ID</red>")
            print(f"Probeer opnieuw.")
            sleep(2)
            continue
        break
    if vind_film_via_imdb(IMDB_ID)==0:
        return None

    Poster_link=vind_film_via_imdb(IMDB_ID)['Poster_link']
    Beschrijving=vind_film_via_imdb(IMDB_ID)['Beschrijving']

    print(f"<b>Titel: ({vind_film_via_imdb(IMDB_ID)['Titel']}) </b>", end="")
    titel=input()
    if not titel:
        titel=vind_film_via_imdb(IMDB_ID)['Titel']

    print(f"<b>Duur: ({vind_film_via_imdb(IMDB_ID)['Duur']}) </b>", end="")
    duur=input()
    if not duur:
        duur=vind_film_via_imdb(IMDB_ID)['Duur']

    print(f"<b>KNT: ({'Nee' if vind_film_via_imdb(IMDB_ID)['KNT']==False else 'Ja'}) </b>", end="")
    knt=input()
    if not knt or not knt.lower() in ['j','ja']:
        knt='Nee' if vind_film_via_imdb(IMDB_ID)['KNT']==False else 'Ja'

    print(f"<b>3D: (Nee)</b> ", end="")
    DrieD=(input()).capitalize()
    if not DrieD or not DrieD.lower() in ['j','ja'] :
        DrieD="Nee"

    insert_film_database(titel, duur, knt, DrieD, IMDB_ID, Poster_link, Beschrijving)

def menu_film_zoeken():
    
    print("<b>Zoek film(s) via titel of imdb:</b>") 
    print("<fg #B15700><b>Tip:</b></fg #B15700> Gebruik + voor meerdere films)")
    gegevens=input("")
    zoek = gegevens.split("+")

    inventaris=get_inventory_list()
    resultaat=[]
    for film in inventaris:
        if len(zoek)==1:
            if zoek[0].lower() in film[1].lower() or zoek[0].lower() in film[4]:
                resultaat.append(film)
        else:
            for item in zoek:
             if item.lower() in film[1].lower() or item.lower() in film[4]:
                resultaat.append(film)

    if len(resultaat)==0:
        print("<red>Geen resultaat</red>")
    else:
        print(show_table(resultaat))
    
    return resultaat

def menu_film_verwijderen():
    while True:
        print("<bg #FF0000><black>VERWIJDEREN</black></bg #FF0000>")
        resultaat=menu_film_zoeken()
        if len(resultaat)==0:
            druk_verder()
            continue
        elif len(resultaat)>5:
            print(f"Er zijn meer dan 5 resultaten ({len(resultaat)})")
            druk_verder()
            break
    
        if len(resultaat)>1:
            print(f"Er zijn {len(resultaat)} resultaten.")
            print(f'U staat op het moment om de films met titels:')
            print('-'*20)
            for titel in resultaat:
                print(titel[1])
            print('-'*20)
            print("te verwijderen.")
        else:
            print(f'U staat op het moment om de film met titel "{resultaat[0][1]}" te wissen.')

        antwoord=druk_neeja()
        if antwoord:
            delete_film_database(resultaat)

        break


# ------------------ CONNECTING TO DATABASE ----------------
# con=sqlite3.connect('data/Databank.db')
# cur=con.cursor()

# cur.execute('''
# CREATE TABLE IF NOT EXISTS Film (
# 	ID_Film INTEGER PRIMARY KEY AUTOINCREMENT,
# 	Titel TEXT,
# 	Duur INT, 
# 	'3D-beschikbaar' TEXT,
# 	KNT TEXT,
# 	IMDB_ID TEXT,
# 	Poster_link TEXT,
# 	Beschrijving TEXT
# )
# ''')

# cur.execute('INSERT INTO Film (Titel,Duur,KNT,IMDB_ID,Poster_link,Beschrijving) VALUES (?,?,?,?,?,?)',('What',36,'no','no','no','none'))



# cur.execute('SELECT * FROM Film WHERE Titel LIKE "%braveheart%"')
# movie_title=cur.fetchall()
# con.commit()
# con.close()

# lijst=[x for x in movie_title[0]]

# print(lijst)s



# menu_film_toevoegen()
# insert_film_database("Enter", 100, "Nee", "Nee", "tt0070034", "https://image.tmdb.org/t/p/original/zN7OOSARMLVzl9xJqkW2CcZ3xhY.jpg", "geen wapens op het eiland zijn.")
menu_startpage()