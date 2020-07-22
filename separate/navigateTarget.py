from SDK import double
import sys

def navigateTarget(xCordinate, yCordinate, stopAngle= 0):
    d3 = double.DRDoubleSDK()
    try:
        d3.sendCommand('events.subscribe', { 'events': [
        'DRCamera.hitResult',
        'DRNavigateModule.newTarget'
        ]})
        d3.sendCommand('navigate.enable');
        d3.sendCommand('navigate.obstacleAvoidance.setLevel',{'level' : '2'});
        d3.sendCommand('camera.hitTest', {'hit': 'true', 'x': 0.5,'y': 0.5,'z': 0, 'highlight': 'true'});
        d3.sendCommand('navigate.target', {'x':float(xCordinate),'y':float(yCordinate),'angleRadians':float(stopAngle),'relative':False,'dock':False,'dockId':0});

        while True:
            packet = d3.recv()
            if packet != None:
                event = packet['class'] + '.' + packet['key']
                if event == 'DRNavigateModule.newTarget':
                    print('new target = ---->', packet['data'], '<----')
    except KeyboardInterrupt:
        d3.close()
        d3.sendCommand('navigate.cancelTarget')
        d3.sendCommand('navigate.disable');
        print('cleaned up')
        sys.exit(0)

if __name__ == '__main__':
    # Map command line arguments to function arguments.
    navigateTarget(*sys.argv[1:])