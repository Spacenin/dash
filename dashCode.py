import RPi.GPIO as GPIO
import os
from datetime import datetime
from time import sleep
from picamera import PiCamera

#Create camera
camera = PiCamera()
sleep(2)
camera.resolution = (1920, 1080)

#Setup button pins
startButton = 23
stopButton = 22
offButton = 24

#Setup GPIO connections
GPIO.setmode(GPIO.BCM)

GPIO.setup(startButton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(stopButton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(offButton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#Loop continuously
while 1:
    #Check capture button
    if GPIO.input(startButton):
        #Log to file
        f = open("/home/chep6/dash/dashLog.txt", "a")
        f.write("Capture start - " + str(datetime.now()) + "\n")
        f.close()
    
        #Start recording
        camera.start_recording("/home/chep6/dash/recordings/recording-" + str(datetime.now()) + ".h264")
        
        #Record while not pressed stop
        while 1:
            if GPIO.input(stopButton):
                #Log to file
                f = open("/home/chep6/dash/dashLog.txt", "a")
                f.write("Capture stop - " + str(datetime.now()) + "\n")
                f.close()

                camera.stop_recording()

                break

    #Check off button
    if GPIO.input(offButton):
        #Log to file
        f = open("/home/chep6/dash/dashLog.txt", "a")
        f.write("Shutting down - " + str(datetime.now()) + "\n")
        f.close()
        
        #Close pi
        os.system("sudo shutdown -h now")
