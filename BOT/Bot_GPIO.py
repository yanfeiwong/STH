############Bot's GPIO#########
import RPi.GPIO as GPIO
import time
IN1 = 12
IN2 = 13
ENA = 6
IN3 = 20
IN4 = 21
ENB = 26
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(IN1,GPIO.OUT)
GPIO.setup(IN2,GPIO.OUT)
GPIO.setup(IN3,GPIO.OUT)
GPIO.setup(IN4,GPIO.OUT)
GPIO.setup(ENA,GPIO.OUT)
GPIO.setup(ENB,GPIO.OUT)
PWMA = GPIO.PWM(ENA,500)
PWMB = GPIO.PWM(ENB,500)
PWMA.start(50)
PWMB.start(50)
def stop():
		GPIO.output(IN1,GPIO.LOW)
		GPIO.output(IN2,GPIO.LOW)
		GPIO.output(IN3,GPIO.LOW)
		GPIO.output(IN4,GPIO.LOW)

def forward():
		GPIO.output(IN1,GPIO.HIGH)
		GPIO.output(IN2,GPIO.LOW)
		GPIO.output(IN3,GPIO.LOW)
		GPIO.output(IN4,GPIO.HIGH)
def backward(self):
		GPIO.output(IN1,GPIO.LOW)
		GPIO.output(IN2,GPIO.HIGH)
		GPIO.output(IN3,GPIO.HIGH)
		GPIO.output(IN4,GPIO.LOW)

def left(self):
		GPIO.output(IN1,GPIO.LOW)
		GPIO.output(IN2,GPIO.LOW)
		GPIO.output(IN3,GPIO.LOW)
		GPIO.output(IN4,GPIO.HIGH)

def right(self):
		GPIO.output(IN1,GPIO.HIGH)
		GPIO.output(IN2,GPIO.LOW)
		GPIO.output(IN3,GPIO.LOW)
		GPIO.output(IN4,GPIO.LOW)
def setPWMA(value):
		PWMA.ChangeDutyCycle(value)

def setPWMB(value):
		PWMB.ChangeDutyCycle(value)
def setMotor(left, right):
                left=-left
		if((right >= 0) and (right <= 100)):
			GPIO.output(IN1,GPIO.HIGH)
			GPIO.output(IN2,GPIO.LOW)
			PWMA.ChangeDutyCycle(right)
		elif((right < 0) and (right >= -100)):
			GPIO.output(IN1,GPIO.LOW)
			GPIO.output(IN2,GPIO.HIGH)
			PWMA.ChangeDutyCycle(0 - right)
		if((left >= 0) and (left <= 100)):
			GPIO.output(IN3,GPIO.HIGH)
			GPIO.output(IN4,GPIO.LOW)
			PWMB.ChangeDutyCycle(left)
		elif((left < 0) and (left >= -100)):
			GPIO.output(IN3,GPIO.LOW)
			GPIO.output(IN4,GPIO.HIGH)
			PWMB.ChangeDutyCycle(0 - left)
