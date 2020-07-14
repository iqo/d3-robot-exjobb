from SDK import double
import sys

def sendCommands():
    try:
        d3 = double.DRDoubleSDK()
        #d3.sendCommand('screensaver.nudge');
        #d3.sendCommand('camera.enable', { 'template': 'screen' });
        #d3.sendCommand('camera.enable', {'width':1152,'height':720,'template':'h264ForWebRTC','gstreamer':'appsrc name=d3src ! autovideosink'});
        d3.sendCommand('navigate.enable');
        d3.sendCommand('navigate.obstacleAvoidance.setLevel',{'level' : '2'});
        d3.sendCommand('navigate.target',{'x':2.901,'y':1.128,'angleRadians':0,'relative':'False','dock':'False','dockId':'0','highlight': 'True'});
        #d3.sendCommand('navigate.hitResult ',{'hit':'False','x':2.901,'y':1.128,'relative':'false'});
        #d3.sendCommand('camera.hitTest', {'x':2.901,'y':1.128,'highlight':'False', 'world': 'True'});
        # d3.sendCommand('base.requestStatus');
        while True:
            pass

    except KeyboardInterrupt:
        d3.sendCommand('camera.disable');
        d3.sendCommand('navigate.disable');
        d3.sendCommand('navigate.cancelTarget')
        d3.sendCommand('screensaver.nudge');
        d3.close()
        print('cleaned up')
        sys.exit(0)

sendCommands()
