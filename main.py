from flask import Flask, render_template, request, url_for, redirect
from datetime import date
import schedule
import time
import threading
from emailtest import sendmail


EMPLOYEEDATA = {
    "3474" : "Muhammad"
}

def background_job():
    masterstring = ''
    simplifydata()
    for values in masterdata:
        masterstring += "<strong>"+values+"</strong>: "+masterdata[values]+"<br>"
    sendmail(masterstring)
    masterdata.clear()

def threadtwo():
    schedule.every().thursday.at("00:45").do(background_job)
    while True:
        schedule.run_pending()
        time.sleep(30)
        print("alooo")



app = Flask(__name__)
masterdata = {}


def simplifydata():
    months=[
        "January",
        "February"
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ]
    for key in masterdata:
        conststring = ''
        dates = masterdata[key]
        x = dates.split(", ")
        for values in x:
            singledate = values.split("-")
            conststring += singledate[2] +" of "+months[int(singledate[1])-1]+", "
        masterdata[key] = conststring

    

@app.before_first_request
def runthread():
    thd = threading.Thread(target=threadtwo)
    thd.start()

@app.route("/", methods=['GET', 'POST'])
def mainSys():
    if request.method == "POST":
        EmpId = request.form.get('EmpID')
        dates = request.form.get('date')
        print(EmpId)
        print(dates)
        if EmpId in EMPLOYEEDATA:
            name = EMPLOYEEDATA[EmpId]
            if name in masterdata:
                return redirect(url_for('dupe',names2 = name,oldates=masterdata[name],newdates = dates))
            else:
                masterdata[name] = dates
                return redirect("/done")
        else:
            return redirect("/logInFail")
    else:
        return render_template('main.html')


@app.route("/logInFail", methods=['GET', 'POST'])
def logInFailed():
    if request.method == "POST":
        return redirect("/", code=302)
    else:
        return render_template('invalidLogin.html')


@app.route("/duplicate", methods=['GET', 'POST'])
def dupe():
    name = request.args.get('names2')
    replaceddates = request.args.get('newdates')
    old = request.args.get('oldates')
    if request.method == "POST":
        if request.form.get("sub"):
            masterdata[name] = replaceddates
            return redirect("/done", code=302)
        else:
            return redirect("/", code=302)
    else:
        return render_template('dupe.html', olddates = old, newdates = replaceddates)


@app.route("/done", methods=['GET', 'POST'])
def end():
    if request.method == "POST":
        if request.form.get("finish"):
            print(masterdata)
            simplifydata()
            print(masterdata)
            masterdata.clear()
            return redirect("/", code=302)
        else:
            print(masterdata)
            return redirect("/", code=302)
    else:
        return render_template('sub.html')


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_flex_quickstart]
