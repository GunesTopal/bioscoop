from datetime import datetime, timedelta

def datumsvoorweek(week,jaar): #Neemt week bv '04' en maakt een list van datums ('25/01/2021', '26/01/2021', '27/01/2021', '28/01/2021', '29/01/2021', '30/01/2021', '31/01/2021') -> 
    week=str(week)
    if len(week)==1:
        week='0'+week
    year=str(jaar)
    date=datetime.strptime(year,"%Y")
    resultaat=[]
    for i in range (365):
        date=date+timedelta(days=1)
        if date.strftime('%W')==week:
            resultaat.append(date.strftime('%d/%m/%Y'))
    return resultaat

datumsinweken={}
for weeknummer in range(53):
    datumsinweken[weeknummer]=datumsvoorweek(weeknummer,2021)
# print(datumsinweken)

datum='01/05/2021'

for i in datumsinweken:
    print(datumsinweken.get(i))
    # if datum in list(i.values()):
    #     print('yup', i)