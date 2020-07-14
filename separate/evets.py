from SDK import double
import sys


def subscribeEvents():
    d3 = double.DRDoubleSDK()
    try:
        d3.sendCommand('events.subscribe', { 'events': [
        'DRBase.status',
        'DRCamera.enable',
        'DRCamera.hitResult',
        'DRNavigateModule.arrive',
        'DRNavigateModule.target',
        'DRNavigateModule.targetState'
    ]})
        while True:
            packet = d3.recv()
            if packet != None:
                event = packet['class'] + '.' + packet['key']
                ''' if event == 'DRBase.status':
                print(packet['data']) '''
                if event == 'DRCamera.enable':
                    print('camera enabled')
                elif event == 'DRCamera.hitResult':
                    print('camerahitResult = ---->', packet['data'], '<----')
                elif event == 'DRNavigateModule.arrive':
                    print('navigate arrive = ---->', packet['data'], '<----')
                elif event == 'DRNavigateModule.target':
                    print('navigate target = ---->', packet['data'], '<----')
                elif event == 'DRNavigateModule.targetState':
                    print('navigate target state  = ---->', packet['data'], '<----')    

    except KeyboardInterrupt:
        d3.close()
        print('cleaned up')
        sys.exit(0)