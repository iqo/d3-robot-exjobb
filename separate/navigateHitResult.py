from SDK import double
import sys

def navigateHitResult(xCordinate, yCordinate, xCamera= 0, yCamera = 0, zCordinate=0):
    d3 = double.DRDoubleSDK()
    try:
        d3.sendCommand('events.subscribe', { 'events': [
        'DRCamera.hitResult',
        'DRNavigateModule.newTarget'
        ]})
        d3.sendCommand('navigate.enable');
        d3.sendCommand('navigate.obstacleAvoidance.setLevel',{'level' : '2'});
        d3.sendCommand('camera.hitTest', {'hit': 'true', 'x': 0.5,'y': 0.5,'z': 0, 'highlight': 'true'});
        d3.sendCommand('navigate.hitResult', {'hit': True,'xCamera': float(xCamera), 'yCamera': float(yCamera), 'type': 'drivable', 'x': float(xCordinate), 'y':float(yCordinate), 'z': float(zCordinate), 'angle': 0,'info1': '', 'info2': ''});
        while True:
            packet = d3.recv()
            if packet != None:
                event = packet['class'] + '.' + packet['key']
                if event == 'DRCamera.hitResult':
                    print('camerahitResult = ---->', packet['data'], '<----')
                elif event == 'DRNavigateModule.newTarget':
                    print('new target = ---->', packet['data'], '<----')
    except KeyboardInterrupt:
        d3.close()
        d3.sendCommand('navigate.cancelTarget')
        d3.sendCommand('navigate.disable');
        print('cleaned up')
        sys.exit(0)

if __name__ == '__main__':
    # Map command line arguments to function arguments.
    navigateHitResult(*sys.argv[1:])