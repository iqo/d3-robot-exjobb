from SDK import double
import sys

def sendCommands():
    d3 = double.DRDoubleSDK()
    try:
        d3.sendCommand('pose.resetOrigin');
    except KeyboardInterrupt:
        d3.close()
        print('Origin reset')
        sys.exit(0)

sendCommands()
