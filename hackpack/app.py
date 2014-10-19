import re
import time, threading
import os, subprocess

from flask import Flask
from flask import render_template
from flask import url_for
from flask import request

from twilio import twiml
from twilio.util import TwilioCapability
from twilio.rest import TwilioRestClient
import datetime
import helper

# Declare and configure application
app = Flask(__name__, static_url_path='/static')
app.config.from_pyfile('local_settings.py')

db = {}

    
db["+16172099765"] = {
    "name":"Santa Claus",
    "dob":datetime.datetime(2014, 7, 05),
    "zipcode":"02139",
    "bcg":datetime.datetime(2014, 7, 06),
    "hepb1":datetime.datetime(2014, 7, 06),
    "hepb2":datetime.datetime(2014, 8, 20),
    "hepb3":0,
    "polio1":datetime.datetime(2014, 7, 06),
    "polio2":datetime.datetime(2014, 8, 20),
    "polio3":datetime.datetime(2014, 9, 20),
    "polio4":0,
    "polio5":0,
    "polio6":0,
    "polio7":0,
    "polio8":0,
    "dtp1":0,
    "dtp2":0,
    "dtp3":0,
    "dtp4":0,
    "dtp5":0,
    "tdap":0,
    "hib1":0,
    "hib2":0,
    "hib3":0,
    "hib4":0,
    "pcv1":datetime.datetime(2014, 8, 20),
    "pcv2":datetime.datetime(2014, 9, 20),
    "pcv3":0,
    "pcv4":0,
    "rv1":datetime.datetime(2014, 8, 20),
    "rv2":datetime.datetime(2014, 9, 20),
    "rv3":0,
    "measles":0,
    "mmr1":0,
    "mmr2":0,
    "var1":0,
    "var2":0,
    "hepa1":0,
    "hepa2":0,
    "typhoid":0,
    "hpv1":0,
    "hpv2":0,
    "hpv3":0,
}

vaccineCode = {
    "9e4f":"bcg",
    "3ifk":"hepb1",
    "36dg":"hepb2",
    "eijl":"hepb3",
    "q52y":"polio1",
    "u0sv":"polio2",
    "26s2":"dtp1",
    "qe10":"dtp2",
}

vaccineTimes = {
    "bcg":datetime.timedelta(days = 0),
    "hepb1":datetime.timedelta(days = 0),
    "hepb2":datetime.timedelta(days = 45),
    "hepb3":datetime.timedelta(days = 185),
    "polio1":datetime.timedelta(days = 0),
    "polio2":datetime.timedelta(days = 45),
    "polio3":datetime.timedelta(days = 70),
    "polio4":datetime.timedelta(days = 100),
    "polio5":datetime.timedelta(days = 185),
    "polio6":datetime.timedelta(days = 275),
    "polio7":datetime.timedelta(days = 365),
    "polio8":datetime.timedelta(days = 1460),
    "dtp1":datetime.timedelta(days = 45),
    "dtp2":datetime.timedelta(days = 70),
    "dtp3":datetime.timedelta(days = 100),
    "dtp4":datetime.timedelta(days = 455),
    "dtp5":datetime.timedelta(days = 1460),
    "tdap":datetime.timedelta(days = 4015),
    "hib1":datetime.timedelta(days = 45),
    "hib2":datetime.timedelta(days = 70),
    "hib3":datetime.timedelta(days = 100),
    "hib4":datetime.timedelta(days = 365),
    "pcv1":datetime.timedelta(days = 45),
    "pcv2":datetime.timedelta(days = 70),
    "pcv3":datetime.timedelta(days = 100),
    "pcv4":datetime.timedelta(days = 365),
    "rv1":datetime.timedelta(days = 45),
    "rv2":datetime.timedelta(days = 70),
    "rv3":datetime.timedelta(days = 100),
    "measles":datetime.timedelta(days = 270),
    "mmr1":datetime.timedelta(days = 365),
    "mmr2":datetime.timedelta(days = 1460),
    "var1":datetime.timedelta(days = 455),
    "var2":datetime.timedelta(days = 1460),
    "hepa1":datetime.timedelta(days = 365),
    "hepa2":datetime.timedelta(days = 365),
    "typhoid":datetime.timedelta(days = 730),
    "hpv1":datetime.timedelta(days = 4015),
    "hpv2":datetime.timedelta(days = 4015),
    "hpv3":datetime.timedelta(days = 4015),
}

def foo():
    client = TwilioRestClient(os.environ.get('TWILIO_ACCOUNT_SID', None), os.environ.get('TWILIO_AUTH_TOKEN', None))
    for number in db:
        needed = []
        for vaccine in vaccineTimes: 
            if (datetime.datetime.now() - db[number]["dob"]) >= vaccineTimes[vaccine] and db[number][vaccine] == 0:
                needed.append(vaccine.upper())
        if len(needed) > 0:
            body = "Your child is due for the following vaccines: "
            for need in needed:
                body += need.upper() + ", "
            body = body[:-2]
            message = client.messages.create(to=number, from_="+14088053907", body=body)
    threading.Timer(7*86400, foo).start()

foo()

# Voice Request URL
@app.route('/voice', methods=['GET', 'POST'])
def voice():
    response = twiml.Response()
    response.say("Congratulations! You deployed the Twilio Hackpack "
                 "for Heroku and Flask.")
    return str(response)


# SMS Request URL
@app.route('/sms', methods=['GET', 'POST'])
def sms():
    response = twiml.Response()
    from_number = request.values.get('From', None)
    body = request.form['Body']
    reg = re.compile('[r|R]eg name:[\s|\S]+ dob:[\s|\S]+ zipcode:[\s|\S]+')
    send = re.compile('[s|S]end \+\d\d\d\d\d\d\d\d\d\d\d')
    if reg.match(body) is not None:
        if from_number in db:
            response.sms("User already exists!")
        else:
            input = re.split(' name:| dob:| zipcode:', body)
            name = input[1]
            dobarray = input[2].split('/')
            month = dobarray[0]
            day = dobarray[1]
            year = dobarray[2]
            dob = datetime.datetime(int(year), int(month), int(day))
            zipcode = input[3]
            db[from_number] = {
                "name":name,
                "dob":dob,
                "zipcode":zipcode,
                "bcg":0,
                "hepb1":0,
                "hepb2":0,
                "hepb3":0,
                "polio1":0,
                "polio2":0,
                "polio3":0,
                "polio4":0,
                "polio5":0,
                "polio6":0,
                "polio7":0,
                "polio8":0,
                "dtp1":0,
                "dtp2":0,
                "dtp3":0,
                "dtp4":0,
                "dtp5":0,
                "tdap":0,
                "hib1":0,
                "hib2":0,
                "hib3":0,
                "hib4":0,
                "pcv1":0,
                "pcv2":0,
                "pcv3":0,
                "pcv4":0,
                "rv1":0,
                "rv2":0,
                "rv3":0,
                "measles":0,
                "mmr1":0,
                "mmr2":0,
                "var1":0,
                "var2":0,
                "hepa1":0,
                "hepa2":0,
                "typhoid":0,
                "hpv1":0,
                "hpv2":0,
                "hpv3":0,
            }
            response.sms(helper.confirmationMsg(name, dob, zipcode))
    elif from_number not in db:
        response.sms("Please register first!")
    elif body in vaccineCode:
        if db[from_number][vaccineCode[body]] != 0:
            response.sms("Already received vaccine!")
        else:
            db[from_number][vaccineCode[body]] = datetime.datetime.now()
            response.sms(helper.responseFromVaccine(vaccineCode[body])) 
    
    elif body == "record":
        response.sms(helper.info(db[from_number], vaccineTimes))
    elif send.match(body) is not None:
        inputs = body.split('+')
        args = ['curl', '-u', 'zD93Tl5vChhg63gpeRLF8JiSvVBCaKEk:AZmEit4I6WQQ19y5QCHWyOVjU5VV2JrpdPtqaIXc4R8In0xQ', '-vX', 'POST', 'https://api.tigertext.me/v1/message', '--data-urlencode', 'recipient=+' + str(inputs[1]), '--data', 'body=' + helper.info(db[from_number], vaccineTimes), '--data', 'ttl=7200']
        subprocess.call(args)

    else:
        response.sms("Error: Ill-formed Submission")
     
    return str(response)


# Twilio Client demo template
@app.route('/client')
def client():
    configuration_error = None
    for key in ('TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN', 'TWILIO_APP_SID',
                'TWILIO_CALLER_ID'):
        if not app.config.get(key, None):
            configuration_error = "Missing from local_settings.py: " \
                                  "{0}".format(key)
            token = None

    if not configuration_error:
        capability = TwilioCapability(app.config['TWILIO_ACCOUNT_SID'],
                                      app.config['TWILIO_AUTH_TOKEN'])
        capability.allow_client_incoming("joey_ramone")
        capability.allow_client_outgoing(app.config['TWILIO_APP_SID'])
        token = capability.generate()
    params = {'token': token}
    return render_template('client.html', params=params,
                           configuration_error=configuration_error)


@app.route('/client/incoming', methods=['POST'])
def client_incoming():
    try:
        from_number = request.values.get('PhoneNumber', None)

        resp = twiml.Response()

        if not from_number:
            resp.say("Your app is missing a Phone Number. "
                     "Make a request with a Phone Number to make outgoing "
                     "calls with the Twilio hack pack.")
            return str(resp)

        if 'TWILIO_CALLER_ID' not in app.config:
            resp.say(
                "Your app is missing a Caller ID parameter. "
                "Please add a Caller ID to make outgoing calls with Twilio "
                "Client")
            return str(resp)

        with resp.dial(callerId=app.config['TWILIO_CALLER_ID']) as r:
            # If we have a number, and it looks like a phone number:
            if from_number and re.search('^[\d\(\)\- \+]+$', from_number):
                r.number(from_number)
            else:
                r.say("We couldn't find a phone number to dial. Make sure "
                      "you are sending a Phone Number when you make a "
                      "request with Twilio Client")

        return str(resp)

    except:
        resp = twiml.Response()
        resp.say("An error occurred. Check your debugger at twilio dot com "
                 "for more information.")
        return str(resp)


# Installation success page
@app.route('/')
def index():
    params = {
        'Voice Request URL': url_for('.voice', _external=True),
        'SMS Request URL': url_for('.sms', _external=True),
        'Client URL': url_for('.client', _external=True)}
    return render_template('index.html', params=params,
                           configuration_error=None)
