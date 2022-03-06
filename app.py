import requests
import csv
from flask import Flask, render_template, request
import json

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()

def save_csv(filename):
    with open('kurs.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for i in range(13):
            spamwriter.writerow([(data[0]['rates'][i]["code"]), (data[0]['rates'][i]["bid"])])
    
#save_csv('kurs.csv')#JUŻ zapisałem
country = {}
def open_csv(filename):
    with open("kurs.csv", newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in csvreader:
            country[row[0]]=row[1]# Metodą prob wychaczyłe jak to robic! Doczytam lub zapytam.

open_csv("kurs.csv")

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("convert.html", country=country)
    elif request.method == 'POST':
        value = request.form['value']
        count = request.form['count']
#        value_ = 0
        for key,val in country.items():
            if key == value:
                value_ = val
        fincount = int(count)*float(value_)/4.12
        return render_template("result.html", fincount=fincount)
    

if __name__ == '__main__':
    app.run(debug=True)