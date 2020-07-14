from SDK import double
import sys

def sendCommands():
    try:
        d3 = double.DRDoubleSDK()
        d3.sendCommand('screensaver.nudge');
        d3.sendCommand('camera.enable', { 'template': 'screen' });
        # d3.sendCommand('camera.enable', {'width':1152,'height':720,'template':'h264ForWebRTC','gstreamer':'appsrc name=d3src ! autovideosink'});
        d3.sendCommand('navigate.enable');
        d3.sendCommand('navigate.obstacleAvoidance.setLevel',{'level' : '2'});
        # d3.sendCommand('navigate.target',{'x':'0','y':'0','angleRadians':'0','relative':'true','dock':'false','dockId':'0'});
        # d3.sendCommand('navigate.hitResult ',{'hit':'true','x':'0.0','y':'0.0','z':'0.0','...'});
        d3.sendCommand('camera.hitTest', {'x':'0.5','y':'0.5','highlight':'true', 'world': 'True'});
        # d3.sendCommand('base.requestStatus');

    except KeyboardInterrupt:
        d3.sendCommand('camera.disable');
        d3.sendCommand('navigate.disable');
        d3.sendCommand('screensaver.nudge');
        d3.close()
        print('cleaned up')
        sys.exit(0)

