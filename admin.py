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
    os.system('cls')


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

def show_inventory():
    # Günes:"Alternatief"

    # connection=sqlite3.connect("data/Databank.db")
    # cursor=connection.cursor()
    # cursor.execute("SELECT ID_Film, Titel, Duur, KNT, IMDB_ID FROM Film")
    # mytable=from_db_cursor(cursor)
    # return mytable

    x=PrettyTable()
    x.field_names=["ID","Titel","Duur","KNT","IMDB"]
    x.add_rows(get_inventory_list())
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
    keuze=input("Druk op ENTER om terug te keren...")
    clear_screen()
    sleep(1)
    
# ------------------ FUNCTIONS SCENARIO ----------------
def menu_startpage():
    while True:
        clear_screen_logo()
        lijst=["Lijst films bewerken","Vertoningen bewerken","Tickets bewerken","Afsluiten"]
        keuze=(presentatie_main(lijst))
        if keuze==lijst[0]:
            menu_films_bewerken()
            break
        elif keuze==lijst[1]:
            print("keuze 2 geselecteerd")
            break

        elif keuze==lijst[2]:
            print("keuze 3 geselecteerd")
            break

        elif keuze==lijst[3]:
            clear_screen()
            print("Programma wordt afgesloten. Bedankt en tot de volgende keer.")
            print("- Günes Topal")
            print("gunes.topal@gmail.com")
            sleep(2)
            break
 
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
            

        elif keuze==lijst[2]:
            pass
            

        elif keuze==lijst[3]:
            pass
            

        elif keuze==lijst[4]:
            menu_startpage()
            

def menu_inventaris():
    clear_screen()
    print("<bg #006263>INVENTARIS</bg #006263>")
    print(show_inventory())
    sleep(1)
    keuze=input("Druk op ENTER om terug te keren...")
    clear_screen()
    sleep(1)

def menu_film_toevoegen():
    clear_screen()
    print("<bg #00FCFF><black>TOEVOEGEN</black></bg #00FCFF>")
    print("<b>IMDB ID van film:</b> ", end="")
    IMDB_ID=input("")
    try:
        Poster_link=vind_film_via_imdb(IMDB_ID)['Poster_link']
    except TypeError:
        menu_film_toevoegen()
    except KeyError:
        menu_film_toevoegen()

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