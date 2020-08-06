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
import math
import numpy as np

class AbsoluteNavigation():
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

        self.originXCordinate = None
        self.originYCordinate = None
        self.originZCordinate = None

        self.transmiterXCordinate = None
        self.transmiterYCordinate = None
        self.transmiterZCordinate = None

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
        #self.data_queue.put(mqttMsgJson)
        jsonMessage = json.dumps(mqttMsgJson)
        if "REPORT:42478B1A6B8CBA16" in jsonMessage:
            cordinate = self.parsCordinates(jsonMessage)
            self.transmiterXCordinate = cordinate[0]
            self.transmiterYCordinate = cordinate[1]
            self.transmiterZCordinate = cordinate[2]

    def unitVector(self,vector):
        """ Returns the unit vector of the vector.  """
        return vector / np.linalg.norm(vector)

    def angleBetween(self,vector1, vector2):
        """ Returns the angle in radians between vectors 'v1' and 'v2'::

                 angle_between((1, 0, 0), (0, 1, 0))
                1.5707963267948966
                 angle_between((1, 0, 0), (1, 0, 0))
                0.0
                angle_between((1, 0, 0), (-1, 0, 0))
                3.141592653589793
        """
        vector1U = self.unitVector(vector1)
        vector2U = self.unitVector(vector2)
        return np.arccos(np.clip(np.dot(vector1U, vector2U), -1.0, 1.0))

    def degree(self, radian):
        degree = math.degrees(radian)
        return degree

    def init_client(self):
        client = mqtt.Client()
        client.on_message = self.on_message
        client.connect(self.broker_url, self.broker_port)
        client.loop_start()
        client.subscribe("ltu-system/#")
        time.sleep(10)
        client.loop_stop()

    def navigateTarget(self):
        try:
            if self.originXCordinate != None and self.originYCordinate != None and self.originZCordinate != None and self.transmiterXCordinate != None and self.transmiterYCordinate != None and self.transmiterZCordinate != None:
                self.d3.sendCommand('navigate.enable')
                self.d3.sendCommand('navigate.obstacleAvoidance.setLevel',{'level' : '2'})
                self.d3.sendCommand('depth.floor.enable')
                self.d3.sendCommand('depth.front.enable')
                vector1 = [self.originXCordinate, self.originYCordinate]
                vector2 = [self.transmiterXCordinate, self.transmiterYCordinate]
                radianAngle = self.angleBetween(vector1, vector2)
                #degreeAngle = self.degree(radianAngle)
                targetX = float(self.transmiterXCordinate) - float(self.originXCordinate)
                targetY = float(self.transmiterYCordinate) - float(self.originYCordinate)
                self.d3.sendCommand('navigate.target', {'x':float(targetX),'y':float(targetY),'angleRadians':float(-radianAngle),'relative':False,'dock':False,'dockId':0})
                print('x:', targetX, ' y:', targetY, ' angle radians:',-radianAngle)
        except KeyboardInterrupt:
            #self.d3.close()
            print('cleaned up')
            #sys.exit(0)
