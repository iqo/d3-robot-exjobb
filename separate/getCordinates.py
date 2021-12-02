import json

testData = '{"host":"WFGATEWAY-3ABFF8D01EFF","message":"REPORT:42478B1A6B8CBA16,0.2.7,5051,6467,1043,0,0,0,3.92,-91.21,588646*9ABD","source":"03FF5C0A2BFA3A9B","time":"2020-07-22T10:27:48.710457759Z","type":"widefind_message"}'
def parsCordinates(jsonData):
    testParse = json.loads(jsonData)
    cords = testParse['message']
    print(cords)
    count = 0
    for n in cords:
        if n == ',':
            count = 1 + count
    split_string = cords.split(",", count)
    xInMeter = (float(split_string[2])/1000)
    yInMeter = (float(split_string[3])/1000)
    zInMeter = (float(split_string[4])/1000)
    print('x cord: ', xInMeter)
    print('y cord: ', yInMeter)
    print('z cord: ', zInMeter)

parsCordinates(testData)