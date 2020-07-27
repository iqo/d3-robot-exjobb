from SDK import double
import sys


def subscribeEvents():
    d3 = double.DRDoubleSDK()
    try:
        d3.sendCommand('events.subscribe', { 'events': [
        'DRMics.status',
        'DRMics.setBoostError',
        'DRNavigateModule.targetState'

    ]})
        d3.sendCommand('mics.setBoost',{'percent':0.25})
        d3.sendCommand('mics.requestStatus')


        while True:
            packet = d3.recv()
            if packet != None:
                event = packet['class'] + '.' + packet['key']
                if event == 'DRNavigateModule.newTarget':
                    print('new target = ---->', packet['data'], '<----')
                elif event == 'DRNavigateModule.targetState':
                    print('navigate target state  = ---->', packet['data'], '<----')
                elif event == 'DRMics.status':
                    print('DRMics.status  = ---->', packet['data'], '<----')
                elif event == 'DRMics.setBoostError':
                    print('DRMics.setBoostError  = ---->', packet['data'], '<----')

    except KeyboardInterrupt:
        d3.close()
        print('cleaned up')
        sys.exit(0)



subscribeEvents()
