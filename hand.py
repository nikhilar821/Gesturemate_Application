import cv2
import mediapipe
import pyautogui
import random
import os
import pyscreeze

# Initialize Hand tracking module
capture_hands = mediapipe.solutions.hands.Hands()
drawing = mediapipe.solutions.drawing_utils

# Get screen dimensions
screen_height, screen_width = pyautogui.size()

window_width = int(screen_width * 1.0)
window_height = int(screen_height * 0.4)

# Open webcam
cam = cv2.VideoCapture(0)

# Initialize variables for hand landmarks
x1 = y1 = x2 = y2 = 0
use_two_fingers = True  # Initially use two fingers (index and thumb)

# Variable to track whether the screenshot has been captured
screenshot_captured = False

#Increase window dimensions to default size
cv2.namedWindow("Hand gesture", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Hand gesture", window_width, window_height)

while True:
    _, img = cam.read()  # Read a frame from the webcam
    img = cv2.flip(img, 1)
    img_height, img_width, _ = img.shape
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Process the image to detect hands
    output_hands = capture_hands.process(rgb_img)
    all_hands = output_hands.multi_hand_landmarks
    
    if all_hands:
        for i, hand in enumerate(all_hands):
            # Generate random color for the hand
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            
            # Draw landmarks on the hand with random color
            drawing.draw_landmarks(img, hand, mediapipe.solutions.hands.HAND_CONNECTIONS, landmark_drawing_spec=drawing.DrawingSpec(color=color, thickness=2, circle_radius=4))
            
            # Get landmarks for one hand
            one_hand_landmarks = hand.landmark
            
            for id, landmark in enumerate(one_hand_landmarks):
                x = int(landmark.x * img_width)
                y = int(landmark.y * img_height)

                if id == 8:
                    # Move mouse cursor to index finger position
                    if use_two_fingers:
                        mouse_x = int(screen_width / img_width * x)
                        mouse_y = int(screen_height / img_height * y)
                        pyautogui.moveTo(mouse_x, mouse_y, duration=0.4) #Reduces cursor speed
                        x1 = x
                        y1 = y
                        cv2.circle(img, (x, y), 10, color, -1)
                    else:
                        # If using single finger (index), hide thumb (ID 4)
                        x2 = -1
                        y2 = -1
                        x1 = x
                        y1 = y
                        mouse_x = int(screen_width / img_width * x)
                        mouse_y = int(screen_height / img_height * y)
                        pyautogui.moveTo(mouse_x, mouse_y)
                        cv2.circle(img, (x, y), 10, color, -1)
                    
                if id == 4 and use_two_fingers:
                    x2 = x
                    y2 = y
                    cv2.circle(img, (x, y), 10, color, -1)
                

        if use_two_fingers:
            dist_y = y2 - y1
        else:
            # When using single finger, consider distance between the finger and the center of the screen
            center_y = screen_height / 2
            dist_y = y1 - center_y
        
        print(dist_y)
        
        # Determine gesture name based on the action being performed
        gesture_name = ""
        if dist_y > 0 and dist_y <= 35:
            gesture_name = "Click"
        elif dist_y <= 0:
            gesture_name = "Scroll Down"
        elif dist_y > 75:
            gesture_name = "Scroll Up"
        elif dist_y > 40 and abs(x2 - x1) <= 55:
            gesture_name = "Drag"

        # Display the gesture name on the screen
        cv2.putText(img, gesture_name, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Perform actions based on gestures

        # Left-click if fingers are close
        if dist_y > 0 and dist_y <= 35:
            pyautogui.click()
        # Scroll up if fingers move down
        elif dist_y <= 0:
            pyautogui.scroll(-53)
        # Scroll down if fingers move up
        elif dist_y > 75:
            pyautogui.scroll(53)
        # Perform drag operation if fingers are close and moving horizontally
        elif dist_y > 40 and abs(x2 - x1) <= 55:
            pyautogui.dragTo(mouse_x + 250, mouse_y, duration=0.5)
        
        # Open the captured screenshot by double-clicking if it has been captured and the double-click gesture is detected
        if screenshot_captured and gesture_name == "Double Click":
            pyautogui.doubleClick(screenshot_path)
    # Disable fail-safe (NOT RECOMMENDED)
    pyautogui.FAILSAFE = False

    # Display the image with hand landmarks and gesture name
    cv2.imshow("Hand gesture", img)
    
    # Wait for a key press
    key = cv2.waitKey(100)
    if key == 27:  # Break the loop when 'Esc' key is pressed
        break
    elif key == ord('s'):  # Toggle between using one and two fingers by pressing 's' key
        use_two_fingers = not use_two_fingers
        
        if not use_two_fingers:
            # Specify the path to save the screenshot
            screenshot_name = "hand_gesture_screenshot.png"  # Specify the desired name for the screenshot
            desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'OneDrive', 'Desktop')  # Get the path to the desktop
            screenshot_path = os.path.join(desktop_path, screenshot_name)  # Specify the path to save the screenshot

            # Capture screenshot using PyAutoGUI
            screenshot = pyautogui.screenshot()
            
            # Save the screenshot
            screenshot.save(screenshot_path)
            
            print(f"Screenshot saved as '{screenshot_name}' on the desktop.")
            
            # Set screenshot_captured flag to True
            screenshot_captured = True
    elif key == ord('d'):  # Perform double click when 'd' key is pressed
        # Simulate double-clicking at the current mouse position
        pyautogui.doubleClick()
        

# Release the webcam and close all windows
cam.release()
cv2.destroyAllWindows()
