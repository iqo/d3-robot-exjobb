import double
import sys

d3 = double.DRDoubleSDK()

try:
    d3.sendCommand('events.subscribe', { 'events': [
        'DRBase.status',
        'DRCamera.enable',
        'DRGridManager.robotGrid'

    ]})
    d3.sendCommand('screensaver.nudge');
    d3.sendCommand('camera.enable', { 'template': 'screen' });
    d3.sendCommand('gridManager.enable');
    d3.sendCommand('base.requestStatus');
    while True:
        packet = d3.recv()
        if packet != None:
            event = packet['class'] + '.' + packet['key']
            if event == 'DRBase.status':
                print(packet['data'])
            if event == 'DRGridManager.robotGrid':
                print('grid enabled')
            elif event == 'DRCamera.enable':
                print('camera enabled')

except KeyboardInterrupt:
    d3.sendCommand('camera.disable');
    d3.sendCommand('gridManager.disable')
    d3.sendCommand('screensaver.nudge');
    d3.close()
    print('cleaned up')
    sys.exit(0)
