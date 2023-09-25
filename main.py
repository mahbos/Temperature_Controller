import os
import glob
import time
from simple_pid import PID
import RPi.GPIO as GPIO

# DS18B20 setup
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

# Settings
DESIRED_TEMPERATURE = 25  # in Celsius

# GPIO settings
HEATER_PIN = 17
FAN_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(HEATER_PIN, GPIO.OUT)
GPIO.setup(FAN_PIN, GPIO.OUT)

heater_pwm = GPIO.PWM(HEATER_PIN, 100)
fan_pwm = GPIO.PWM(FAN_PIN, 100)
heater_pwm.start(0)
fan_pwm.start(0)

def read_temp_raw():
    with open(device_file, 'r') as f:
        return f.readlines()

def get_current_temperature():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

def control_heater_and_fan(output):
    if output > 0:
        heater_pwm.ChangeDutyCycle(min(output*100, 100))
        fan_pwm.ChangeDutyCycle(0)
    elif output < 0:
        fan_pwm.ChangeDutyCycle(min(-output*100, 100))
        heater_pwm.ChangeDutyCycle(0)
    else:
        heater_pwm.ChangeDutyCycle(0)
        fan_pwm.ChangeDutyCycle(0)

# PID controller setup
pid = PID(1, 0.1, 0.01, setpoint=DESIRED_TEMPERATURE)
pid.output_limits = (-1, 1)  # outputs can range from -1 to 1

try:
    while True:
        current_temperature = get_current_temperature()
        output = pid(current_temperature)
        control_heater_and_fan(output)
        print(f"Current Temperature: {current_temperature}C, PID Output: {output}")
        time.sleep(5)  # wait for 5 seconds before checking again

except KeyboardInterrupt:
    heater_pwm.stop()
    fan_pwm.stop()
    GPIO.cleanup()
