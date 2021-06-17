from subprocess import run
import PySimpleGUI as gui
import sqlite3
from datetime import datetime
from time import sleep
from db.databasemanager import *
# Documentatie: https://pysimplegui.readthedocs.io/en/latest/call%20reference/




# ------------------ MISC ----------------
gui.theme('GreenTan')

# ------------------ CUSTOM VARIABLES ----------------
vandaag=datetime.now()
vandaag_datum=vandaag.strftime("%d/%m/%Y")
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

films=[vertoning[1][1] for vertoning in allevertoningen if vertoning[2]==vandaag_datum]


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
        [gui.Text('Aantal Kinderen:')],
        [gui.Text('Prijs')],
        [gui.Button('Tickets kopen', key='-KNOP-', enable_events=True, disabled=True)]
    ]
    kolom4=[
        [gui.Spin([str(i) for i in range(11)], key='-SPINVOLWASSENEN-', enable_events=True)],
        [gui.Spin([str(i) for i in range(11)], key='-SPINKINDEREN-', enable_events=True)],
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
    layout = [
        [gui.Column(kolom5, justification="center")],
        [gui.Column(kolom1, vertical_alignment="top"), gui.Column(kolom2, vertical_alignment="top")]
    ]
    window1 = gui.Window("Cinemax", layout,size=(635, 330))
    return window1

# ------------------ VARIABLES WITH FUNCTIONS ----------------
films=controle_dubbels(films)
window1=win1()

# ------------------ SHOWTIME ----------------
while True:
    event, values = window1.read()
    if event == '-films-':
        info=[]
        for i in allevertoningen:
            if i[1][1]==values['-films-'][0] and i[2]==vandaag_datum:
                vertoningid=i[0]
                datum=i[2]
                moment=i[3]
                zaal=i[5]
                DrieD='.' if i[4]=='Nee' else ' in 3D.'
                info.append(f"{datum} om {moment} uur in zaal {zaal}{DrieD}")
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
        window1=win1()

    if event == gui.WIN_CLOSED:
        break

window1.close()