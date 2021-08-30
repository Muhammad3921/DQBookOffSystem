from flask import Flask, render_template, request, url_for, redirect
from datetime import date
from emailtest import generateString, sendmail
import schedule
import time
import threading




app = Flask(__name__)
masterdata = {}
name1 = []
dates1 = []

def background_job():
    finalmsg = generateString(masterdata)
    masterdata.clear()
    sendmail(finalmsg)

def threadtwo():
    schedule.every().thursday.at("23:59").do(background_job)
    while True:
     schedule.run_pending()
     time.sleep(60)

@app.route("/", methods=['GET', 'POST'])
def mainSys():
    if request.method == "POST":
        name = request.form["namess"]
        dates = request.form["date"]
        if(name in masterdata.keys()):
            name1.clear()
            dates1.clear()
            name1.append(name)
            dates1.append(dates)
            return redirect("/duplicate", code=302)

        masterdata[name] = dates
        name = ""
        dates = ""
        return redirect("/done", code=302)
    else:
        return render_template('main.html')


@app.route("/duplicate", methods=['GET', 'POST'])
def dupe():
    if request.method == "POST":
        if request.form.get("sub"):
            dates = dates1[-1]
            name = name1[-1]
            dates1.clear()
            name1.clear()
            masterdata[name] = dates
            name = ""
            dates = ""
            dates1.clear()
            name1.clear()
            return redirect("/done", code=302)
        else:
            return redirect("/", code=302)
    else:
        return render_template('dupe.html')


@app.route("/done", methods=['GET', 'POST'])
def end():
    if request.method == "POST":
        if request.form.get("finish"):
            masterdata.clear()
            return redirect("/", code=302)
        else:
            return redirect("/", code=302)
    else:
        return render_template('sub.html')


def prettify(a_dict, key):

    todays_date = date.today()
    x = []
    z = []
    temp = a_dict[key]
    x = temp.split(", ")
    for value in x:
        y = value.split("-")
        if (int(y[0]) == todays_date.year):
            z.append(y[1]+"-"+y[2])
            y.clear
    a_dict[key] = z
    z.clear
    x.clear
    temp = ""
    return a_dict

thd = threading.Thread(target=threadtwo)
thd.start()


