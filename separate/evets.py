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
        mics = [{'deviceId': 'default', 'label': 'Default'}, {'deviceId': '5e8b0f4ab10c10738ebcd48e7dccc13e77cdddfde57a62e572832cea2f7135f1', 'label': 'Mic Rear Center'}, {'deviceId': '44a3555dfc5944c9181460fd7e94262145672678a6992df0e5f614de6252ccdd', 'label': 'Mic Front Center'}, {'deviceId': '6f185b2d609490ba81582f9e352aa43662b0f404e2762845bb6708b90a375ff6', 'label': 'Mic Front Left/Right'}, {'deviceId': '88bfaf9b4a0527df3337062c17cf5c8e596708ba06084bb2e91116d34f74c03d', 'label': 'Mic Ears Left/Right'}]
        #d3.sendCommand('mics.setBoost',{'percent':0.25})
        d3.sendCommand('accessoryWebView.message.from',{mics:mics})
        d3.sendCommand('accessoryWebView.message.to',{'mic':'deafult'})
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


