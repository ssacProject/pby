from Adafruit_MotorHAT import Adafruit_MotorHAT
import time


# setup motor controller

# motor_left =0
# motor_right=0

# sets motor speed between [-1.0, 1.0]
def set_speed(motor_ID, value):
	max_pwm = 115.0
	speed = int(min(max(abs(value * max_pwm), 0), max_pwm))

	if motor_ID == 1:
		motor = motor_left
	elif motor_ID == 2:
		motor = motor_right
	else:
		return
	
	motor.setSpeed(speed)

	if value > 0:
		motor.run(Adafruit_MotorHAT.BACKWARD)
	else:                
		motor.run(Adafruit_MotorHAT.FORWARD)


# stops all motors
def all_stop():
	motor_left.setSpeed(0)
	motor_right.setSpeed(0)

	motor_left.run(Adafruit_MotorHAT.RELEASE)
	motor_right.run(Adafruit_MotorHAT.RELEASE)
 
 # go front
def motor_start():
    set_speed(motor_left_ID, 0.2)
    set_speed(motor_right_ID, 0.2)
    
# go left
def motor_left_direction():
    set_speed(motor_left_ID, 0.2)
    set_speed(motor_right_ID, 0.25)
    
# go right
def motor_right_direction():
    set_speed(motor_left_ID, 0.25)
    set_speed(motor_right_ID, 0.2)
    
# motor init    

motor_driver = Adafruit_MotorHAT(i2c_bus=1)

motor_left_ID = 1
motor_right_ID = 2

motor_left = motor_driver.getMotor(motor_left_ID)
motor_right = motor_driver.getMotor(motor_right_ID)

set_speed(motor_left_ID,   0.0)
set_speed(motor_right_ID,  0.0)

time.sleep(0.1)

#set_speed(motor_left_ID, 0.0)
#set_speed(motor_right_ID, 0.0)

left = 0.0
right = 0.0

def motor_run(distance):
    if distance is None:
        print("distance is None")
        return -1

    if 25 >= abs(distance) > 0:
        motor_start()
        print("front !!")
    elif distance < -25 :
        motor_left_direction()
        print("right !!")
    elif distance > 25 :
        motor_right_direction()
        print("left !!")
    else :
        all_stop()
        print("distance is None")
        
