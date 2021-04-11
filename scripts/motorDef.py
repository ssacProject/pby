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
def all_stop(state):
    if state == 2:
        state = 3 
        motor_right_direction(0.35, 0.2)
    elif state == 3 : 
        state = 2 
        motor_left_direction(0.2, 0.35)
    

def real_stop():

    motor_left.setSpeed(0)
    motor_right.setSpeed(0)

    motor_left.run(Adafruit_MotorHAT.RELEASE)
    motor_right.run(Adafruit_MotorHAT.RELEASE)
 
 # go front
def motor_start(left_value, right_value):
    set_speed(motor_left_ID, left_value)
    set_speed(motor_right_ID, right_value)
    
# go left
def motor_left_direction(left_value, right_value):
    set_speed(motor_left_ID, left_value)
    set_speed(motor_right_ID, right_value)
    
# go right
def motor_right_direction(left_value, right_value):
    set_speed(motor_left_ID, left_value)
    set_speed(motor_right_ID, right_value)
    
# motor init    
motor_driver = Adafruit_MotorHAT(i2c_bus=1)

motor_left_ID = 1
motor_right_ID = 2

motor_left = motor_driver.getMotor(motor_left_ID)
motor_right = motor_driver.getMotor(motor_right_ID)

set_speed(motor_left_ID,   0.0)
set_speed(motor_right_ID,  0.0)

#time.sleep(0.1)

#set_speed(motor_left_ID, 0.0)
#set_speed(motor_right_ID, 0.0)

def motor_run(distance, state):
    dist_range = 25
    #global state
    
    if distance is None:
        print("distance is None")
        #return -1

    if dist_range >= abs(distance) :#25 state = 1
        state = 1

        motor_start(0.3, 0.3)
        #print("go front !!")
    elif -50 < distance < -dist_range : #state = 2
        state = 2
        motor_left_direction(0.2, 0.23) # 0.2 0.25 left wheel
        #print("go left1 !!")
    elif 50 > distance > dist_range : # state = 3
        state = 3
        motor_right_direction(0.23, 0.2) # 0.26, 0.2 right wheel
        #print("go right1 !!")
    elif -80 < distance <= -50:
        state = 2
        motor_left_direction(0.2, 0.26)
    elif 50 >= distance > 80:
        state = 3
        motor_right_direction(0.26, 0.2)

    elif distance <= -80 : #state = 2
        state = 2 
        motor_left_direction(0.2, 0.28)
        #print("go left2 !!")
    elif distance >= 80 : # state = 3
        state = 3
        motor_right_direction(0.28, 0.2)
        #print("go right2 !!")
        #all_stop()
        #print("distance is None")
    return state   
