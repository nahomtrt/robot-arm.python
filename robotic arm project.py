import serial
import time

# Initialize Serial Communication
arduino = serial.Serial(port='COM3', baudrate=9600, timeout=1)

def send_command(command):
    """Send a command to the robotic arm via Serial."""
    arduino.write(command.encode())
    time.sleep(0.1)

send_command("M1:90;M2:45;M3:0")

def move_motor(joint, angle):
    """Move a specific motor (joint) to the desired angle."""
    command = f"M{joint}:{angle};"
    send_command(command)

move_motor(1, 90)

move_motor(2, 45)

import math

def calculate_angles(x, y, l1, l2):
    """Calculate joint angles for a 2D robotic arm with 2 links."""
    d = (x**2 + y**2)**0.5
    if d > l1 + l2:
        raise ValueError("Target out of reach")

    theta2 = math.acos((x**2 + y**2 - l1**2 - l2**2) / (2 * l1 * l2))
    theta1 = math.atan2(y, x) - math.atan2(l2 * math.sin(theta2), l1 + l2 * math.cos(theta2))

    return math.degrees(theta1), math.degrees(theta2)

link1_length = 10
link2_length = 10
x_target = 15
y_target = 5

theta1, theta2 = calculate_angles(x_target, y_target, link1_length, link2_length)
print(f"Joint 1 Angle: {theta1}, Joint 2 Angle: {theta2}")
