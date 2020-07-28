from SDK import double
import sys


def subscribeEvents():
    d3 = double.DRDoubleSDK()
    try:
        d3.sendCommand('events.subscribe', { 'events': [
        'DRGUI.accessoryWebView.message.to',
        'DRGUI.accessoryWebView.message.from',
        'DRNavigateModule.targetState',
        'DRNavigateModule.newTarget'

    ]})
        #d3.sendCommand('mics.setBoost',{'percent':0.25})
        d3.sendCommand('accessoryWebView.message.from',{'mic':'deafult'})
        d3.sendCommand('accessoryWebView.message.from',{'mic':'deafult'})
        #d3.sendCommand()
        while True:
            packet = d3.recv()
            if packet != None:
                event = packet['class'] + '.' + packet['key']
                if event == 'DRNavigateModule.newTarget':
                    print('new target = ---->', packet['data'], '<----')
                elif event == 'DRNavigateModule.targetState':
                    print('navigate target state  = ---->', packet['data'], '<----')
                elif event == 'DRGUI.accessoryWebView.message.to':
                    print('accessoryWebView.message.to = ---->', packet['data'], '<----')
                elif event == 'DRGUI.accessoryWebView.message.from':
                    print('DRGUI.accessoryWebView.message.from  = ---->', packet['data'], '<----')

    except KeyboardInterrupt:
        d3.close()
        print('cleaned up')
        sys.exit(0)



subscribeEvents()
