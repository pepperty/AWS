import RPi.GPIO as GPIO
import os
import time

# Define GPIO to use on Pi
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
IO_01 = 5
IO_02= 6
IO_03 = 13
IO_04 = 19
IO_05= 26

# ULtrasonic trigger time
TRIGGER_TIME = 0.00001
MAX_TIME = 0.05  # max time waiting for response in case something is missed

# GPIO.setup(IO_TRIG01, GPIO.OUT)  # Trigger
# GPIO.setup(IO_EXC01, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Echo
# GPIO.setup(IO_TRIG02, GPIO.OUT)  # Trigger
# GPIO.setup(IO_EXC02, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Echo

GPIO.setup(IO_01, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IO_02, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IO_03, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IO_04, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IO_05, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# out  = 0 # test
# if out == 0:
#     GPIO.output(IO_EXC01, False)
#     GPIO.output(IO_EXC02, False)
#     GPIO.output(IO_DET01, False)
#     GPIO.output(IO_DET02, False)
#     GPIO.output(IO_TRIG01, False)
#     GPIO.output(IO_TRIG02, False)
#     GPIO.output(IO_REL01, False)
#     GPIO.output(IO_REL02, False)
# if out == 1:
#     GPIO.output(IO_EXC01, True)
#     GPIO.output(IO_EXC02, True)
#     GPIO.output(IO_DET01, True)
#     GPIO.output(IO_DET02, True)
#     GPIO.output(IO_TRIG01, True)
#     GPIO.output(IO_TRIG02, True)
#     GPIO.output(IO_REL01, True)
#     GPIO.output(IO_REL02, True)


# # This function measures a distance
# def measure():
#     # Pulse the trigger/echo line to initiate a measurement
#     GPIO.output(IO_TRIG01, True)
#     time.sleep(TRIGGER_TIME)
#     GPIO.output(IO_TRIG01, False)

#     # ensure start time is set in case of very quick return
#     start = time.time()
#     timeout = start + MAX_TIME

#     # set line to input to check for start of echo response
#     while GPIO.input(IO_EXC01) == 0 and start <= timeout:
#         start = time.time()

#     if(start > timeout):
#         return -1

#     stop = time.time()
#     timeout = stop + MAX_TIME
#     # Wait for end of echo response
#     while GPIO.input(IO_EXC01) == 1 and stop <= timeout:
#         stop = time.time()

#     if(stop <= timeout):
#         elapsed = stop-start
#         distance = float(elapsed * 34300)/2.0
#     else:
#         return -1
#     return distance

# print ("")
if __name__ == '__main__':
    try:
        while True:
            # distance = measure()
            # if(distance > -1):
            #     print("Measured Distance = %.1f cm" % distance)
            # else:
            #     print("#")
            if GPIO.input(IO_01) == 0:
                print("1")
            if GPIO.input(IO_01) == 0:
                print("2")
            if GPIO.input(IO_01) == 0:
                print("3")
            if GPIO.input(IO_01) == 0:
                print("4")
            if GPIO.input(IO_01) == 0:
                print("5")
            time.sleep(1)
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()