# from subprocess import run
from re import A, I
import PySimpleGUI as gui
from PIL import Image
import os, io
import urllib.request
import sqlite3
from datetime import datetime
from time import sleep
from ansimarkup import ansiprint as print
from db.databasemanager import *
from tools.movie_request import vind_film_via_imdb

# Documentatie: https://pysimplegui.readthedocs.io/en/latest/call%20reference/

# ------------------ MISC ----------------
gui.theme('LightBlue4')


# ------------------ CUSTOM FUNCTIONS ----------------

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

def insert_verkoop_database(ID_Vertoning, Tickets_kids, Tickets_standaard, Prijs):
    con=sqlite3.connect('data/Databank.db')
    cur=con.cursor()
    cur.execute('INSERT INTO Verkoop (ID_Vertoning,Tickets_kids,Tickets_standaard,Prijs) VALUES (?,?,?,?)',(ID_Vertoning, Tickets_kids, Tickets_standaard, Prijs))
    con.commit()
    con.close()

def lijsturl_naar_lijstimagegui(lijst, x=150, y=150, sleutel="POSTER"): #neemt de lijst met (meerdere) URL's, steekt die in een ander lijst als GUIimage object en geeft het een automatische key met nummer
    #lijst vb: [14, 'Back to the Future', 116, 'Nee', 'https://image.tmdb.org/t/p/original/fNOH9f1aA7XRTzl1sAOx9iF553Q.jpg', 'tt0088763']
    posters=[]
    if len(lijst) > 1:
        for item in lijst:
            urllib.request.urlretrieve(item[4],"URL")
            image = Image.open("URL")
            image.thumbnail((x, y))
            bio = io.BytesIO()
            image.save(bio, format="PNG")
            gegevens=bio.getvalue()
            posters.append([gui.Image(data=gegevens, key=f"-{sleutel}{lijst.index(item)+1}-", enable_events=True)])
    else:
            urllib.request.urlretrieve(lijst[0][4],"URL")
            image = Image.open("URL")
            image.thumbnail((x, y))
            bio = io.BytesIO()
            image.save(bio, format="PNG")
            gegevens=bio.getvalue()
            posters.append([gui.Image(data=gegevens)])#, key=f"-{key}-", enable_events=True)])
    return posters 

# ------------------ WINDOW 0 ----------------
def win0():
    layout0=[
        [gui.Image('data/splash.png')],
        [gui.Button('', key='-LADEN-', visible=False)]
    ]

    window0= gui.Window('Window Title', [[gui.Image('data/splash.png')]], transparent_color=gui.theme_background_color(), no_titlebar=True, keep_on_top=True)
    return window0


# ------------------ WINDOW 1 ----------------
def win1(lijst): #rijen met max 4 posters naast elkaar
    #vb: lijst= [[14, 'Back to the Future', 116, 'Nee', 'https://image.tmdb.org/t/p/original/fNOH9f1aA7XRTzl1sAOx9iF553Q.jpg', 'tt0088763'],...]
    rij1=[]
    rij2=[]
    rij3=[]
    rij4=[]
    images=lijst
    for i in images:
        if images.index(i)<4:
            rij1+=i
        elif images.index(i)<8 and images.index(i)>3:
            rij2+=i
        elif images.index(i)<12 and images.index(i)>7:
            rij3+=i
        elif images.index(i)<16 and images.index(i)>11:
            rij4+=i

    layout=[
        [gui.Image('data/logo_cinemax.png')],
        [gui.Column([rij1])],
        [gui.Column([rij2])],
        [gui.Column([rij3])],
        [gui.Column([rij4])]
    ]
    window = gui.Window("Cinemax", layout,size=(550, 650), element_justification = "center")
    return window

# ------------------ WINDOW 2 ----------------#TODO: hier is something wrong
def win2(lijst): # lijst vb: [14, 'Back to the Future', 116, 'Nee', 'https://image.tmdb.org/t/p/original/fNOH9f1aA7XRTzl1sAOx9iF553Q.jpg', 'tt0088763']
    info=[]
    titel=lijst[1]
    for i in allevertoningen:
        if i[1][1]==titel and i[2]==vandaag_datum:
            vertoningid=i[0]
            datum=i[2]
            moment=i[3]
            zaal=i[5]
            DrieD='.' if i[4]=='Nee' else ' in 3D.'
            info.append(f"{datum} om {moment} uur in zaal {zaal}{DrieD}")

    tijd_uur=int(lijst[2]/60)
    tijd_minuut=lijst[2]-(tijd_uur*60)
    kolom3=[[gui.Text(lijst[1], font = ("Arial, 16"))], [gui.Text(f"{tijd_uur} u {tijd_minuut} min")], [gui.Text(vind_film_via_imdb(lijst[5])['Beschrijving'],size=(30,10))]]
    kolom6=[[gui.Button('Terug naar films', key='-TERUG-')]]
    kolom7=[[gui.Button('Vertoning kiezen', key='-KIEZEN-', disabled=True)]]    
    kolom5=[[gui.Column(kolom6, element_justification="left"),gui.Column(kolom7, element_justification="right")]]
    kolom4=[[gui.Listbox(info, size=(38, 5), key="-infofilm-", enable_events=True)], [gui.Column(kolom5)]]
    kolom2=[[gui.Column(kolom3)], [gui.Column(kolom4)]]

    gegevens=lijsturl_naar_lijstimagegui([lijst], x=500, y=500)
    layout=[[gegevens[0][0], gui.Column(kolom2)]]
    window = gui.Window("Cinemax", layout,size=(700, 600), element_justification = "center")
    return window 

# ------------------ WINDOW 3 ----------------
def win3(lijst):
    pass


# ------------------ CUSTOM VARIABLES ----------------
vandaag=datetime.now()
vandaag_datum='06/06/2021'#vandaag.strftime("%d/%m/%Y")
vandaag_tijd=vandaag.strftime("%H:%M")
vandaag_jaar=vandaag.strftime("%Y")
vandaag_maand_getal=vandaag.strftime("%M")
vandaag_week=vandaag.strftime("%W")
prijs_ticket={'standaard':9,'kids':7,'langspeel':1,'3D':1.5}

allevertoningen=get_vertoning_list() #vb: [7, (1, 'Forrest Gump'), '04/06/2021', '10:00', 'Nee', 7]
alleverkopen=get_verkoop_list() #vb: [1, 1, 2, 2, 32.0]
allefilms=get_inventory_list() #vb: [18, 'Alien', 122, 'Ja', 'tt2316204', 'Nee']

titel=[""]
datum=""
moment=""
zaal=""
DrieD=""
#TODO: CHECK VARIABLES



huidigevertoning=[vertoning for vertoning in allevertoningen if vertoning[2]=="06/06/2021"]#vandaag_datum] vb: [7, (1, 'Forrest Gump'), '04/06/2021', '10:00', 'Nee', 7]
lijstfilms=[(vertoning[1][0],vertoning[1][1]) for vertoning in huidigevertoning] #vb:[(18, 'Alien')]
films=[i[1] for i in lijstfilms]
korteinfofilms=[[f[0], f[1], k[2],k[3],k[4]] for k in allefilms for f in lijstfilms if k[0] == f[0] ] #vb: [[18, 'Alien', 122, 'Ja', tt2316204]]
gegevensfilms=[] #vb: [14, 'Back to the Future', 116, 'Nee', 'https://image.tmdb.org/t/p/original/fNOH9f1aA7XRTzl1sAOx9iF553Q.jpg', 'tt0088763']
info=[]



# ------------------ SHOWTIME ----------------
window=win0()
while True:
    event, values =window.read(timeout=10)
    if event == None:
        break
    else:
        postersfilms=[vind_film_via_imdb(k[4])['Poster_link'] for k in korteinfofilms] #via imdb-id wordt de link naar de poster gehaald
        for nummer in range (len(korteinfofilms)):
            korteinfofilms[nummer].insert(-1,postersfilms[nummer]) #de link naar de poster wordt bij de details van films in vertoning toegevoegd
        gegevensfilms=controle_dubbels(korteinfofilms) #dubbels worden verwijderd
        reclame=lijsturl_naar_lijstimagegui(gegevensfilms, x=150,y=150) #posters (in jpg) worden omgebouwd (naar png) en de data wordt als imagegui opgeslagen in de lijst 'posters'
        break
window.close()


window=win1(reclame)
while True:
    event, values = window.read()
    if event == gui.WIN_CLOSED:
        break
    if event == "-POSTER1-":
        window.close()
        window=win2(gegevensfilms[0])#De eerst film links boven

    if event == "-POSTER2-":
        window.close()
        window=win2(gegevensfilms[1])

    if event == "-POSTER3-":
        window.close()
        window=win2(gegevensfilms[2])

    if event == "-POSTER4-":
        window.close()
        window=win2(gegevensfilms[3])

    if event == "-POSTER5-":
        window.close()
        window=win2(gegevensfilms[4])
    if event == "-POSTER6-":
        window.close()
        window=win2(gegevensfilms[5])
    if event == "-POSTER7-":
        window.close()
        window=win2(gegevensfilms[6])
    if event == "-POSTER8-":
        window.close()
        window=win2(gegevensfilms[7])
    if event == "-POSTER9-":
        window.close()
        window=win2(gegevensfilms[8])
    if event == "-POSTER10-":
        window.close()
        window=win2(gegevensfilms[9])

    if event == '-KIEZEN-':
        window.close()
        window=win3(reclame)

    if event =='-TERUG-':
        window.close()
        window=win1(reclame)

    if event == '-infofilm-':
        window['-KIEZEN-'].update(disabled=False)
window.close()