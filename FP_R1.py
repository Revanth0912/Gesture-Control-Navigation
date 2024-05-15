import cv2
import mediapipe
import pyautogui
pyautogui.FAILSAFE = False
capture_hands = mediapipe.solutions.hands.Hands()
drawing_option = mediapipe.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
camera = cv2.VideoCapture(0)
x1 = y1 = x2 = y2 =0
while True:
    _,image = camera.read()
    image_height, image_width, _ = image.shape
    image = cv2.flip(image,1)
    rgb_image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    output_hands =  capture_hands.process(rgb_image)
    all_hands = output_hands.multi_hand_landmarks
    if all_hands:
        for hand in all_hands:
            drawing_option.draw_landmarks(image,hand)
            one_hand_landmarks =  hand.landmark
            for id, lm in enumerate(one_hand_landmarks):
                x = int(lm.x * image_width)
                y = int(lm.y * image_height)
                #print(x,y)
                if id == 8:
                    mouse_x = int(screen_width / image_width * x) * 1.5     
                    mouse_y = int(screen_height / image_height * y) *1.5                
                    cv2.circle(image,(x,y),5,(255,0,0))
                    #pyautogui.moveTo(mouse_x,mouse_y)
                    x1 = x
                    y1 = y
                if id == 4:
                    x2= x
                    y2 = y
                    cv2.circle(image,(x,y),5,(255,0,0))
        dist = y2 - y1
        print(dist)
        if(dist<15):
             if x2 < x1:  # Left hand (thumb to the left of index finger)
                pyautogui.press('left')
             else:  # Right hand (thumb to the right of index finger)
                pyautogui.press('right')
    cv2.imshow("Hand movement video capture",image)
    key = cv2.waitKey(100)
    if key == 27:
        break
camera.release()
cv2.destroyAllWindows()