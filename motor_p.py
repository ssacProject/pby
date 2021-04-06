from Adafruit_MotorHAT import Adafruit_MotorHAT
import time

# motor_left_ID = 1
# motor_right_ID = 2

def motor_INIT():
    # setup motor controller
    motor_driver = Adafruit_MotorHAT(i2c_bus=1)

    motor_left_ID = 1
    motor_right_ID = 2

    motor_left = motor_driver.getMotor(motor_left_ID)
    motor_right = motor_driver.getMotor(motor_right_ID)

    set_speed(motor_left_ID,   0.0)
    set_speed(motor_right_ID,  0.0)

    time.sleep(1.0)

    #motorFront(0.2, 0.2)
    print("init start")

# sets motor speed between [-1.0, 1.0]
def set_speed(motor_ID, value):

    max_pwm = 115.0
    speed = int(min(max(abs(value * max_pwm), 0), max_pwm))

    if motor_ID == 1:
            motor = motor_left
    elif motor_ID == 2:
            motor = motor_righ
    else:
            return
    
    motor.setSpeed(speed)

    if value > 0:
            motor.run(Adafruit_MotorHAT.BACKWARD)
    else:    
            motor.run(Adafruit_MotorHAT.FORWARD)

def motorFront(left, right):

    set_speed(1, 0.1)
    set_speed(2, 0.1)

def motorLeft(left, right):



    set_speed(motor_left_ID, left)
    set_speed(motor_right_ID,right)


def motorRight(left, right):



    set_speed(motor_left_ID, left)
    set_speed(motor_right_ID,right)

#def motorBack():
# stops all motors
def all_stop():
        motor_left.setSpeed(0)
        motor_right.setSpeed(0)

        motor_left.run(Adafruit_MotorHAT.RELEASE)
        motor_right.run(Adafruit_MotorHAT.RELEASE)


def motor_run(distance):
    
    if distance < 0 :
        if abs(distance) > 10:
            left +=0.1
            right -=0.1
            motorLeft(left,right)
            print("left motor up")
    else :
        if abs(distance) >10:
            left -=0.1
            right +=0.1
            motorRight(left,right)
            print("right motor up")
