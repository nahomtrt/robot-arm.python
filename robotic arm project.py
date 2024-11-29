import pyttsx3
import speech_recognition as sr
from gpiozero import Servo
from time import sleep

engine = pyttsx3.init()

engine.setProperty('rate', 150)  
engine.setProperty('volume', 1.0)  

servo_base = Servo(17)  
servo_shoulder = Servo(18)  
servo_gripper = Servo(27)  

def speak(text):
    engine.say(text)
    engine.runAndWait()

def move_base_left():
    speak("Turning the base to the left.")
    print("Moving base left...")
    servo_base.max()
    sleep(1)
    servo_base.mid()
    speak("Base moved to the left.")

def move_base_right():
    speak("Turning the base to the right.")
    print("Moving base right...")
    servo_base.min()
    sleep(1)
    servo_base.mid()
    speak("Base moved to the right.")

def lift_arm():
    speak("Lifting the arm.")
    print("Lifting arm...")
    servo_shoulder.max()
    sleep(1)
    servo_shoulder.mid()
    speak("The arm has been lifted.")

def lower_arm():
    speak("Lowering the arm.")
    print("Lowering arm...")
    servo_shoulder.min()
    sleep(1)
    servo_shoulder.mid()
    speak("The arm has been lowered.")

def open_gripper():
    speak("Opening the gripper.")
    print("Opening gripper...")
    servo_gripper.min()
    sleep(1)
    servo_gripper.mid()
    speak("Gripper is now open.")

def close_gripper():
    speak("Closing the gripper.")
    print("Closing gripper...")
    servo_gripper.max()
    sleep(1)
    servo_gripper.mid()
    speak("Gripper is now closed.")

# Voice recognition setup
recognizer = sr.Recognizer()

def listen_for_command():
    with sr.Microphone() as source:
        speak("Listening for your command.")
        print("Listening...")
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Please repeat.")
            return None

# Main loop to handle commands
def main():
    speak("Robot arm is ready for commands.")
    while True:
        command = listen_for_command()
        if command:
            if "move base left" in command:
                move_base_left()
            elif "move base right" in command:
                move_base_right()
            elif "lift arm" in command:
                lift_arm()
            elif "lower arm" in command:
                lower_arm()
            elif "open gripper" in command:
                open_gripper()
            elif "close gripper" in command:
                close_gripper()
            elif "stop" in command:
                speak("Stopping all operations. Goodbye!")
                break
            else:
                speak("Sorry, I didn't understand that command. Please try again.")

# Run the program
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        speak("Shutting down the robot arm. Goodbye!")
