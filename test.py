import sqlite3
from models.clsFilm import Film
from models.clsVerkoop import Verkoop
from models.clsVertoning import Vertoning
from models.clsZaal import Zaal


def sql_film_database():
    conn=sqlite3.connect('data/Databank.db')
    cursor=conn.cursor()
    cursor.execute('SELECT * FROM Film')
    record=cursor.fetchall()
    conn.commit()
    conn.close()
    resultaat=[]
    for rij in record:
        resultaat.append(Film(rij[0], rij[1], rij[2], rij[3], rij[4], rij[5], rij[6], rij[7]))
    return resultaat

def sql_zaal_database():
    conn=sqlite3.connect('data/Databank.db')
    cursor=conn.cursor()
    cursor.execute('SELECT * FROM Zalen')
    record=cursor.fetchall()
    conn.commit()
    conn.close()
    resultaat=[]
    for rij in record:
        resultaat.append(Zaal(rij[0], rij[1], rij[2]))
    return resultaat

def sql_vertoning_database():
    conn=sqlite3.connect('data/Databank.db')
    cursor=conn.cursor()
    cursor.execute('SELECT * FROM Vertoning')
    record=cursor.fetchall()
    conn.commit()
    conn.close()
    resultaat=[]
    for rij in record:
        print(rij)
        resultaat.append(Vertoning(rij[0], rij[1], rij[2], rij[3], rij[4], rij[5]))
    return resultaat


def sql_Verkoop_database():
    conn=sqlite3.connect('data/Databank.db')
    cursor=conn.cursor()
    cursor.execute('SELECT * FROM Verkoop')
    record=cursor.fetchall()
    conn.commit()
    conn.close()
    resultaat=[]
    for rij in record:
        resultaat.append(Verkoop(rij[0], rij[1], rij[2], rij[3], rij[4]))
    return resultaat

print("<b>Zoek film(s) via titel of imdb: (Gebruik + voor meerdere films)</b> ", end="")
gegevens=input("")
zoek = gegevens.split("+")

print(zoek)  