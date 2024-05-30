import cv2
import mediapipe as mp
import pyautogui
import time
import subprocess
import psutil
import pygetwindow as gw
import json
import threading

# Define gesture_applications globally
gesture_applications = {}

# Define a flag to control the loop
config_updated = False

# Function to periodically check for updates in gesture configuration
def check_gesture_config():
    global gesture_applications, config_updated  # Declare gesture_applications and config_updated as global
    while True:
        # Read the updated gesture configuration from the file
        with open("gesture_config.json", "r") as f:
            updated_config = json.load(f)
        
        # Check if the updated configuration is different from the current one
        if updated_config != gesture_applications:
            # If yes, update the gesture_applications variable
            gesture_applications = updated_config
            print("Gesture configuration updated:", gesture_applications)
            config_updated = True  # Set the flag to True
            break  # Exit the loop

# Start the gesture configuration update thread
threading.Thread(target=check_gesture_config).start()

# Wait for the configuration update to finish
while not config_updated:
    time.sleep(0.1)  # Sleep for a short duration to avoid busy waiting

# Disable pyautogui fail safe
pyautogui.FAILSAFE = False

# Initialize Mediapipe Hands and Drawing utilities
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Set up camera capture and screen dimensions
camera = cv2.VideoCapture(0)
screen_width, screen_height = pyautogui.size()

# Function to check for left or right hand
def get_hand_orientation(hand_landmarks):
    return 'right' if hand_landmarks.landmark[17].x > hand_landmarks.landmark[5].x else 'left'

# Function to check which fingers are up
def fingers_up(hand_landmarks, hand_orientation):
    fingers = []

    # Thumb: Check if the thumb tip is to the left (right hand) or right (left hand) of the thumb knuckle
    if hand_orientation == 'right':
        fingers.append(1 if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x else 0)
    else:
        fingers.append(0 if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x else 1)

    # Index Finger: Check if the tip is above the PIP joint
    fingers.append(1 if hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y else 0)
    # Middle Finger: Check if the tip is above the PIP joint
    fingers.append(1 if hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y else 0)
    # Ring Finger: Check if the tip is above the PIP joint
    fingers.append(1 if hand_landmarks.landmark[16].y < hand_landmarks.landmark[14].y else 0)
    # Pinky Finger: Check if the tip is above the PIP joint
    fingers.append(1 if hand_landmarks.landmark[20].y < hand_landmarks.landmark[18].y else 0)

    return fingers

def is_process_running(process_name):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == process_name:
            return True
    return False

def bring_notepad_to_front():
    notepad_windows = gw.getWindowsWithTitle("Untitled - Notepad")
    if notepad_windows:
        notepad_window = notepad_windows[0]
        if notepad_window.isMinimized:
            notepad_window.restore()
        notepad_window.activate()

# Initialize the Hands solution
with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.9,
    min_tracking_confidence=0.5) as hands:

    pTime = time.time()
    fps = 0
    fps_update_interval = 1  # update every second
    fps_last_update = time.time()
    sensitivity = 1.5  # Adjusted sensitivity for cursor movement

    # Debounce mechanism
    debounce_interval = 2  # 2 seconds debounce interval
    last_notepad_open_time = 0

    instagram_opened = False

    while True:
        success, image = camera.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue
        
        # Flip the image horizontally for a later selfie-view display
        image = cv2.flip(image, 1)
        image_height, image_width, _ = image.shape
    
        # Convert the BGR image to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
        # Process the image and find hands
        output_hands = hands.process(rgb_image)
        all_hands = output_hands.multi_hand_landmarks
    
        # Calculate and display frame rate
        cTime = time.time()
        if cTime - fps_last_update > fps_update_interval:
            fps = 1 / (cTime - pTime)
            fps_last_update = cTime
        pTime = cTime
        cv2.putText(image, f'FPS: {int(fps)}', (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    
        if all_hands:
            for hand_landmarks in all_hands:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                hand_orientation = get_hand_orientation(hand_landmarks)
                finger_states = fingers_up(hand_landmarks, hand_orientation)
    
                # Move the cursor if only index finger is up 
                if finger_states == [0, 1, 0, 0, 0]:
                    x = int(hand_landmarks.landmark[8].x * image_width)
                    y = int(hand_landmarks.landmark[8].y * image_height)
                    mouse_x = int(screen_width / image_width * x * sensitivity)
                    mouse_y = int(screen_height / image_height * y * sensitivity)
                    pyautogui.moveTo(mouse_x, mouse_y)
    
                # Custom gesture to trigger Instagram (spider-man pose)
                elif finger_states == [1, 1, 0, 0, 1] and hand_orientation == 'right':
                    if not instagram_opened:
                        subprocess.Popen([gesture_applications['Open Instagram'], "instagram.com"])
                        instagram_opened = True
    
                # Notepad gesture
                elif finger_states == [0, 1, 1, 1, 1] and hand_orientation == 'right':
                    if (cTime - last_notepad_open_time) > debounce_interval:
                        if not is_process_running(gesture_applications['Open Notepad']):
                            subprocess.Popen([gesture_applications['Open Notepad']])
                        else:
                            bring_notepad_to_front()
                        last_notepad_open_time = cTime
    
                # Clicking operation
                elif finger_states[1] == 0:  # Index finger is in clicking position
                    distance = hand_landmarks.landmark[4].y - hand_landmarks.landmark[8].y  # Distance between index finger and thumb
                    if distance < 0.02:  # 0.01 is verified limiting distance for the click
                        pyautogui.click()
    
        # Display the resulting image
        cv2.imshow("Hand movement video capture", image)
        
        key = cv2.waitKey(1)
        if key == 27:  # ESC key to break
            break
        
        # Check if Instagram is closed (by checking if the Chrome process is closed)
        if instagram_opened and not any("chrome.exe" in p.name() for p in psutil.process_iter()):
            instagram_opened = False  # Reset the flag if Instagram is closed

# Release the camera and close all OpenCV windows
camera.release()
cv2.destroyAllWindows()
