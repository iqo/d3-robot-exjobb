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


class Navigate():
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
            self.d3.sendCommand('navigate.enable')
            self.d3.sendCommand('navigate.obstacleAvoidance.setLevel',{'level' : '2'})     
            if self.x != None and self.y != None:
                self.d3.sendCommand('navigate.cancelTarget')
                self.d3.sendCommand('navigate.hitResult', {'hit': True,'xCamera': float(xCamera), 'yCamera': float(yCamera), 'type': 'drivable', 'x': float(self.x), 'y':float(self.y), 'z': float(self.z), 'angle': 0,'info1': '', 'info2': ''})
                print('x: ', self.x, 'y: ', self.y)
                #time.sleep(10)
                #self.d3.sendCommand('navigate.cancelTarget')
        except KeyboardInterrupt:
            self.d3.close()
            print('cleaned up')
            sys.exit(0)

    def cancelNavigation(self):
        try:
            self.d3.sendCommand('navigate.cancelTarget')
        except KeyboardInterrupt:
            self.d3.close()
            print('cleaned up')
            sys.exit(0)

    def navigateTarget(self,stopAngle= 0):
        try:
            self.d3.sendCommand('navigate.enable')
            self.d3.sendCommand('navigate.obstacleAvoidance.setLevel',{'level' : '2'})     
            while True:
                if self.x != None and self.y != None:
                    self.d3.sendCommand('navigate.target', {'x':float(self.x),'y':float(self.y),'angleRadians':float(stopAngle),'relative':False,'dock':False,'dockId':0})
                    print('x: ', self.x, 'y: ', self.y)
                    time.sleep(5)
        except KeyboardInterrupt:
            self.d3.close()
            print('cleaned up')
            sys.exit(0)

#if __name__ == '__main__':
   #test = navigate()
   #test.init_client()
   #test.navigateHitResult()
   #test.navigateTarget()
   #send_data()
   #spawn thread mqtt
   #run send_data function