from SDK import double
import sys


def subscribeEvents():
    d3 = double.DRDoubleSDK()
    try:
        d3.sendCommand('events.subscribe', { 'events': [
        'DRBase.status',
        'DRCamera.enable',
        'DRNavigateModule.targetState',
        'DRNavigateModule.newTarget',
        'DRPose.resetOrigin',
        'DRPose.pose',
        'DRPose.model'
    ]})
        while True:
            packet = d3.recv()
            if packet != None:
                event = packet['class'] + '.' + packet['key']
                ''' if event == 'DRBase.status':
                print(packet['data']) '''
                if event == 'DRCamera.enable':
                    print('camera enabled')
                elif event == 'DRNavigateModule.newTarget':
                    print('new target = ---->', packet['data'], '<----')
                elif event == 'DRNavigateModule.targetState':
                    print('navigate target state  = ---->', packet['data'], '<----')
                elif event == 'DRPose.resetOrigin':
                    print('DRPose.resetOrigin  = ---->', packet['data'], '<----')
                elif event == 'DRPose.pose':
                    print('DRPose.pose  = ---->', packet['data'], '<----')
                elif event == 'DRPose.model':
                    print('DRPose.model  = ---->', packet['data'], '<----')

    except KeyboardInterrupt:
        d3.close()
        print('cleaned up')
        sys.exit(0)



subscribeEvents()
