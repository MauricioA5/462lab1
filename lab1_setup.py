import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)     # Disable warnings
GPIO.setmode(GPIO.BCM)      # Use Broadcom pin numbering (GPIO pin numbers, not physical pin numbers)

class GPIO_OUTPUT:
    def __init__(self, pins):
        #initialize GPIO
        self.pins = pins
        for i in pins:
            GPIO.setup(i, GPIO.OUT, initial=GPIO.LOW)
    def on(self, num):
        GPIO.output(num, GPIO.HIGH)
    def clear(self):
        for i in self.pins:
            GPIO.output(i, GPIO.LOW)
    def size_check(self, size):
        if(len(self.pins) != size):
            raise ValueError(f'Expected Pins: {size}, Received: {len(self.pins)}')

class LED(GPIO_OUTPUT):
    def __init__(self,pins):
        super().__init__(pins)
        self.size_check(3)
        self.RGB = {
            "R": self.pins[0],
            "G": self.pins[1],
            "B": self.pins[2]
        }
    def set(self,color):
        self.clear()
        self.on(self.RGB[color])
    def flash(self, color, times,period=0.5):
        for i in range(times):
            self.set(color)
            time.sleep(period)
            self.clear()
            time.sleep(period)
        
class SEG_DISPLAY(GPIO_OUTPUT):
    def __init__(self,pins):
        super().__init__(pins)
        self.size_check(7)
        self.TOP_RIGHT = self.pins[0]
        self.TOP = self.pins[1]
        self.TOP_LEFT = self.pins[2]
        self.CENTER = self.pins[3]
        self.BOTTOM_RIGHT = self.pins[4]
        self.BOTTOM = self.pins[5]
        self.BOTTOM_LEFT = self.pins[6]
        # Number Mapping
        self.digits = {
            0: [self.TOP_LEFT, self.TOP, self.TOP_RIGHT, self.BOTTOM_LEFT, self.BOTTOM, self.BOTTOM_RIGHT],
            1: [self.TOP_RIGHT, self.BOTTOM_RIGHT],
            2: [self.TOP, self.TOP_RIGHT, self.CENTER, self.BOTTOM_LEFT, self.BOTTOM],
            3: [self.TOP, self.TOP_RIGHT, self.CENTER, self.BOTTOM_RIGHT, self.BOTTOM],
            4: [self.TOP_LEFT, self.CENTER, self.TOP_RIGHT, self.BOTTOM_RIGHT],
            5: [self.TOP, self.TOP_LEFT, self.CENTER, self.BOTTOM_RIGHT, self.BOTTOM],
            6: [self.TOP, self.TOP_LEFT, self.CENTER, self.BOTTOM_LEFT, self.BOTTOM, self.BOTTOM_RIGHT],
            7: [self.TOP, self.TOP_RIGHT, self.BOTTOM_RIGHT],
            8: self.pins,  # all segments
            9: [self.TOP, self.TOP_LEFT, self.TOP_RIGHT, self.CENTER, self.BOTTOM_RIGHT, self.BOTTOM],
        }
    def display(self,num):
        self.clear()
        for i in self.digits[num]:
            self.on(i)
    def countdown(self, led):
        for i in range(9,-1,-1):
            self.display(i)
            if i <= 4:
                led.flash("B", 1)
            else:
                time.sleep(1)
        self.clear()

class BUTTON:
    def __init__(self,pin):
        self.pin = pin
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    def IS_PRESSED(self):
        return GPIO.input(self.pin) == GPIO.HIGH


# Hardware Components
LED1 = LED([17,27,22])
LED2 = LED([23,24,25])
DISPLAY = SEG_DISPLAY([6,13,19,26,16,20,21])
GATE = BUTTON(12)

def TRAFFIC(channel):
    global cooldown_time
    if not (time.time() < cooldown_time):
        cooldown_time = time.time() + 20
        #4b
        LED2.flash("B", 3,0.5)
        LED2.set("R")
        #4c
        LED1.set("G")
        #4d
        DISPLAY.countdown(LED1)
        #4e
        LED1.set("R")
        LED2.set("G") #4a
    
    

cooldown_time = 0