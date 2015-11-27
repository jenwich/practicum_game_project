from practicum import findDevices
from peri import PeriBoard

devs = findDevices()

if len(devs) == 0:
    print "*** No MCU board found."
    exit(1)

board = PeriBoard(devs[0])
print "*** MCU board found"
print "*** Device manufacturer: %s" % board.getVendorName()
print "*** Device name: %s" % board.getDeviceName()

minLight = [9999, 9999, 9999]
maxLight = [0, 0, 0]

while(1):
    for i in range(0, 3):
        light = board.getLight(i)
        if light > maxLight[i]:
            maxLight[i] = light
        if light < minLight[i]:
            minLight[i] = light
    print (minLight[0], maxLight[0]), (minLight[1], maxLight[1]), (minLight[2], maxLight[2])
