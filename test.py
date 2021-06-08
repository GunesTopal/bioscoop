from datetime import datetime, timedelta
week='22'
year='2021'
date=datetime.strptime(year,"%Y")

for i in range (365):
    date=date+timedelta(days=1)
    if date.strftime('%W')==week:
        print(date.strftime('%d/%m/%Y'))
        continue