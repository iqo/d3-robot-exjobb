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
from SDK import double
#import parsingTest


#testData = '{"host":"WFGATEWAY-3ABFF8D01EFF","message":"REPORT:42478B1A6B8CBA16,0.2.7,-19,207,3515,28,-30,10,4.10,-78.86,858027*6707","source":"03FF5C0A2BFA3A9B","time":"2020-07-22T13:29:05.838339518Z","type":"widefind_message"}'
class pars():
    def __init__(self):
        #test = parsingTest.pars()
        #Loading config
        self.config = toml.load("config_widefind.toml")

        #MQTT IP for widefind
        self.broker_url = self.config["connection"]["broker_ip"]
        self.broker_port = self.config["connection"]["broker_port"]

        self.blacklist = self.config["connection"]["blacklist"]#NO DATA EXPECTED FOR ADMIN THEREFORE IS IN BLACKLIST (no data downloaded for users in blacklist)
        self.entrypoint = self.config["connection"]["entrypoint"]
        self.port = self.config["connection"]["entrypoint_port"]

        #Creating Queue
        self.data_queue = queue.Queue()

    def parsCordinates(self, data):
        testParse = json.loads(data)
        cords = testParse['message']
        print(cords)
        count = 0
        for n in cords:
            if n == ',':
                count = 1 + count
        split_string = cords.split(",", count)
        xInMeter = (float(split_string[2])/1000)
        yInMeter = (float(split_string[3])/1000)
        zInMeter = (float(split_string[4])/1000)
        return xInMeter, yInMeter, zInMeter



    def on_message(self, client, userdata, message):
        mqttMsgString = message.payload.decode()
        mqttMsgJson = json.loads(mqttMsgString)
        #print(mqttMsgJson)
        self.data_queue.put(mqttMsgJson)

    def init_client(self):
        client = mqtt.Client()
        client.on_message = self.on_message
        client.connect(self.broker_url, self.broker_port)
        client.loop_start()
        client.subscribe("ltu-system/#")

    def testtest(self):
        while True:
            message = self.data_queue.get(block=True)
            jsonMessage = json.dumps(message)
            if "BEACON" in jsonMessage:
            #if "REPORT" in jsonMessage:
                self.parsCordinates(jsonMessage)
                #print(cord[0])

if __name__ == '__main__':
   test = pars()
   test.init_client()
   test.testtest()
   #send_data()
   #spawn thread mqtt
   #run send_data function
