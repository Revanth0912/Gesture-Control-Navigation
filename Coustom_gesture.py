import cv2
import mediapipe as mp
import pyautogui
import time
import subprocess
import psutil

# Disable pyautogui fail safe
pyautogui.FAILSAFE = False

# Initialize Mediapipe Hands and Drawing utilities
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Set up camera capture and screen dimensions
camera = cv2.VideoCapture(0)
screen_width, screen_height = pyautogui.size()

hand_orientation = 'right' #setting default hand orientation is right(it will be modified in the 1st iteration)

# Function to check which fingers are up
def fingers_up(hand_landmarks):#defines the oreintation of hand
    fingers = []
    
    # Check for left or right hand
    global hand_orientation
    if hand_landmarks.landmark[17].x > hand_landmarks.landmark[5].x:
        hand_orientation = 'right' # for right hand
    else:
        hand_orientation = 'left' # for left hand

    # Thumb: Check if the thumb tip is to the left (right hand) or right (left hand) of the thumb knuckle
    if hand_orientation == 'right':
        if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x: 
            fingers.append(1)
        else:
            fingers.append(0)
    else:
        if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x: 
            fingers.append(0)
        else:
            fingers.append(1)

    # Index Finger: Check if the tip is above the PIP joint
    if hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y:
        fingers.append(1)
    else:
        fingers.append(0)
    
    # Middle Finger: Check if the tip is above the PIP joint
    if hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y:
        fingers.append(1)
    else:
        fingers.append(0)
    
    # Ring Finger: Check if the tip is above the PIP joint
    if hand_landmarks.landmark[16].y < hand_landmarks.landmark[14].y:
        fingers.append(1)
    else:
        fingers.append(0)
    
    # Pinky Finger: Check if the tip is above the PIP joint
    if hand_landmarks.landmark[20].y < hand_landmarks.landmark[18].y:
        fingers.append(1)
    else:
        fingers.append(0)
    
    return fingers

# Flag to track if Notepad is already open
notepad_opened = False

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
                finger_states = fingers_up(hand_landmarks)
                #print(f'Finger states: {finger_states}')  # Print the array indicating which fingers are up

                # Move the cursor if only index finger is up 
                if finger_states[0] == 0 and finger_states[1] == 1 and finger_states[2] == 0 and finger_states[3] == 0 and finger_states[4] == 0:
                    x = int(hand_landmarks.landmark[8].x * image_width)
                    y = int(hand_landmarks.landmark[8].y * image_height)
                    mouse_x = int(screen_width / image_width * x) * sensitivity
                    mouse_y = int(screen_height / image_height * y) * sensitivity
                    pyautogui.moveTo(mouse_x, mouse_y)
                #costum gesture to trigger instagram(spider-man pose)   
                elif finger_states[0]==1 and finger_states[1] == 1 and finger_states[2] == 0 and finger_states[3] == 0 and finger_states[4] == 1 and hand_orientation=='right':
                        if not notepad_opened:  # Check if Notepad is not already open
                            subprocess.Popen(["C:\Program Files\Google\Chrome\Application\chrome.exe","instagram.com"])
                            notepad_opened = True  # Set the flag to indicate that Notepad is open
                #notepad gesture
                elif finger_states[0]==1 and finger_states[1] == 0 and finger_states[2] == 0 and finger_states[3] == 0 and finger_states[4] == 0 and hand_orientation=='right':
                        if not notepad_opened:  # Check if Notepad is not already open
                            subprocess.Popen(["notepad"])
                            notepad_opened = True  # Set the flag to indicate that Notepad is open            
                else:
                    #clicking operation
                    if finger_states[1]==0:    #index finger is clicking position
                        distance = hand_landmarks.landmark[4].y - hand_landmarks.landmark[8].y #distance between index finger and thumb finger
                        #print(distance)
                        if distance < 0.02 : #0.01 is verified limiting distance for the click
                            pyautogui.click()
                        


        # Display the resulting image
        cv2.imshow("Hand movement video capture", image)
        key = cv2.waitKey(1)
        if key == 27:  # ESC key to break
            break

        # Check if Notepad window is closed
        if notepad_opened and not any("notepad.exe" in p.name() for p in psutil.process_iter()):
            notepad_opened = False  # Reset the flag if Notepad is closed

# Release the camera and close all OpenCV windows
camera.release()
cv2.destroyAllWindows()
