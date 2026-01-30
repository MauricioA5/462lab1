from lab1_setup import *

if __name__ == "__main__":
    try:
        GPIO.add_event_detect(GATE.pin, GPIO.FALLING, bouncetime=200)
        GPIO.add_event_callback(GATE.pin, GPIO.FALLING, callback=TRAFFIC)
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
