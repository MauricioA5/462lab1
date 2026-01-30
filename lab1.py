from lab1_setup import *

if __name__ == "__main__":
    LED2.set("G")
    try:
        while(True):
            time.sleep(0.01)
            if(GATE.IS_PRESSED()):
                # Set Cooldown (4f)
                TRAFFIC()
                
    except KeyboardInterrupt:
        GPIO.cleanup()

