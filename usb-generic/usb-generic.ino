#include <usbdrv.h>

#define RQ_SET_LED    0
#define RQ_GET_SWITCH 1
#define RQ_GET_LIGHT1  2
#define RQ_GET_LIGHT2  3
#define RQ_GET_LIGHT3  4

//////////////////////////////////////////////////////////////////////
usbMsgLen_t usbFunctionSetup(uint8_t data[8])
{
  usbRequest_t *rq = (usbRequest_t*)data;
  static uint8_t switch_state;
  static uint16_t ldr_value1, ldr_value2, ldr_value3;

  if (rq->bRequest == RQ_SET_LED)
  {
    uint8_t led_val = rq->wValue.bytes[0];
    uint8_t led_no  = rq->wIndex.bytes[0];

    if (led_no == 0)
      digitalWrite(PIN_PB0, led_val);
    else if (led_no == 1)
      digitalWrite(PIN_PB2, led_val);
    else if (led_no == 2)
      digitalWrite(PIN_PB4, led_val);

    return 0;  // return no data back to host
  }

  else if (rq->bRequest == RQ_GET_SWITCH)
  {
    if (digitalRead(PIN_PB5) == LOW) /* switch is pressed */ 
      switch_state = 1;
    else
      switch_state = 0;

    /* point usbMsgPtr to the data to be returned to host */
    usbMsgPtr = (uint8_t*) &switch_state;

    /* return the number of bytes of data to be returned to host */
    return sizeof(switch_state);
  }
  
  else if (rq->bRequest == RQ_GET_LIGHT1)
  {
    ldr_value1 = analogRead(PIN_PC0);
    usbMsgPtr = (uint8_t*) &ldr_value1;
    return sizeof(ldr_value1);
  }
  
  else if (rq->bRequest == RQ_GET_LIGHT2)
  {
    ldr_value2 = analogRead(PIN_PC1);
    usbMsgPtr = (uint8_t*) &ldr_value2;
    return sizeof(ldr_value2);
  }
  
  else if (rq->bRequest == RQ_GET_LIGHT3)
  {
    ldr_value3 = analogRead(PIN_PC2);
    usbMsgPtr = (uint8_t*) &ldr_value3;
    return sizeof(ldr_value3);
  }


  return 0;   /* nothing to do; return no data back to host */
}

//////////////////////////////////////////////////////////////////////
void setup()
{
    pinMode(PIN_PC0,INPUT);
    pinMode(PIN_PC1,INPUT);
    pinMode(PIN_PC2,INPUT);
    pinMode(PIN_PB5,INPUT_PULLUP);
    pinMode(PIN_PB0,OUTPUT);
    pinMode(PIN_PB2,OUTPUT);
    pinMode(PIN_PB4,OUTPUT);
    // pinMode(PIN_PC4,INPUT);
    pinMode(PIN_PD3,OUTPUT);

    usbInit();

    /* enforce re-enumeration of USB devices */
    usbDeviceDisconnect();
    delay(300);
    usbDeviceConnect();
}

//////////////////////////////////////////////////////////////////////
void loop()
{
  usbPoll();
}
