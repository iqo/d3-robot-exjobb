from SDK import double
import sys


def subscribeEvents():
    d3 = double.DRDoubleSDK()
    try:
        d3.sendCommand('events.subscribe', { 'events': [
        'DRWebRTC.stats',
        'DRWebRTC.event',
        'DRNavigateModule.targetState',
        'DRNavigateModule.newTarget'

    ]})
        d3.sendCommand('mics.setBoost',{'percent':0.25})
        d3.sendCommand('webrtc.enable',{'servers':[{'urls':'stun:rtc.doublerobotics.com'}],'transportPolicy':'all','manageCamera':False})
        d3.sendCommand('webrtc.setMicrophoneVolume', {'percent':20})
        while True:
            packet = d3.recv()
            if packet != None:
                event = packet['class'] + '.' + packet['key']
                if event == 'DRNavigateModule.newTarget':
                    print('new target = ---->', packet['data'], '<----')
                elif event == 'DRNavigateModule.targetState':
                    print('navigate target state  = ---->', packet['data'], '<----')
                elif event == 'DRWebRTC.stats':
                    print('DRWebRTC.stats  = ---->', packet['data'], '<----')
                elif event == 'DRWebRTC.event':
                    print('DRWebRTC.event  = ---->', packet['data'], '<----')

    except KeyboardInterrupt:
        d3.close()
        print('cleaned up')
        sys.exit(0)



subscribeEvents()
