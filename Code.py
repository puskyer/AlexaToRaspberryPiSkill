import logging
import os

from pymochad import controller
from pymochad import device
from flask import Flask
from flask_ask import Ask, request, session, question, statement
import RPi.GPIO as GPIO

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

STATUSON = ['on','high']
STATUSOFF = ['off','low']

@ask.launch
def launch():
    speech_text = 'Welcome to Raspberry Pi Automation.'
    return question(speech_text).reprompt(speech_text).simple_card(speech_text)

@ask.intent('MochadIntent', mapping = {'status':'status'})
def mochad_Intenet(status,room):
    mochad = controller.PyMochad(server='127.0.0.1',port=1099)
    print("Status is")
    print(mochad.status())
    if status in STATUSON:
	light_switch = device.Device(mochad, 'a15')
        light_switch.send_cmd('on')
        print("Light on")
	return statement('turning {} lights'.format(status))
    elif status in STATUSOFF:
        light_switch = device.Device(mochad, 'a15')
        light_switch.send_cmd('off')
        print("Light off")
        return statement('turning {} lights'.format(status))
    else:
        return statement('Sorry not possible.')

def Gpio_Intent(status,room):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)    
    GPIO.setup(17,GPIO.OUT)



 
@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = 'You can say hello to me!'
    return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)


@ask.session_ended
def session_ended():
    return "{}", 200


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True)
