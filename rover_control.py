import pygame
from time import sleep


#pygame.joystick.init()
#joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

joystick = pygame.joystick.Joystick(0)
screen = pygame.display.set_mode((400, 600))

import RPi.GPIO as GPIO
from time import sleep

ledpin_left = (12, 18)
ledpin_right = (13, 19)				# PWM pin connected to LED
GPIO.setwarnings(False)			#disable warnings
GPIO.setmode(GPIO.BOARD)		#set pin numbering system

GPIO.setup(ledpin_left[0], GPIO.OUT)
GPIO.setup(ledpin_left[1], GPIO.OUT)
GPIO.setup(ledpin_right[0], GPIO.OUT)
GPIO.setup(ledpin_right[1], GPIO.OUT)
PWM_OFF = 15

pwm_left_rear = GPIO.PWM(ledpin_left[0], 100)		#create PWM instance with frequency
pwm_left_front = GPIO.PWM(ledpin_left[1], 100)		#create PWM instance with frequency
pwm_right_rear = GPIO.PWM(ledpin_right[0], 100)
pwm_right_front = GPIO.PWM(ledpin_right[1], 100)

pwm_left_rear.start(15)				#start PWM of required Duty Cycle 
pwm_left_front.start(15)
pwm_right_rear.start(15)
pwm_right_front.start(15)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT():
            pygame.quit()
    
    # print analog axes
    y_offset = 50
    for axis in range(joystick.get_numaxes()):
        axis_val = joystick.get_axis()
        font = pygame.font.get_default_font()
        axis_text = font.render(str(axis), True, (1, 1, 1))
        val_text = font.render(str(axis_val), True, (1, 1, 1))
        # Print axis and value pairs
        screen.blit(axis_text, (20, y_offset))
        screen.blit(val_text, (200, y_offset))

        y_offset += 30

    # forward and backward
    left_axis = joystick.get_axis(1)
    right_axis = joystick.get_axis(4)

    left_duty_cycle = left_axis**3 * 10 + 15
    right_duty_cycle = right_axis**3 * 10 + 15

    # button 5 should be right bumper
    # should only move if rb is pressed
    if joystick.get_button(5):
        pwm_left_rear.ChangeDutyCycle(left_duty_cycle)
        pwm_left_front.ChangeDutyCycle(left_duty_cycle)
        pwm_right_front.ChangeDutyCycle(right_duty_cycle)
        pwm_right_rear.ChangeDutyCycle(right_duty_cycle)
    else:
        pwm_left_rear.ChangeDutyCycle(PWM_OFF)
        pwm_left_front.ChangeDutyCycle(PWM_OFF)
        pwm_right_front.ChangeDutyCycle(PWM_OFF)
        pwm_right_rear.ChangeDutyCycle(PWM_OFF)

    sleep(0.01)
    
    # full reverse - 10

    # full forward - 20

    
