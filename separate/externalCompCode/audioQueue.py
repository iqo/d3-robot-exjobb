import time
import speech_recognition as sr
import autoParseClass
import paho.mqtt.client as mqtt
import datetime
import toml
import time
from datetime import datetime,timezone, timedelta, date
import sys
import json
import pika
import queue
import logging
from logging.handlers import QueueHandler, QueueListener
import sys
import threading
from python_logging_rabbitmq import RabbitMQHandlerOneWay
from io import StringIO
#import parsingTest


#test = parsingTest.pars()
#Loading config
config = toml.load("config_widefind.toml")

# Initialize logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# out_handler = logging.StreamHandler(sys.stdout)
# out_handler.setLevel(logging.DEBUG)
# logger.addHandler(out_handler)

rabbit_handler = RabbitMQHandlerOneWay(
    host=config['rabbitmq']['host'],
    username=config['rabbitmq']['username'],
    password=config['rabbitmq']['password'],
    connection_params={
       'virtual_host':'/',
       'connection_attempts': 3,
       'socket_timeout': 5000
    })
#logger.addHandler(rabbit_handler)

#Creating Queue
data_queue = queue.Queue()

def send_data():
    parameters = pika.URLParameters(
       "amqp://"+config['rabbitmq']['username']+":"+config['rabbitmq']['password']+"@"+config['rabbitmq']['host']+"/"+config['rabbitmq']['username']
    )
    try:
       connection = pika.BlockingConnection(parameters)
       logger.info("Initialized RabbitMQ connection")
    except:
       logger.info("Failed to connect to RabbitMQ")
       raise
    channel = connection.channel()
    message = data_queue.get(block=True)
    formated_message = message 
    #{
        #"time": datetime.now().isoformat(),
        #"event_type": "audioTrascribe",
        #"sensor_type": "computerMic",
        #"payload": message
    #} 
#       #logger.debug("Sending message: {}".format(formated_message))
    message = json.dumps(formated_message)
    print(message)
    channel.basic_publish(exchange=config['rabbitmq']['sensor_exchange'],
                        routing_key = config['rabbitmq']['routing_key'],
                        body = message
    )
    connection.close()


# this is called from the background thread
def callback(recognizer, audio):
    #auto = autoParseClass.pars()
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        test = recognizer.recognize_google(audio)
        print("Google Speech Recognition thinks you said " + recognizer.recognize_google(audio))
        data_queue.put(test)
        send_data()
        print("start")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

r = sr.Recognizer()
m = sr.Microphone(device_index=13)
with m as source:
    r.adjust_for_ambient_noise(source,duration=3)  # we only need to calibrate once, before we start listening

# start listening in the background (note that we don't have to do this inside a `with` statement)
stop_listening = r.listen_in_background(m, callback)
# `stop_listening` is now a function that, when called, stops background listening

# do some unrelated computations for 5 seconds
for _ in range(50): time.sleep(0.1)  # we're still listening even though the main thread is doing other things

# calling this function requests that the background listener stop listening
#stop_listening(wait_for_stop=False)

# do some more unrelated things
while True: time.sleep(0.1)  # we're not listening anymore, even though the background thread might still be running for a second or two while cleaning up and stopping

#if __name__ == '__main__':
   #init_client()
   #testtest()
   #send_data()
   #spawn thread mqtt
   #run send_data function
