from SDK import double
import sys

def navigate():
    d3 = double.DRDoubleSDK()
    try:
        d3.sendCommand('events.subscribe', { 'events': [
        'DRCamera.hitResult',
        'DRNavigateModule.newTarget'
        ]})
        d3.sendCommand('screensaver.nudge');
        d3.sendCommand('camera.enable', { 'template': 'screen' });
        d3.sendCommand('navigate.enable');
        d3.sendCommand('navigate.obstacleAvoidance.setLevel',{'level' : '2'});
        #d3.sendCommand('navigate.target ', {'x':0,'y':0,'angleRadians':0,'relative':False,'dock':False,'dockId':0});
        d3.sendCommand('camera.hitTest', {'hit': 'true', 'x': 0.5,'y': 0.5,'z': 0, 'highlight': 'true'});
        while True:
            packet = d3.recv()
            if packet != None:
                event = packet['class'] + '.' + packet['key']
                if event == 'DRCamera.hitResult':
                    d3.sendCommand('navigate.hitResult', {'hit': True,'xCamera': -0.2511, 'yCamera': -0.443, 'type': 'drivable', 'x': 4.186, 'y': 0.212, 'z': 0, 'angle': 0,'info1': '', 'info2': ''});
                    # d3.sendCommand('navigate.target',packet['data'])
                    print('camerahitResult = ---->', packet['data'], '<----')
                elif event == 'DRNavigateModule.newTarget':
                    print('new target = ---->', packet['data'], '<----')
    except KeyboardInterrupt:
        d3.close()
        d3.sendCommand('navigate.cancelTarget')
        d3.sendCommand('camera.disable');
        print('cleaned up')
        sys.exit(0)

navigate()
