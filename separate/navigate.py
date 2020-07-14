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
        d3.sendCommand('camera.hitTest', {'hit': 'true', 'x': 0.5,'y': 0.5,'z': 0, 'highlight': 'true'})
        while True:
            packet = d3.recv()
            if packet != None:
                event = packet['class'] + '.' + packet['key']
                if event == 'DRCamera.hitResult':
                    d3.sendCommand('navigate.target', {'hit': True, 'xCamera': -0.2511, 'yCamera': -0.443, 'type': 'drivable', 'x': 2.454, 'y': 1.037, 'z': 0, 'angle': 0, 'info1': '', 'info2': ''})
                    # d3.sendCommand('navigate.target',packet['data'])
                    print('camerahitResult = ---->', packet['data'], '<----')
    except KeyboardInterrupt:
        d3.close()
        print('cleaned up')
        sys.exit(0)

navigate()
