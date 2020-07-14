from SDK import double
import sys

def navigate():
    d3 = double.DRDoubleSDK()
    try:
        d3.sendCommand('events.subscribe', { 'events': [
        'DRCamera.hitResult',
        ]})
        d3.sendCommand('navigate.enable');
        d3.sendCommand('navigate.obstacleAvoidance.setLevel',{'level' : '2'});
        d3.sendCommand('camera.hitTest', {	'hit': true, 'x': 3,'y': 1,'z': 0})
        while True:
            packet = d3.recv()
            if packet != None:
                event = packet['class'] + '.' + packet['key']
                if event == 'DRCamera.hitResult':
                    print('camerahitResult = ---->', packet['data'], '<----')
    except KeyboardInterrupt:
        d3.close()
        print('cleaned up')
        sys.exit(0)

navigate()