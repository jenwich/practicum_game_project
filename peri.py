from practicum import McuBoard

RQ_SET_LED    = 0
RQ_GET_SWITCH = 1
RQ_GET_LIGHT  = 2

####################################
class PeriBoard(McuBoard):

    ################################
    def setLed(self, led_no, led_val):
        '''
        Set status of LED led_no on peripheral board to led_val
        '''
        self.usbWrite(request=RQ_SET_LED,index=led_no,value=led_val)
        # return

    ################################
    def setLedValue(self, value):
        '''
        Display value's 3 LSBs on peripheral board's LEDs
        '''
        self.setLed(0, value%2)
        value /= 2
        self.setLed(1, value%2)
        value /= 2
        self.setLed(2, value%2)

    ################################
    def getSwitch(self):
        '''
        Return a boolean value indicating whether the switch on the peripheral
        board is currently pressed
        '''
        x = self.usbRead(request=RQ_GET_SWITCH,length=1)
        return bool(x[0])

    ################################
    def getLight(self):
        '''
        Return the current reading of light sensor on peripheral board
        '''
        x = self.usbRead(request=RQ_GET_LIGHT, length=2)
        return x[1]*256 + x[0]
