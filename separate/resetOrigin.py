from SDK import double
import sys

def sendCommands():
    try:
        d3 = double.DRDoubleSDK()
        d3.sendCommand('pose.resetOrigin');
        
    except KeyboardInterrupt:
        d3.close()
        print('Origin reset')
        sys.exit(0)

sendCommands()
