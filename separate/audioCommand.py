import time
import speech_recognition as sr
import navigate
import autoNavigateClass

drive = navigate.Navigate()
autoDrive = autoNavigateClass.AutoNavigate()
while True:
    r = sr.Recognizer()
    m = sr.Microphone(device_index=29)
    with m as source:
        r.adjust_for_ambient_noise(source,duration=5)
        print("Say Something")
        audio=r.listen(source)
    try:    
        inputAudio = r.recognize_google(audio)
        print("did you say: ", r.recognize_google(audio),"\n")
        if inputAudio == "test":
            print('start start')
            drive.init_client()
            drive.navigateHitResult()
        elif inputAudio == "auto":
            autoDrive.navigateHitResult()

    except sr.UnknownValueError:
        print("could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))