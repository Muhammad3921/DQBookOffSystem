from flask import Flask, render_template, request, url_for, redirect
from datetime import date
from emailtest import generateString, sendmail
import schedule
import time
import threading
import os
from dotenv import load_dotenv

load_dotenv()

EMPLOYEEDATA = os.getenv("EMPDATA")


def threadtwo():
    schedule.every().saturday.at("15:23").do(background_job)
    while True:
        schedule.run_pending()
        time.sleep(30)


thd = threading.Thread(target=threadtwo)
thd.start()

app = Flask(__name__)
masterdata = {}


def background_job():
    finalmsg = generateString(masterdata)
    masterdata.clear()
    sendmail(finalmsg)


@app.route("/", methods=['GET', 'POST'])
def mainSys():
    if request.method == "POST":
        EmpId = request.form.get('EmpId')
        if EmpId in EMPLOYEEDATA:
            name = EMPLOYEEDATA[EmpId]
            if name in masterdata:
                return redirect("/loggedin", Name=name, datess=masterdata[name], code=302)
            else:
                return redirect("/loggedin", Name=name, datess="", code=302)
    else:
        return render_template('main.html')


@app.route("/loggedin", methods=['GET', 'POST'])
def loggedin():
    if request.method == "POST":
        dates = request.form["date"]
        name = request.form["name"]
        if name in masterdata:
            return redirect("/duplicate", Name=name, newdates=dates, code=302)
        else:
            masterdata[name] = dates
            return redirect("/done")

    else:
        return render_template('login.html')


@app.route("/logInFail", methods=['GET', 'POST'])
def logInFailed():
    if request.method == "POST":
        return redirect("/", code=302)
    else:
        return render_template('invalidLogin.html')


@app.route("/duplicate", methods=['GET', 'POST'])
def dupe():
    if request.method == "POST":
        if request.form.get("sub"):
            

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


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_flex_quickstart]
