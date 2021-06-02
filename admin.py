import sqlite3
from ansimarkup import ansiprint as print
import os
from time import sleep
from prettytable import PrettyTable, from_db_cursor
from sql_list import sql_film_database, sql_vertoning_database, sql_zaal_database
from tools.movie_request import vind_film_via_imdb
from datetime import datetime, timedelta
import locale
locale.setlocale(locale.LC_ALL, "")


# ------------------ CUSTOM VARIABLES ----------------
vandaag=datetime.now()
vandaag_datum=vandaag.strftime("%d/%m/%Y")
vandaag_tijd=vandaag.strftime("%H:%M")


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

def druk_continue():
    print()
    keuze=input("Druk op ENTER om verder te gaan...")
    sleep(.7)

def kleur_goud(string):
    if not type(string)==str:
        string=str(string)
    string=f"<fg #FFD700>{string}</fg #FFD700>"
    return string

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

def datum_ingave(prompt):
    while True:
        try:
            datum=input(prompt)
            if not datum:
                datum=datetime.now()
                datum=datum.strftime("%d/%m/%Y")
                datum=datetime.strptime(datum,"%d/%m/%Y")
                print(datum.strftime("%d/%m/%Y"))
            else:
                datum=datetime.strptime(datum,"%d/%m/%Y")
        except TypeError:
            print(f"Datum is fout ingegeven.")
            continue
        except ValueError:
            print(f"Datum is fout ingegeven.")
            continue
        break
    datum=datum.strftime("%d/%m/%Y")

    return datum


def moment_ingave(prompt):
    while True:
        try:
            moment=input(prompt)
            if not moment:
                continue
            else:
                if len(moment)==2:
                    moment=moment+':00'
                moment=datetime.strptime(moment,"%H:%M")
        except TypeError:
            continue
        except ValueError:
            continue
        break
    moment=moment.strftime("%H:%M")

    return moment

def controle_dubbels(lijst): 
    controlelijst = []
    for x in lijst:
        if x in controlelijst:
            ()
        else:
            controlelijst.append(x) 
    if len(controlelijst)<len(lijst):
        return list(controlelijst)
    return lijst

def getInteger(vraag,minima=(-9**9),maxima=(9**9)):
    while True:
        try:
            getal = int( input( vraag ) )
            if getal < minima: 
                print(f"Vul een getal in, groter of gelijk aan {minima}.")
                continue
            if getal > maxima:
                print(f"Vul een getal in, kleiner of gelijk aan {maxima}.")
                continue
        except ValueError:
            print( "Vul een getal in aub." )
            continue
        return getal
def presentatie_main(lijst):
    keuze_dict={}
    for getal in range (len(lijst)):
        if getal != len(lijst)-1:
            keuze_dict[getal+1]=lijst[getal]
            print(f"{kleur_goud(getal+1)}: {lijst[getal]}")
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
        resultaat_film=[i for i in resultaat if int(film_id) == int(i[1][0])]
        resultaat=resultaat_film

    if zaal:
        resultaat_zaal=[i for i in resultaat if i[5]==zaal]
        resultaat=resultaat_zaal
    return resultaat 

def show_table_inventory(list):
    x=PrettyTable()
    x.field_names=["ID","Titel","Duur","KNT","IMDB", "3D Film"]
    x.add_rows(list)
    return x

def show_table_vertoning(list):
    x=PrettyTable()
    x.field_names=["ID_Vertoning","Titel_Film","Datum","Moment","3D","ID_Zaal"]
    x.add_rows(list)
    return x

def id_naar_titel(id):
    inventaris=get_inventory_list()
    for rij in inventaris:
        if rij[0] == id:
            return rij[1]

def insert_vertoning_database(ID_Film, Datum, Moment, DrieD, ID_Zaal):
    DrieD=True if DrieD=="Ja" else False

    con=sqlite3.connect('data/Databank.db')
    cur=con.cursor()
    cur.execute('INSERT INTO Vertoning (ID_Film,Datum,Moment,"3D",ID_Zaal) VALUES (?,?,?,?,?)',(ID_Film, Datum, Moment, DrieD, ID_Zaal))
    print(f"<green>De Film met titel '{kleur_goud(id_naar_titel(ID_Film))}' werd aan de database van vertoning toegevoegd!</green>")
    con.commit()
    con.close()
    druk_verder()

def insert_film_database(titel, duur, knt, DrieD, IMDB_ID, Poster_link, Beschrijving):
    DrieD=True if DrieD=="Ja" else False

    knt=True if knt=='Ja' else False
    con=sqlite3.connect('data/Databank.db')
    cur=con.cursor()
    cur.execute('INSERT INTO Film (Titel,Duur,KNT,IMDB_ID,Poster_link,"3Dbeschikbaar",Beschrijving) VALUES (?,?,?,?,?,?,?)',(titel,duur,knt,IMDB_ID,Poster_link,DrieD,Beschrijving))
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
    druk_verder()
    con.commit()
    con.close()


    
# ------------------ FUNCTIONS SCENARIO ----------------


# ------------------ MAIN PAGE----------------
def menu_startpage():
    while True:
        clear_screen_logo()
        lijst=[f"{kleur_goud('Films')} bewerken",f"{kleur_goud('Vertoningen')} bewerken",f"{kleur_goud('Ticket')} bewerken","<red>Afsluiten</red>"]
        keuze=(presentatie_main(lijst))
        if keuze==lijst[0]:
            menu_films_bewerken()
            
        elif keuze==lijst[1]:
            menu_vertoningen_bewerken()
            sleep(1)

        elif keuze==lijst[2]:
            print("keuze 3 geselecteerd")
            sleep(1)

        elif keuze==lijst[3]:
            clear_screen()
            print("Programma wordt afgesloten. Bedankt en tot de volgende keer.")
            print("<bg #000000>- Günes Topal</bg #000000>")
            print("<bg #FFDF00><fg #000000>versie: 1.0.1 - 2021/06/02</fg #000000></bg #FFDF00>")
            print("<bg #ED0000>gunes.topal@gmail.com</bg #ED0000>")
            sleep(2)
            exit()
# ------------------ MAIN VERTONING----------------
def menu_vertoningen_bewerken():
    while True:
        clear_screen()
        print("<bg #FF00E4>VERTONINGEN</bg #FF00E4>")
        lijst=["Alle vertoningen", "Vertoning <green>toevoegen</green>", "Vertoning <red>verwijderen</red>", "Terug"]
        keuze=(presentatie_main(lijst))
        if keuze==lijst[0]:
            menu_vertoning_tonen()
            continue
            
        elif keuze==lijst[1]:
            menu_vertoning_toevoegen()
            continue

        elif keuze==lijst[2]:
            menu_vertoning_verwijderen()
            continue

        elif keuze==lijst[3]:
            menu_startpage()
        

def menu_vertoning_verwijderen():
    menu_vertoning_tonen(1)


def menu_vertoning_zoeken():
    pass


def menu_vertoning_toevoegen():
    clear_screen()
    print("<bg #51B848><black>VERTONINGEN - TOEVOEGEN</black></bg #51B848>")

# Datumkeuze !!!!!!!!!!!!
    while True:
        print("<b>Datum van uw vertoning:</b>")
        print(f"<fg #B15700><b>Tip:</b></fg #B15700> bijvoorbeeld '{kleur_goud('31/05/2021')}'")
        
        datum=datum_ingave("Datum: ")    
        if datetime.strptime(datum, "%d/%m/%Y") < datetime.strptime(vandaag_datum,"%d/%m/%Y"):
            print("<red>U kunt <u>geen</u> vertoningen plannen in het verleden.</red>")
            druk_verder()
            menu_vertoning_toevoegen()

# filmkeuze !!!!!!!!!!!!

        print("<b>Voeg <fg #00FFFF>één</fg #00FFFF> film aan uw lijst van vertoningen:</b>")
        resultaat=menu_film_zoeken(1)
        if not resultaat:
            return
        if not len(resultaat)==1:
            continue
        duurkeuze=resultaat[0][2]
        idkeuze=resultaat[0][0]

        break
    print("<b>Zaal van uw vertoning:</b>")
    print(f"<fg #B15700><b>Tip:</b></fg #B15700> bijvoorbeeld '{kleur_goud('3')}'")
    loop=False
# 3D Film ???????????????
    while True or not loop:
        DrieD=resultaat[0][5]
        zalen=get_zaal_list()

# Zaalkeuze !!!!!!!!!!!!
        zaal=getInteger("Zaal id: ",1,7)
    # controle als 3D film in een 3D zaal kan afspelen
        for i in zalen:
            if i[0]==zaal and i[1]=='Nee' and DrieD=='Ja':
                print(f"<red>Zaal {kleur_goud(zaal)} kan geen 3D films afspelen.</red>")
                loop=True
                print()
                break
            else:
                loop=False
        if loop:
            continue


        vertoning=get_vertoning_list(datum,None,zaal)
        lijst_vertoning_tijdspanne=""
        if len(vertoning)!=0:
            print(f"<fg #767676>{show_table_vertoning(vertoning)}</fg #767676>")
            lijstallefilms=get_inventory_list()
            planning=[[j[0],j[1],j[3], (datetime.strptime(f"{datum} {j[3]}", "%d/%m/%Y %H:%M")+timedelta(minutes=30+i[2])).strftime("%d/%m/%Y %H:%M")] for i in lijstallefilms for j in vertoning if i[0]==j[0]]
            lijst_vertoning_tijdspanne=[[f"{datum} {i[2]}",i[3]] for i in planning]

# Momentkeuze !!!!!!!!!!!!
        print("<b>Moment van uw vertoning:</b>")
        print(f"<fg #B15700><b>Tip:</b></fg #B15700> bijvoorbeeld '{kleur_goud('12:00')}'")
        while True:
            moment=moment_ingave("Tijd: ")
            if moment=="":
                print("Geef een tijd in. (TOEKOMST)")
                continue
            if lijst_vertoning_tijdspanne!="":
                if datum==vandaag_datum and datetime.strptime(moment, '%H:%M')<datetime.strptime(vandaag_tijd, '%H:%M'):
                    print("<red>U kunt <u>geen</u> vertoningen plannen in het verleden.</red>")
                    continue
            break
        print()
# controle of de startmoment van keuze valt tussen lopende vertoningen  !!!!!!!!!!!!
        keuze_eindmoment=datetime.strptime(f"{datum} {moment}", '%d/%m/%Y %H:%M')+timedelta(minutes=duurkeuze)
        keuze_eindmoment=keuze_eindmoment.strftime('%d/%m/%Y %H:%M')
        keuze_tijdspanne=[f"{datum} {moment}", keuze_eindmoment]
    
        for tijd in lijst_vertoning_tijdspanne:
            if datetime.strptime(keuze_tijdspanne[0],'%d/%m/%Y %H:%M') > datetime.strptime(tijd[0],'%d/%m/%Y %H:%M') and datetime.strptime(keuze_tijdspanne[0],'%d/%m/%Y %H:%M') < datetime.strptime(tijd[1],'%d/%m/%Y %H:%M') or datetime.strptime(keuze_tijdspanne[1],'%d/%m/%Y %H:%M') > datetime.strptime(tijd[0],'%d/%m/%Y %H:%M') and datetime.strptime(keuze_tijdspanne[1],'%d/%m/%Y %H:%M') < datetime.strptime(tijd[1],'%d/%m/%Y %H:%M'):
                conflictfilm=[i for i in planning if i[2]==tijd[0][11:16]]
                print(f"<fg #E52B00>{show_table_vertoning(vertoning)}</fg #E52B00>")
                print(f"Uw keuze komt in conflict met de film: '{kleur_goud(conflictfilm[0][1][1])}', die om {kleur_goud(conflictfilm[0][2])} uur in zaal {kleur_goud(zaal)} gepland staat.")
                loop=True
                druk_continue()
                continue
        if loop:
            continue
        else:
            break

    print(f"De film met de titel: {kleur_goud(resultaat[0][1])}{' in <blue>3D</blue>' if DrieD=='Ja' else ''} kan ingepland worden voor vertoning.")
    datum=datetime.strptime(datum, '%d/%m/%Y')
    datum=datum.strftime("%A %d/%m/%Y")
    keuze_eindmoment=datetime.strptime(keuze_eindmoment, '%d/%m/%Y %H:%M')
    keuze_eindmoment=keuze_eindmoment.strftime('%H:%M')
    print(f"{datum.capitalize()} om {moment} in zaal {zaal}.")
    print(f"Na de film is zaal {zaal} terug beschikbaar om {keuze_eindmoment} uur.")
    print("Is dit OK?")
    antwoord=druk_neeja()
    if not antwoord:
        print("Verder gaan?")
        antwoord=druk_neeja()
        if not antwoord:
            return None
        else:
            menu_vertoning_toevoegen()
    datum=datum[-10::1]
    insert_vertoning_database(idkeuze, datum, moment, DrieD, zaal)
    return None

def menu_vertoning_tonen(delete=None):
    while True:
        clear_screen()
        print("<bg #FF00E4>VERTONINGEN</bg #FF00E4>" if not delete else "<bg #FF0000>VERTONINGEN</bg #FF0000>")
        lijst=["Toon vertoning(en) op datum", "Toon vertoning(en) FILM(s)","Terug"] if not delete else ["Vertoning(en) verwijderen op datum", "Vertoning(en) verwijderen volgens FILM(s)","Terug"]
        keuze=(presentatie_main(lijst))
        if keuze==lijst[0]:
            menu_vertoning_toon_op_datum() if not delete else menu_vertoning_toon_op_datum(1)
            continue
            
        elif keuze==lijst[1]:
            menu_vertoning_toon_op_film() if not delete else menu_vertoning_toon_op_film(1)
            continue

        elif keuze==lijst[2]:
            menu_vertoningen_bewerken()
            break

def menu_vertoning_toon_op_datum(delete=None):
    while True:
        clear_screen()
        print("<bg #00FCFF><black>DATUM</black></bg #00FCFF>" if not delete else "<bg #FF0000><white>DATUM</white></bg #FF0000>")
        print("<b>Toon vertoning(en) op datum:</b> " if not delete else "<b>Zoek vertoning(en) op <u>datum</u> om te <red>verwijderen</red>:</b> ")
        print(f"<fg #B15700><b>Tip:</b></fg #B15700> bijvoorbeeld '{kleur_goud('31/05/2021')}'")
        
        datum=datum_ingave("Datum: ")
        if len(get_vertoning_list(datum,None,None))==0:
            print(f"<fg #FFBF00>Op de datum van {'vandaag' if datum==vandaag_datum else datum} zijn <red><b>geen</b></red> resultaten gevonden.</fg #FFBF00>")
        else: 
            resultaat=get_vertoning_list(datum,None,None)
            print(show_table_vertoning(get_vertoning_list(datum,None,None)))
        break
    druk_verder() if not delete else druk_continue()
    # return None if not delete or len(get_vertoning_list(datum,None,None))==0 else print("Heya")
    if delete or len(get_vertoning_list(datum,None,None))!=0:
        lijst=["<red>Verwijder</red> keuze","Alles <red>Verwijderen</red>","<fg #00BAFF>Annuleren</fg #00BAFF>"]
        keuze=presentatie_main(lijst)
        if keuze==lijst[0]:
            print(resultaat)
            druk_verder()
        elif keuze==lijst[1]:
            print(resultaat)
            druk_verder()
        elif keuze==lijst[2]:
            return




def menu_vertoning_toon_op_film(delete=None):
    while True:
        clear_screen()
        print("<bg #00FCFF><black>FILM</black></bg #00FCFF>" if not delete else "<bg #FF0000><white>FILM</white></bg #FF0000>")
        print("<b>Toon vertoning(en) op film:</b> ")
        print(f"<fg #B15700><b>Tip:</b></fg #B15700> bijvoorbeeld '{kleur_goud('33')} of '{kleur_goud('The Lion King')}'")
        zoek=input()
        if not zoek:
            return None
        if type(zoek)==int:
            zoek=(int(zoek) if int(zoek[0]) in [0,1,2,3,4,5,6,7,8,9] else str(zoek))
        resultaat=get_vertoning_list(None,zoek,None)
        if len(resultaat)==0:
            print("<red>Geen resultaat gevonden.</red>")
        else:
            print(show_table_vertoning(get_vertoning_list(None,zoek,None)))
        break
    if not delete:
        druk_verder()
    else:
        print("tot hier")

# ------------------ MAIN FILMS----------------
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
            druk_verder()
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
            break
            
def menu_inventaris():
    clear_screen()
    print("<bg #006263>INVENTARIS</bg #006263>")
    print(show_table_inventory(get_inventory_list()))
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

def menu_film_zoeken(controle=0):
    
    print("<b>Film via id, titel of imdb:</b>" if controle ==1 else "<b>Film(s) via id, titel of imdb:</b>")
    if controle!=1:
        print("<fg #B15700><b>Tip:</b></fg #B15700> Gebruik + voor meerdere films.")

    while True:
        gegevens=input("")
        if not gegevens:
            return None #als niets wordt ingevuld
            # continue
        break
    search = gegevens.split("+")

    zoek=[]
    for i in search:
        if i[0] in ('1','2','3','4','5','6','7','8','9','0'):
            i=int(i)
        zoek.append(i)


    inventaris=get_inventory_list()
    resultaat=[]
    for film in inventaris:
        if len(zoek)==1:
            if type(zoek[0])== int:
                if zoek[0] == film[0]:
                    resultaat.append(film)
            else:
                if zoek[0].lower() in film[1].lower() or zoek[0].lower() == film[4]:
                    resultaat.append(film)
        else:
            for item in zoek:
                if type(item) == int:
                    if item == film[0]:
                        resultaat.append(film)
                else:                 
                    if item.lower() in film[1].lower() or item.lower() == film[4]:
                        resultaat.append(film)

    if len(resultaat)==0:
        print("<red>Geen resultaat gevonden.</red>")
    else:
        print(show_table_inventory(controle_dubbels(resultaat)))
    
    return resultaat

def menu_film_verwijderen():
    while True:
        print("<bg #FF0000><black>VERWIJDEREN</black></bg #FF0000>")
        resultaat=menu_film_zoeken()
        if resultaat==None:
            druk_verder()
            return None
            
        elif len(resultaat)>5:
            print(f"Er zijn meer dan 5 resultaten ({len(resultaat)})")
            druk_verder()
            break
        elif len(resultaat)==0:
            druk_verder()
            continue
    
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

menu_startpage()
