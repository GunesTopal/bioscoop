from subprocess import run
import PySimpleGUI as gui
import sqlite3
from datetime import datetime
from time import sleep
import os, sys
from db.databasemanager import *

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

films=[vertoning[1][1] for vertoning in allevertoningen if vertoning[2]=="06/06/2021"]#vandaag_datum]
films=controle_dubbels(films)


# ------------------ WINDOW 1 ----------------

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
    [gui.Column(kolom1, vertical_alignment="top"), gui.Column(kolom2, vertical_alignment="top")],
]
window1 = gui.Window("Cinemax", layout,size=(635, 330))

while True:
    event, values = window1.read()
    if event == '-films-':
        info=[]
        for i in allevertoningen:
            if i[1][1]==values['-films-'][0] and i[2]==vandaag_datum:
                vertoningid=i[0]
                info.append(f"{i[2]} om {i[3]} uur in zaal {i[5]}{'.' if i[4]=='Nee' else ' in 3D.'}")
        window1["-infofilm-"].update(values=info)
    if values['-films-'] and values["-infofilm-"] and (values['-SPINVOLWASSENEN-']!='0' or values['-SPINKINDEREN-']!='0'):
        window1['-KNOP-'].update(disabled=False)

    if (event == '-SPINVOLWASSENEN-' or event == '-SPINKINDEREN-') and (values['-SPINVOLWASSENEN-']!='0' or values['-SPINKINDEREN-']!='0'):
        prijs= (float(values['-SPINVOLWASSENEN-']) * (prijs_ticket['standaard']+prijs_ticket['3D']+prijs_ticket['langspeel']) + float(values['-SPINKINDEREN-']) * (prijs_ticket['standaard']+prijs_ticket['3D']+prijs_ticket['langspeel']))
        window1['-PRIJS-'].update(value=prijs)

 
    if values['-SPINVOLWASSENEN-']=='0' and values['-SPINKINDEREN-']=='0' or values["-infofilm-"]=='':
        window1['-PRIJS-'].update(value="")
        window1['-KNOP-'].update(disabled=True)            

    if  event == '-KNOP-':
        window1['-PRIJS-'].update(value="")
        window1['-SPINVOLWASSENEN-'].update(value="0")
        window1['-SPINKINDEREN-'].update(value='0')
        insert_verkoop_database(vertoningid, values['-SPINKINDEREN-'], values['-SPINVOLWASSENEN-'], prijs)
        window1['-KNOP-'].update(disabled=True)
        break

    if event == '-Exit-' or event == gui.WIN_CLOSED:
        break
window1.close()

# ------------------ WINDOW 2 ----------------
layout=[
    [gui.Text('Geniet van de film!', font=('arial', 15))],
    [gui.Button('OK', key='-OK-', enable_events=True)]
]
window2= gui.Window("Success!",layout, size=(200,100))

while True:
    event, values = window2.read()
    if event['-OK-']:
        main()
    if event == '-Exit-' or event == gui.WIN_CLOSED:
        break
window2.close()