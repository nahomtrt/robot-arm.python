import tkinter as tk
from gpiozero import Servo
import pyttsx3
import speech_recognition as sr
from time import sleep
import threading

# Initialize Text-to-Speech
engine = pyttsx3.init()

# Servo configurations
servo_joint_1 = Servo(17)  # Replace GPIO 17 with the pin for Joint 1
servo_joint_2 = Servo(18)  # Replace GPIO 18 with the pin for Joint 2
joint_1_angle = 0
joint_2_angle = 0

# Joint limits
JOINT_1_LIMITS = (-90, 90)
JOINT_2_LIMITS = (-90, 90)

# Safety mechanism flags
emergency_stop = False


# --- Helper Functions ---
def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()


def set_joint_angle(servo, angle, joint_name):
    """Set the servo to a specific angle with limit checks."""
    global emergency_stop
    if emergency_stop:
        speak("Emergency stop is active. Unable to move.")
        return
    
    if joint_name == "Joint 1" and not JOINT_1_LIMITS[0] <= angle <= JOINT_1_LIMITS[1]:
        speak("Joint 1 angle out of bounds.")
        return
    if joint_name == "Joint 2" and not JOINT_2_LIMITS[0] <= angle <= JOINT_2_LIMITS[1]:
        speak("Joint 2 angle out of bounds.")
        return
    
    # Convert angle to servo value (-1 to 1)
    servo.value = angle / 90.0
    speak(f"{joint_name} moved to {angle} degrees.")
    print(f"{joint_name} set to {angle} degrees.")


def move_joint(command):
    """Interpret voice command and move joints."""
    global joint_1_angle, joint_2_angle
    if "up" in command:
        joint_2_angle += 10
        set_joint_angle(servo_joint_2, joint_2_angle, "Joint 2")
    elif "down" in command:
        joint_2_angle -= 10
        set_joint_angle(servo_joint_2, joint_2_angle, "Joint 2")
    elif "left" in command:
        joint_1_angle -= 10
        set_joint_angle(servo_joint_1, joint_1_angle, "Joint 1")
    elif "right" in command:
        joint_1_angle += 10
        set_joint_angle(servo_joint_1, joint_1_angle, "Joint 1")
    elif "stop" in command:
        global emergency_stop
        emergency_stop = True
        speak("Emergency stop activated.")
    elif "resume" in command:
        emergency_stop = False
        speak("Resuming operations.")
    elif "calibrate" in command:
        calibrate_arm()
    else:
        speak("Command not recognized. Please try again.")


def calibrate_arm():
    """Reset the arm to its initial position."""
    global joint_1_angle, joint_2_angle
    joint_1_angle = 0
    joint_2_angle = 0
    set_joint_angle(servo_joint_1, joint_1_angle, "Joint 1")
    set_joint_angle(servo_joint_2, joint_2_angle, "Joint 2")
    speak("Calibration complete. Arm reset to initial position.")


def listen_for_commands():
    """Continuously listen for voice commands."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Voice recognition activated. Listening for commands.")
        while True:
            try:
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio).lower()
                print(f"Command received: {command}")
                move_joint(command)
            except sr.UnknownValueError:
                speak("Sorry, I didn't catch that. Please try again.")
            except Exception as e:
                speak(f"An error occurred: {str(e)}")


# --- GUI ---
def create_gui():
    """Create a simple GUI to monitor and control the robot arm."""
    def emergency_stop_action():
        global emergency_stop
        emergency_stop = True
        speak("Emergency stop activated from GUI.")

    def resume_action():
        global emergency_stop
        emergency_stop = False
        speak("Resuming operations from GUI.")

    def calibrate_action():
        calibrate_arm()

    root = tk.Tk()
    root.title("Robotic Arm Controller")

    tk.Label(root, text="Robotic Arm Status", font=("Arial", 16)).pack(pady=10)

    tk.Button(root, text="Emergency Stop", command=emergency_stop_action, bg="red", fg="white").pack(pady=5)
    tk.Button(root, text="Resume", command=resume_action, bg="green", fg="white").pack(pady=5)
    tk.Button(root, text="Calibrate", command=calibrate_action, bg="blue", fg="white").pack(pady=5)

    root.mainloop()


# --- Main Program ---
if __name__ == "__main__":
    # Start the voice recognition in a separate thread
    voice_thread = threading.Thread(target=listen_for_commands)
    voice_thread.daemon = True
    voice_thread.start()

    # Start the GUI
    create_gui()