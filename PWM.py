#Libraries
import RPi.GPIO as GPIO
import time

#Disable warnings
GPIO.setwarnings(False)

#Select GPIO mode
GPIO.setmode(GPIO.BCM)

#Set buzzer - pin GPIO13 as output and us PWM
buzzer = 13
GPIO.setup(buzzer, GPIO.OUT)
p1 = GPIO.PWM(buzzer, 500)

#Set LED - pin GPIO19 as output and use PWM
LED = 19
GPIO.setup(LED, GPIO.OUT)
p2 = GPIO.PWM(LED, 100)

#Set Ultrasonic pins
GPIO_TRIGGER = 4
GPIO_ECHO = 17
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

# method to take in readings from ultrasonic and calculate object distance 
def distance():
    # set Trigger to LOW and wait for sensor to settle
    GPIO.output(GPIO_TRIGGER, False)
    time.sleep(2)
 
    # set trigger to high
    GPIO.output(GPIO_TRIGGER, True)
    # set trigger to low after 0.01ms
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    
    # work out distance
    distance = TimeElapsed * 17150 

    # return distance of object
    return distance
 
# try catch to be able to exit the program and set LED and Buzzer to zero (off)
try:
    # start the two PWM channels
    p1.start(0)
    p2.start(0)
    
    # infinite loop until Crtl + C pressed 
    while True:
        # save the distance returned from distance() funtion in dist
        dist = distance()
        
        # cap distance at 200cm
        if dist > 200:
            dist = 200
        
        # work out duty cycle by dividing distance by max distance and
        # multiply by 100 to get a value from 0 to 100
        PWM_Output = (dist / 200) * 100
                
        # print distance to screen
        print("Distance:", dist)
        
        # set PWM channels duty cycle as the calculate value
        p1.ChangeDutyCycle(PWM_Output)
        p2.ChangeDutyCycle(PWM_Output)
        
        # wait for 100ms
        time.sleep(0.1)
 
# Reset by pressing CTRL + C
except KeyboardInterrupt:
    # stop p1 and p2
    p1.stop()
    p2.stop()
    GPIO.cleanup()
 
