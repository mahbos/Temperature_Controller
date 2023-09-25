# Temperature_Controller
Temperature Controller for Raspberry Pi using PID Control and DS18B20
This script demonstrates a PID controller that manages the temperature by actuating a heater and a fan using Raspberry Pi GPIO pins, based on readings from a DS18B20 temperature sensor.

Key Features:

Sensor Setup:
Utilizes DS18B20 temperature sensor.
Reads data directly from the Linux kernel's w1 subsystem.
Temperature Control:
Targets a pre-set desired temperature.
Uses PID control for error minimization.
Hardware Interactions:
GPIO pins are configured for the heater and fan.
PWM (Pulse Width Modulation) is employed to manage heater and fan intensities based on the PID output.
Temperature Reading:
get_current_temperature(): Fetches the current temperature from DS18B20.
Actuator Control:
control_heater_and_fan(output): Adjusts the intensity of the heater and fan based on the PID controller output.
Main Loop:
Continuously reads the temperature.
Adjusts the heater and fan based on PID control until the program is interrupted.
Safety:
Gracefully handles interruptions (e.g., KeyboardInterrupt) to turn off the heater and fan and cleanup GPIO.
To utilize this script, you'll need a Raspberry Pi, a DS18B20 temperature sensor, and appropriate setup for the heater and fan. Ensure you have the simple_pid module installed for PID control.
