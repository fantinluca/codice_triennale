import csv

with open('padua_weather.csv', 'r', newline='') as csvfile:
    csvreader = csv.reader(csvfile)
    print("PRIMA RIGA: ")
    print(next(csvreader))
    print("ALTRE RIGHE:")
    for row in csvreader:
        print(row)