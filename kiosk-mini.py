from subprocess import run
import PySimpleGUI as gui
import sqlite3
from datetime import datetime
from time import sleep
from ansimarkup import ansiprint as print
from db.databasemanager import *
from tools.movie_request import vind_film_via_imdb

# Documentatie: https://pysimplegui.readthedocs.io/en/latest/call%20reference/

# ------------------ MISC ----------------
gui.theme('LightBrown8')

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

#TODO:check variabel
huidigevertoning=[vertoning for vertoning in allevertoningen if vertoning[2]=="06/06/2021"]#vandaag_datum] vb: [7, (1, 'Forrest Gump'), '04/06/2021', '10:00', 'Nee', 7]
lijstfilms=[(vertoning[1][0],vertoning[1][1]) for vertoning in huidigevertoning] #vb:[(18, 'Alien')]
gegevensfilms=[(f[0], f[1], k[2],k[3],k[4]) for k in allefilms for f in lijstfilms if k[0] == f[0] ] #vb: [(18, 'Alien', 122, 'Ja', tt2316204)]
films=[i[1] for i in lijstfilms]



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

# ------------------ WINDOW 1 ----------------
def win1():
    kolom3=[
        [gui.Text('Aantal Volwassenen:')],
        [gui.Text('Aantal Kinderen:', key='-AANTAL_KINDEREN-')],
        [gui.Text('Prijs')],
        [gui.Button('Tickets kopen', key='-KNOP-', enable_events=True, disabled=True)]
    ]
    kolom4=[
        [gui.Spin([str(i) for i in range(11)], key='-SPINVOLWASSENEN-', initial_value="0",enable_events=True)],
        [gui.Spin([str(i) for i in range(11)], key='-SPINKINDEREN-',initial_value="0", enable_events=True)],
        [gui.Text('', size=(5,1),key='-PRIJS-', enable_events=True)]
    ]
    kolom1=[
        [gui.Listbox(films, size=(38, 13), key="-films-", enable_events=True)]
    ]
    kolom2=[
        [gui.Text('Vertoningen')],
        [gui.Listbox("", size=(38, 5), key="-infofilm-", enable_events=True)],
        [gui.Column(kolom3, vertical_alignment="top"),gui.Column(kolom4,vertical_alignment="top")]
    ]
    kolom5=[
        [gui.Image('data/logo_cinemax.png')]
    ]

    kolom8=[
        [gui.Text("",size=(8,1),key='-DUUR-')]
    ]

    kolom9=[
        [gui.Text("KINDEREN NIET TOEGELATEN",key='-KNT-',text_color="green", enable_events=True)]
    ]

    kolom7=[
        [gui.Column(kolom8, vertical_alignment="top", justification="left"), gui.Column(kolom9, vertical_alignment="top")]
    ]

    kolom6=[
        [gui.Column(kolom7, vertical_alignment="top")],
        [gui.Text("Het gevecht tussen detective Hoffman en Jill Tuck duurt voort. Ondertussen ontmoeten een aantal overleevenden van de spelletjes van Jigsaw, waaronder Dr. Lawrence Gordon, elkaar bij een sessie van Bobby Dagen, die beweert zelf ook een overlevende van Jigsaw te zijn. Maar dan wordt Bobby ontvoerd en zal hij een serie tests moeten afleggen om zijn vrienden en uiteindelijk zijn vrouw te redden.", key='-OMSCHRIJVING-', size=(45,10))]

    ]





    layout = [
        [gui.Column(kolom5, justification="center")],
        [gui.Column(kolom1, vertical_alignment="top"), gui.Column(kolom2, vertical_alignment="top")],
        [gui.Frame("",kolom6, key='-FRAME-',border_width=3, visible=False)]#[gui.Column(kolom6, justification="center", size=(200,200))],
    ]
    window1 = gui.Window("Cinemax", layout,size=(635, 630), element_justification = "center")
    return window1

# ------------------ WINDOW 2 ----------------
def win2():
    kolom6=[
        [gui.Text('Geniet van de film!', font=('arial', 15))],
        [gui.Text(titel, font=('arial', 10))],
        [gui.Text(f"{datum}", font=('arial', 10))], 
        [gui.Text(f"om {moment} uur", font=('arial', 10))], 
        [gui.Text(f"in zaal {zaal}", font=('arial', 10)),], 
        [gui.Text(f"{DrieD}", font=('arial', 10))],
        [gui.Button('OK', key='-OK2-', enable_events=True)]
    ]
    layout2=[
        [gui.Column(kolom6, element_justification="center")]
    ]

    window2= gui.Window("Success!",layout2, size=(220,220))
    return window2


# ------------------ VARIABLES WITH FUNCTIONS ----------------
films=controle_dubbels(films)
window1=win1()

# ------------------ SHOWTIME ----------------
while True:
    event, values = window1.read()
    if event == '-films-':
        window1["-FRAME-"].update(visible=True)
        info=[]
        titel=values['-films-'][0]
        for i in allevertoningen:
            if i[1][1]==values['-films-'][0] and i[2]==vandaag_datum:
                vertoningid=i[0]
                datum=i[2]
                moment=i[3]
                zaal=i[5]
                DrieD='.' if i[4]=='Nee' else ' in 3D.'
                info.append(f"{datum} om {moment} uur in zaal {zaal}{DrieD}")
        
        window1["-FRAME-"].update(value=titel)
        imdb=[i[4] for i in gegevensfilms if i[1]==titel]
        proef=vind_film_via_imdb(imdb[0])
        omschrijving=proef["Beschrijving"]
        window1["-OMSCHRIJVING-"].update(value=omschrijving)

        for i in gegevensfilms:
            if i[1]==titel:
                duur=i[2]
        window1["-DUUR-"].update(value=f"{duur} min.")

        for i in gegevensfilms:
            if i[1]==titel:
                KNT=i[3]
        if KNT=='Ja':

            window1["-AANTAL_KINDEREN-"].update(visible=False)
            window1["-SPINKINDEREN-"].update(visible=False)
        else:

            window1["-AANTAL_KINDEREN-"].update(visible=True)
            window1["-SPINKINDEREN-"].update(visible=True)
        window1["-KNT-"].update(text_color='red' if KNT=='Ja' else 'green')
        window1["-KNT-"].update(value=f"{'KINDEREN NIET TOEGELATEN' if KNT=='Ja' else 'KINDEREN TOEGELATEN'}")
        window1["-infofilm-"].update(values=info)


    if (event == '-SPINVOLWASSENEN-' or event == '-SPINKINDEREN-'):
        if (values['-SPINVOLWASSENEN-']!='0' or values['-SPINKINDEREN-']!='0'):
            window1['-KNOP-'].update(disabled=False)
            prijs= "€ {:.2f}".format((float(values['-SPINVOLWASSENEN-']) * (prijs_ticket['standaard']+prijs_ticket['3D']+prijs_ticket['langspeel']) + float(values['-SPINKINDEREN-']) * (prijs_ticket['standaard']+prijs_ticket['3D']+prijs_ticket['langspeel'])))
            window1['-PRIJS-'].update(value=prijs)
        elif (values['-SPINVOLWASSENEN-']=='0' and values['-SPINKINDEREN-']=='0'):# or not values["-infofilm-"] :
            window1['-KNOP-'].update(disabled=True)
            window1['-PRIJS-'].update(value="")
                    

    if  event == '-KNOP-':
        insert_verkoop_database(vertoningid, values['-SPINKINDEREN-'], values['-SPINVOLWASSENEN-'], prijs)
        window2=win2()
        while True:
            event, values = window2.read()
            window2.close()
            break


        window1=win1()
        # window2=win2()
        # while True:
        #     event, values = window2.read()
        #     if event == '-OK2-':
        #         window1=win1()
        #         window2.close()
        #         break
        #     if event == gui.WIN_CLOSED:
        #         window1=win1()
        #         window2.close()
        #         break

    if event == gui.WIN_CLOSED:
        break

window1.close()