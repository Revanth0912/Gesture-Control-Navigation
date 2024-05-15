# importing dependencies
import cv2
import mediapipe as mp
import pyautogui
import time

# Disable pyautogui fail safe
pyautogui.FAILSAFE = False

# Initialize Mediapipe Hands and Drawing utilities
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Set up camera capture and screen dimensions
camera = cv2.VideoCapture(0)
screen_width, screen_height = pyautogui.size()

# Initialize the Hands solution
with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

    # Initializing variables
    sensitivity = 2
    pTime = 0
    fps = 0
    fps_update_interval = 1  # update every second
    fps_last_update = time.time()

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
                one_hand_landmarks = hand_landmarks.landmark

                '''for id, lm in enumerate(one_hand_landmarks):
                    x = int(lm.x * image_width)
                    y = int(lm.y * image_height)

                    if id == 9 or id == 0:
                        mouse_x = int(screen_width / image_width * x) * sensitivity
                        mouse_y = int(screen_height / image_height * y) * sensitivity
                        cv2.circle(image, (x, y), 5, (255, 0, 0), -1)
                        pyautogui.moveTo(mouse_x, mouse_y)
                        x1, y1 = x, y

                    if id == 12 or id == 4:
                        x2, y2 = x, y
                        cv2.circle(image, (x, y), 5, (255, 0, 0), -1)'''

                '''dist = y1 - y2
                print(dist)
                if dist < 24.9:
                    if x2 < x1:
                        pyautogui.press('left')
                    else:
                        pyautogui.press('right')
                if dist < -13:
                    pyautogui.click()'''

        # Display the resulting image
        cv2.imshow("Hand movement video capture", image)
        key = cv2.waitKey(1)
        if key == 27:  # ESC key to break
            break

# Release the camera and close all OpenCV windows
camera.release()
cv2.destroyAllWindows()
