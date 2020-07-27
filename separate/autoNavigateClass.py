import paho.mqtt.client as mqtt
import datetime
import toml
import time
from datetime import datetime,timezone, timedelta, date
import sys
import json
#import pika
import queue
import logging
from logging.handlers import QueueHandler, QueueListener
import sys
import threading
#from python_logging_rabbitmq import RabbitMQHandlerOneWay
from SDK import double


#testData = '{"host":"WFGATEWAY-3ABFF8D01EFF","message":"REPORT:42478B1A6B8CBA16,0.2.7,-19,207,3515,28,-30,10,4.10,-78.86,858027*6707","source":"03FF5C0A2BFA3A9B","time":"2020-07-22T13:29:05.838339518Z","type":"widefind_message"}'
class pars():
    def __init__(self):
        #d3 sdk
        self.d3 = double.DRDoubleSDK()

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

        self.y = None
        self.x = None
        self.z = 0
        self.state = ""
        self.timeout = time.time() + 5

    def parsCordinates(self, data):
        testParse = json.loads(data)
        cords = testParse['message']
        #print(cords)
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
        jsonMessage = json.dumps(mqttMsgJson)
        if "REPORT" in jsonMessage:
            cordinate = self.parsCordinates(jsonMessage)
            self.x = cordinate[0]
            self.y = cordinate[1]
            self.z = cordinate[2]

    def init_client(self):
        client = mqtt.Client()
        client.on_message = self.on_message
        client.connect(self.broker_url, self.broker_port)
        client.loop_start()
        client.subscribe("ltu-system/#")

    def navigateHitResult(self, xCamera= 0, yCamera = 0):
        try:
            self.d3.sendCommand('navigate.enable');
            self.d3.sendCommand('navigate.obstacleAvoidance.setLevel',{'level' : '2'});     
            while True:
                if self.x != None and self.y != None:
                    print('current state: ', self.state)
                    if self.state['state'] == 'Arrived': #or time.time() > self.timeout:
                        self.d3.sendCommand('navigate.cancelTarget')
                        self.d3.sendCommand('navigate.hitResult', {'hit': True,'xCamera': float(xCamera), 'yCamera': float(yCamera), 'type': 'drivable', 'x': float(self.x), 'y':float(self.y), 'z': float(self.z), 'angle': 0,'info1': '', 'info2': ''})
                        print('x: ', self.x, 'y: ', self.y)
                        #time.sleep(5)
        except KeyboardInterrupt:
            self.d3.close()
            print('cleaned up')
            sys.exit(0)

    def navigateTarget(self,stopAngle= 0):
        try:
            self.d3.sendCommand('navigate.enable');
            self.d3.sendCommand('navigate.obstacleAvoidance.setLevel',{'level' : '2'});     
            while True:
                if self.x != None and self.y != None:
                    if self.state['state'] == 'Arrived' or time.time() > self.timeout:
                        self.d3.sendCommand('navigate.target', {'x':float(self.x),'y':float(self.y),'angleRadians':float(stopAngle),'relative':False,'dock':False,'dockId':0})
                        print('x: ', self.x, 'y: ', self.y)
                        #time.sleep(5)
        except KeyboardInterrupt:
            self.d3.close()
            print('cleaned up')
            sys.exit(0)

    def subscribeEvents(self):
        try:
            self.d3.sendCommand('events.subscribe', { 'events': [
            'DRNavigateModule.targetState'
        ]})

            while True:
                packet = self.d3.recv()
                if packet != None:
                    event = packet['class'] + '.' + packet['key']
                    if event == 'DRNavigateModule.targetState':
                        self.state = packet['data']
                        print('navigate target state  = ---->', self.state, '<----')
        except KeyboardInterrupt:
            self.d3.close()
            print('cleaned up')
            sys.exit(0)

if __name__ == '__main__':
   test = pars()
   test.init_client()
   test.navigateHitResult()
   test.subscribeEvents()
   #test.navigateTarget()
   #send_data()
   #spawn thread mqtt
   #run send_data function
