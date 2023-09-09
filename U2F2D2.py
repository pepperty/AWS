import RPi.GPIO as GPIO
import os
import time

# Define GPIO to use on Pi
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

IO_DET01 = 18
IO_DET02= 23
IO_EXC01 = 24
IO_EXC02 = 25
IO_TRIG01= 8
IO_TRIG02 = 7
IO_REL01 = 12
IO_REL02 = 16

# ULtrasonic trigger time
TRIGGER_TIME = 0.00001
MAX_TIME = 0.05  # max time waiting for response in case something is missed

GPIO.setup(IO_DET01, GPIO.IN, pull_up_down=GPIO.PUD_Down)
GPIO.setup(IO_DET02, GPIO.IN, pull_up_down=GPIO.PUD_Down)
GPIO.setup(IO_EXC01, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IO_EXC02, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IO_TRIG01, GPIO.OUT)
GPIO.setup(IO_TRIG02, GPIO.OUT)
GPIO.setup(IO_REL01, GPIO.OUT)
GPIO.setup(IO_REL02, GPIO.OUT)

# This function measures a distance
def measure(IO_TRIG,IO_EXC):
    # Pulse the trigger/echo line to initiate a measurement
    GPIO.output(IO_TRIG, True)
    time.sleep(TRIGGER_TIME)
    GPIO.output(IO_TRIG, False)

    # ensure start time is set in case of very quick return
    start = time.time()
    timeout = start + MAX_TIME

    # set line to input to check for start of echo response
    while GPIO.input(IO_EXC) == 0 and start <= timeout:
        start = time.time()

    if(start > timeout):
        return -1

    stop = time.time()
    timeout = stop + MAX_TIME
    # Wait for end of echo response
    while GPIO.input(IO_EXC) == 1 and stop <= timeout:
        stop = time.time()

    if(stop <= timeout):
        elapsed = stop-start
        distance = float(elapsed * 34300)/2.0
    else:
        return -1
    return distance

if __name__ == '__main__':
    try:
        while True:
            dist_A  = 0
            dist_B  = 0
            dist_A  = measure(IO_TRIG01,IO_EXC01)
            dist_B  = measure(IO_TRIG02,IO_EXC02)

            if(dist_A > -1):
                print("Measured Distance = %.1f cm" % dist_A)
            else:
                print("#UA")
            if(dist_B > -1):
                print("Measured Distance = %.1f cm" % dist_A)
            else:
                print("#UB")
            time.sleep(0.1)

            # Read the state of the GPIO pin
            DET01_state = GPIO.input(IO_DET01)
            DET02_state = GPIO.input(IO_DET02)

            # Print the state (it should read LOW when the button is not pressed)
            if DET01_state == GPIO.HIGH:
                print("DET01 Detect")
            else:
                print("DET01 Non Detect")
            if DET02_state == GPIO.HIGH:
                print("DET02 Detect")
            else:
                print("DET02 Non Detect")

            # Add a small delay to avoid rapid readings
            time.sleep(0.1)

            

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
    except Exception as e:
        print(f"An error occurred: {e}")
        GPIO.cleanup()
    GPIO.cleanup()