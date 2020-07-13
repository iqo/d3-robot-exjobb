import double
import sys

d3 = double.DRDoubleSDK()

try:
    d3.sendCommand('events.subscribe', { 'events': [
        'DRBase.status',
        'DRCamera.enable',
        'DRCamera.hitResult'

    ]})
    d3.sendCommand('screensaver.nudge');
    # d3.sendCommand('camera.enable', { 'template': 'screen' });
    d3.sendCommand('camera.enable', {'width':1152,'height':720,'template':'h264ForWebRTC','gstreamer':'appsrc name=d3src ! autovideosink'});
    #d3.sendCommand('navigate.enable');
    #d3.sendCommand('navigate.obstacleAvoidance.setLevel',{'level' : '2'});
    #d3.sendCommand('navigate.target',{'x':'0','y':'0','angleRadians':'0','relative':'true','dock':'false','dockId':'0'});
    # d3.sendCommand('navigate.hitResult ',{'hit':'true','x':'0.0','y':'0.0','z':'0.0','...'});
    #d3.sendCommand('camera.hitTest', {'x':'0.5','y':'0.5','highlight':'true'});
    d3.sendCommand('base.requestStatus');
    while True:
        packet = d3.recv()
        if packet != None:
            event = packet['class'] + '.' + packet['key']
            if event == 'DRBase.status':
                print(packet['data'])
            elif event == 'DRCamera.enable':
                print('camera enabled')
            elif event == 'DRCamera.hitResult':
                print('hitResult =', packet['data'])
                

except KeyboardInterrupt:
    d3.sendCommand('camera.disable');
    d3.sendCommand('navigate.disable');
    d3.sendCommand('screensaver.nudge');
    d3.close()
    print('cleaned up')
    sys.exit(0)

