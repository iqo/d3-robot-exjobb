from SDK import double
import sys

def navigate():
    d3 = double.DRDoubleSDK()
    try:
        d3.sendCommand('events.subscribe', { 'events': [
        'DRCamera.pose.setRequired',
        'DRPose.model',
        'DRPose.pose'
        'DRPose.resetOrigin'
        ]})
        d3.sendCommand('navigate.enable');
        d3.sendCommand('navigate.obstacleAvoidance.setLevel',{'level' : '2'});
        d3.sendCommand('pose.requestModel')
        d3.sendCommand('camera.pose.setRequired');

        while True:
            packet = d3.recv()
            if packet != None:
                event = packet['class'] + '.' + packet['key']
                if event == 'DRCamera.pose.setRequired':
                    print('DRCamera pose setReq',packet['data'])
                elif event == 'DRPose.model':
                    print('pose model',packet['data'])
                elif event == 'DRPose.pose':
                    print('pose',packet['data'])
                elif event == 'DRPose.resetOrigin':
                    print('pose reset origin',packet['data'])
    except KeyboardInterrupt:
        d3.close()
        print('cleaned up')
        sys.exit(0)

navigate()