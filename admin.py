import sqlite3
from ansimarkup import ansiprint as print
import os
from time import sleep
from prettytable import PrettyTable, from_db_cursor
from sql_list import sql_film_database, sql_vertoning_database, sql_zaal_database, sql_verkoop_database
from tools.movie_request import vind_film_via_imdb
from datetime import datetime, timedelta
import locale
locale.setlocale(locale.LC_ALL, "")


# ------------------ CUSTOM VARIABLES ----------------
vandaag=datetime.now()
vandaag_datum=vandaag.strftime("%d/%m/%Y")
vandaag_tijd=vandaag.strftime("%H:%M")
prijs_ticket={'standaard':9,'kids':7,'langspeel':1,'3D':1.5}


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

def datum_ingave(prompt, delete=None):
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
def presentatie_main(lijst, nulerbij=None):
    keuze_dict={}
    for getal in range (len(lijst)):
        if not nulerbij:
            if getal != len(lijst)-1:
                keuze_dict[getal+1]=lijst[getal]
                print(f"{kleur_goud(getal+1)}: {lijst[getal]}")
            else:
                keuze_dict[0]=lijst[getal]
                print(f"<red>{0}: </red>{lijst[getal]}")
        else:
                keuze_dict[getal+1]=lijst[getal]
                print(f"{kleur_goud(getal+1)}: {lijst[getal]}")           
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
            resultaat_idorfilm=[i  for x in film_id for i in resultaat if i[1][0] == x] 
        elif type(film_id)==int:
            resultaat_idorfilm=[i for i in resultaat if i[1][0]==film_id and type(film_id)==int]
        elif type(film_id)==str:
            resultaat_idorfilm=[i for i in resultaat if film_id in i[1][1] and type(film_id)==str]

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

def show_table_verkoop(lijst):
    x=PrettyTable()
    x.field_names=["Verkoop_ID", "ID_Vertoning","Tickets_kids","Tickets_standaard","Prijs"]
    x.add_rows(lijst)
    return x

def id_naar_titel(id):
    inventaris=get_inventory_list()
    for rij in inventaris:
        if rij[0] == id:
            return rij[1]

# ------------------ MYSQLITE FUNCTIONS ----------------


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

def insert_vertoning_database(ID_Film, Datum, Moment, DrieD, ID_Zaal):
    DrieD=True if DrieD=="Ja" else False

    con=sqlite3.connect('data/Databank.db')
    cur=con.cursor()
    cur.execute('INSERT INTO Vertoning (ID_Film,Datum,Moment,"3D",ID_Zaal) VALUES (?,?,?,?,?)',(ID_Film, Datum, Moment, DrieD, ID_Zaal))
    print(f"<green>De Film met titel '{kleur_goud(id_naar_titel(ID_Film))}' werd aan de database van vertoning toegevoegd!</green>")
    con.commit()
    con.close()
    druk_verder()


def insert_verkoop_database(ID_Vertoning, Tickets_kids, Tickets_standaard, Prijs):
    con=sqlite3.connect('data/Databank.db')
    cur=con.cursor()
    cur.execute('INSERT INTO Verkoop (ID_Vertoning,Tickets_kids,Tickets_standaard,Prijs) VALUES (?,?,?,?)',(ID_Vertoning, Tickets_kids, Tickets_standaard, Prijs))
    con.commit()
    con.close()

def delete_film_database(list):
    con=sqlite3.connect('data/Databank.db')
    cur=con.cursor()
    if len(list)==1:
        cur.execute(f'DELETE FROM Film WHERE ID_Film={list[0][0]}')
    else:
        for film in list:
            cur.execute(f'DELETE FROM Film WHERE ID_Film={film[0]}')
    con.commit()
    con.close()

def delete_vertoning_database(list):
    con=sqlite3.connect('data/Databank.db')
    cur=con.cursor()
    if len(list)==1: # één
        cur.execute(f'DELETE FROM Vertoning WHERE ID_Vertoning={list[0][0]}')
    elif len(list)>1: #alles
        for vertoning in list:
            cur.execute(f'DELETE FROM Vertoning WHERE ID_Vertoning={vertoning[0]}')
    con.commit()
    con.close()

def delete_verkoop_database(list):
    con=sqlite3.connect('data/Databank.db')
    cur=con.cursor()
    if len(list)==1:
        cur.execute(f'DELETE FROM Verkoop WHERE Verkoop_ID={list[0][0]}')
    else:
        for verkoop in list:
            cur.execute(f'DELETE FROM Verkoop WHERE Verkoop_ID={verkoop[0]}')
    con.commit()
    con.close()

# ------------------ FUNCTIONS SCENARIO ----------------


# ------------------ MAIN PAGE----------------
def menu_startpage():
    while True:
        clear_screen_logo()
        lijst=[f"{kleur_goud('Films')} bewerken",f"{kleur_goud('Vertoningen')} bewerken",f"{kleur_goud('Verkoop')} bewerken","<red>Afsluiten</red>"]
        keuze=(presentatie_main(lijst))
        if keuze==lijst[0]:
            menu_films_bewerken()
        elif keuze==lijst[1]:
            menu_vertoningen_bewerken()
            sleep(1)
        elif keuze==lijst[2]:
            menu_verkoop_bewerken()
            sleep(1)

        elif keuze==lijst[3]:
            clear_screen()
            print("Programma wordt afgesloten. Bedankt en tot de volgende keer.")
            print("<bg #000000>- Günes Topal</bg #000000>")
            print("<bg #FFDF00><fg #000000>versie: 1.0.3 - 2021/06/05</fg #000000></bg #FFDF00>")
            print("<bg #ED0000>gunes.topal@gmail.com</bg #ED0000>")
            sleep(2)
            exit()

# ------------------ MAIN VERKOOP----------------
def menu_verkoop_bewerken():
    while True:
        clear_screen()
        print("<bg #80C662><black>💲 VERKOOP 💲</black></bg #80C662>")
        lijst=["Tickets", "Wekelijkse ticketverkoop", "Omzet per film", "Terug"]
        keuze=(presentatie_main(lijst))
        if keuze==lijst[0]:
            menu_verkoop_tickets()
            continue
        if keuze==lijst[1]:
            menu_verkoop_wekelijks()
            continue
        if keuze==lijst[2]:
            menu_verkoop_omzet()
            continue
        if keuze==lijst[3]:
            menu_startpage()
def menu_verkoop_tickets():
    while True:
        clear_screen()
        print("<bg #80C662><black>💲 VERKOOP - tickets 💲</black></bg #80C662>")
        lijst=["Ticket verkopen", "Ticket zoeken", "Ticket verwijderen", "Terug"]
        keuze=(presentatie_main(lijst))
        if keuze==lijst[0]:
            menu_verkoop_tickets_verkopen()
            continue
        if keuze==lijst[1]:
            menu_verkoop_tickets_zoeken()
            continue
        if keuze==lijst[2]:
            menu_verkoop_tickets_verwijderen()
            continue
        if keuze==lijst[3]:
            menu_verkoop_bewerken()
def menu_verkoop_tickets_verkopen():
    print("Geef de id van vertoning:  ", end="")
    zoek=getInteger("",minima=1)
    allefilms=get_inventory_list()
    alleverkopen=get_verkoop_list()
    allevertoningen=get_vertoning_list()
    allezalen=get_zaal_list()
    zetelstotaal=""

    prijs=0
    info={}
    ticket={}
    for i in allevertoningen:
        if i[0]==zoek:
            info["ID_Vertoning"]=i[0]
            info["Titel"]= i[1][1]
            info["ID_Film"]= i[1][0]
            for film in allefilms:
                if film[0] == i[1][0]:
                    info["Duur"] = film[2]
                    info["3D"]="Ja" if film[5]=="Ja" else "Nee"
                    info["KNT"]= "Ja" if film[3]=="Ja" else "Nee"
            info["Datum"]=i[2] 
            info["Moment"]=i[3]
            info["Zaal"]=i[5]

    for j in allezalen:
        if j[0]==info["Zaal"]:
            zetelstotaal=j[2]

    for k in alleverkopen:
        if k[1]==info["ID_Vertoning"]:
            zetelstotaal=zetelstotaal-k[2]
            zetelstotaal=zetelstotaal-k[3]

    if zetelstotaal!=0:
        if len(info)!=0:
            print()
            print("Ticket verkoop voor de film:")
            print(kleur_goud("Titel:"), info["Titel"])
            print(kleur_goud("Speelduur:"), info["Duur"])
            print(kleur_goud("Datum:"), info["Datum"], "om", info["Moment"])
            print(kleur_goud("Zaal:"), info["Zaal"])
            print(kleur_goud("In 3D") if info["3D"]=="Ja" else "")
        else:
            print("<red>Geen resultaat gevonden.</red>")
            sleep(1)        
            return

        print()

        ticket['ID_Vertoning']=zoek
        ticket['3D']=prijs_ticket['3D'] if info["3D"]=="Ja" else 0
        ticket['Langspeel']=prijs_ticket['langspeel'] if info["Duur"]>120 else 0

        print(f"Er zijn {zetelstotaal} plaatsen vrij voor deze vertoning.")
        print("Aantal volwassenen?  ", end="")
        ticket['standaard']=getInteger("",minima=0,maxima=zetelstotaal)
        zetelstotaal-=ticket['standaard']


        if info["KNT"]== "Ja" or zetelstotaal==0: #Geen vraag voor tickets kinderen als het een mature film is
            ticket['kids']=0

        else:
            print("Aantal kinderen?  ", end="")
            ticket['kids']=getInteger("",minima=0,maxima=zetelstotaal)



        if info["KNT"]== "Ja": 
            prijs= (ticket['standaard'] * (prijs_ticket['standaard']+ticket['3D']+ticket['Langspeel']))
        else:
            prijs= (ticket['standaard'] * (prijs_ticket['standaard']+ticket['3D']+ticket['Langspeel'])) + (prijs_ticket['kids']+ticket['kids'] * (ticket['3D']+ticket['Langspeel']))


        print("De <u>totale kost</u> voor deze verkoop is € {:.2f}".format(prijs))
        antwoord=druk_neeja()
        if antwoord:
            insert_verkoop_database(zoek, ticket['kids'], ticket['standaard'], prijs)
            print(f"<green>Ticket nummer {kleur_goud(zoek)} is bevestigd! </green>")
            sleep(0.5)
            print(f"De ticket wordt afgedrukt..")
            sleep(1.5)
            print(f"Geniet van de film!")
            print(f"Er zijn {zetelstotaal} plaatsen vrij voor deze vertoning.")        
    else:
        print("Onze excuses, er zijn voor deze vertoning geen plaatsen meer beschikbaar.")
    druk_verder()
def menu_verkoop_tickets_zoeken():
    print("Geef de id van het ticket:")
    zoek=getInteger("",minima=1)
    alletickets=get_verkoop_list()
    allevertoningen=get_vertoning_list()
    info=[]
    for i in alletickets:
        if i[0]==zoek:
            print("<blue>Gegevens ticket:</blue>")
            print(f"{kleur_goud('ID:')}{i[0]}")
            for vertoning in allevertoningen:
                if vertoning[0] == i[1]:
                    info.append(f"{kleur_goud('Film:')} {vertoning[1][1]}") 
                    info.append(f"op <u>{vertoning[2]}</u> om {vertoning[3]} uur in zaal {vertoning[5]}")
                    info.append(f"in 3D." if vertoning[4]=="Ja" else "zonder 3D.")
            info.append(f"{kleur_goud('Omschrijving:')}")
            info.append(f"{i[3]} standaard {'tickets' if i[3]!=1 else 'ticket'}")
            info.append(f"{i[2]} kinder {'tickets' if i[2]!=1 else 'ticket'}")
            info.append("Prijs: € {:.2f}".format(i[4]))
    if len(info)!=0:
        for toon in info:
            print(toon)
    else:
        print("<red>Geen resultaat gevonden.</red>")
        sleep(1)
    druk_verder()
def menu_verkoop_tickets_verwijderen():
    while True:

        print("Geef de id van het ticket:")
        zoek=getInteger("",minima=1)
        alletickets=get_verkoop_list()
        allevertoningen=get_vertoning_list()
        try:
            resultaat=[i for i in alletickets if i[0]==zoek]
            break
        except ValueError:
            print("Fout")
            continue
    print(f'U staat op het moment om de ticket met nummer "{kleur_goud(zoek)}" te wissen.')
    for i in alletickets:
        if i[0]==zoek:
            print("<blue>Gegevens ticket:</blue>")
            print(f"{kleur_goud('ID:')}{i[0]}")
            for vertoning in allevertoningen:
                if vertoning[0] == i[1]:
                    print(f"{kleur_goud('Film:')} {vertoning[1][1]}") 
                    print(f"op <u>{vertoning[2]}</u> om {vertoning[3]} uur in zaal {vertoning[5]}")
                    print(f"in 3D." if vertoning[4]=="Ja" else "zonder 3D.")
            print(f"{kleur_goud('Omschrijving:')}{i[0]}")
            print(f"{i[3]} standaard {'tickets' if i[3]!=1 else 'ticket'}")
            print(f"{i[2]} kinder {'tickets' if i[2]!=1 else 'ticket'}")
            print("Prijs: € {:.2f}".format(i[4]))
    antwoord=druk_neeja()
    if antwoord:
        delete_verkoop_database(resultaat)
        print(f"<red>Ticket nummer {kleur_goud(zoek)} werd gewist!</red>")
    druk_verder()
    



def menu_verkoop_wekelijks():
    while True:
        clear_screen()
        print("<bg #80C662><black>💲 VERKOOP - cijfers 💲</black></bg #80C662>")
        lijst=["Cijfers per week", "Tickets per film per week", "Terug"]
        keuze=(presentatie_main(lijst))
        if keuze==lijst[0]:
            menu_verkoop_cijfers_week()
            continue
        if keuze==lijst[1]:
            menu_verkoop_cijfers_filmweek()
            continue
        if keuze==lijst[2]:
            menu_verkoop_bewerken()
def menu_verkoop_cijfers_week():
    pass
def menu_verkoop_cijfers_filmweek():
    pass


def menu_verkoop_omzet():
    while True:
        clear_screen()
        print("<bg #80C662><black>💲 VERKOOP - omzet 💲</black></bg #80C662>")
        lijst=["Totale omzet per film", "Records", "Terug"]
        keuze=(presentatie_main(lijst))
        if keuze==lijst[0]:
            menu_verkoop_omzet_film()
            continue
        if keuze==lijst[1]:
            menu_verkoop_omzet_records()
            continue
        if keuze==lijst[2]:
            menu_verkoop_bewerken()
def menu_verkoop_omzet_film():
    pass
def menu_verkoop_omzet_records():
    pass





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
        loop=False
# Zaalkeuze !!!!!!!!!!!!
        zaal=getInteger("Zaal id: ",0,7)
    # controle als 3D film in een 3D zaal kan afspelen
        if zaal==0:
            return
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
                break

        print("hier")
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
    if delete and len(get_vertoning_list(datum,None,None))!=0:
        lijst=["<red>Verwijder</red> één vertoning","<red>Verwijderen</red> alle vertoningen","<fg #00BAFF>Annuleren</fg #00BAFF>"]
        keuze=presentatie_main(lijst)
        if keuze==lijst[0]:
            vrwkeuze=[(presentatie_main(resultaat, 1))]
            antwoord=druk_neeja()
            if antwoord:
                print(f"De vertoning")
                print(f"id: {vrwkeuze[0][1][0]} titel: '{vrwkeuze[0][1][1]}'")
                print(f"Datum: {vrwkeuze[0][2]} om {vrwkeuze[0][3]}")
                print(f"{'<green>Met 3D</green>' if vrwkeuze[0][4]=='Ja' else 'Zonder 3D'}")
                print(f"Zaal: {vrwkeuze[0][5]}")
                print(f"<red>...werd van de database verwijderd!</red>")
                delete_vertoning_database(vrwkeuze)
                druk_verder()
        elif keuze==lijst[1]:
            antwoord=druk_neeja()
            if antwoord:
                print(f"<red>Alle vertoningen zijn verwijderd!</red>")
                delete_vertoning_database(resultaat) 
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
        zoek=(int(zoek) if zoek[0] in ['0','1','2','3','4','5','6','7','8','9'] else str(zoek))
        resultaat=get_vertoning_list(None,zoek,None)
        if len(resultaat)==0:
            print("<red>Geen resultaat gevonden.</red>")
            sleep(1)
            druk_verder() if delete else None

        else:
            print(show_table_vertoning(get_vertoning_list(None,zoek,None)))
        break
    if not delete:
        druk_verder()
    if delete and len(resultaat)!=0:
        lijst=["<red>Verwijder</red> één vertoning","<red>Verwijderen</red> alle vertoningen","<fg #00BAFF>Annuleren</fg #00BAFF>"]
        keuze=presentatie_main(lijst)
        if keuze==lijst[0]:
            vrwkeuze=[(presentatie_main(resultaat, 1))]
            print(vrwkeuze)
            antwoord=druk_neeja()
            if antwoord:
                print(f"De vertoning")
                print(f"id: {vrwkeuze[0][1][0]} titel: '{vrwkeuze[0][1][1]}'")
                print(f"Datum: {vrwkeuze[0][2]} om {vrwkeuze[0][3]}")
                print(f"{'<green>Met 3D</green>' if vrwkeuze[0][4]=='Ja' else 'Zonder 3D'}")
                print(f"Zaal: {vrwkeuze[0][5]}")
                print(f"<red>...werd van de database verwijderd!</red>")
                delete_vertoning_database(vrwkeuze) 
        elif keuze==lijst[1]:
            print(resultaat)
            antwoord=druk_neeja()
            if antwoord:
                print(f"<red>Alle vertoningen zijn verwijderd!</red>")
                delete_vertoning_database(resultaat) 
        elif keuze==lijst[2]:
            return

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
    
        if len(resultaat)>1 and len(resultaat)<=5:
            print(f"Er zijn {len(resultaat)} resultaten.")
            print(f'U staat op het moment om de films met titels:')
            print('-'*20)
            for titel in resultaat:
                print(titel[1])
            print('-'*20)
            print("te verwijderen.")
        else:
            print(f'U staat op het moment om de film met titel "{kleur_goud(resultaat[0][1])}" te wissen.')

# Wat als de film die je wil verwijderen nog vertoont zal worden?
        idfilm=[x[0] for x in resultaat]
        print()
        geplandevertoning=[]
        for x in idfilm:
            if len(get_vertoning_list(datum=None,film_id=x, zaal=None)) ==1:
                geplandevertoning.append(get_vertoning_list(datum=None,film_id=x, zaal=None)[0])
                print(f"{kleur_goud(1)} vertoning van {kleur_goud(id_naar_titel(x))}.")
            else:
                for item in get_vertoning_list(datum=None,film_id=x, zaal=None):
                    geplandevertoning.append(item)
                print(f"{kleur_goud(len(get_vertoning_list(datum=None,film_id=x, zaal=None)))} vertoningen van {kleur_goud(id_naar_titel(x))}.")

        print()


        if len(geplandevertoning)==1:
            print(f"<red>Er is {kleur_goud(len(geplandevertoning))} vertoning met die film.</red>")
            print(f"Wilt u de gekozen film met zijn vertoning(en) verwijderen?")
        else:
            if len(geplandevertoning)>1:
                print(f"<red>Als u bevestigt, worden er in het totaal {kleur_goud(len(geplandevertoning))} vertoningen samen met de films verwijderd !!!</red>")
                print(f"Wilt u de gekozen films met hun vertoningen verwijderen?")
            if len(geplandevertoning)==0:
                print(f"Wilt u de gekozen film verwijderen?")
        antwoord=druk_neeja()
        if antwoord:
            delete_vertoning_database(geplandevertoning)
            delete_film_database(resultaat)
        
        druk_verder()

menu_startpage()
# menu_verkoop_tickets_verkopen()
