"""
Invisibility Cloak Project - Harry Potter Style
Using OpenCV to create a real-time invisibility cloak effect
"""

import cv2
import numpy as np
import time

def create_invisibility_cloak():
    """
    Main function to create the invisibility cloak effect
    """
    print("Starting Invisibility Cloak...")
    print("Please move out of the camera view when the countdown starts!")
    
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    
    # Check if camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera")
        return
    
    # Set camera resolution for better performance
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    print("Camera initialized successfully!")
    print("Countdown starting in 3 seconds...")
    time.sleep(3)
    
    print("Capturing background... Please move out of the frame!")
    
    # Capture background frame
    # Let the camera adjust to lighting conditions
    for i in range(60):
        ret, background = cap.read()
        if not ret:
            print("Error: Failed to capture background")
            cap.release()
            return
        
        # Show countdown
        if i % 10 == 0:
            print(f"Capturing background frame {i+1}/60")
    
    print("Background captured successfully!")
    
    # Flip the background for mirror effect
    background = cv2.flip(background, 1)
    
    print("Starting invisibility cloak effect...")
    print("Wear something bright red to become invisible!")
    print("Press 'q' to quit")
    
    # Main processing loop
    while True:
        # Read current frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame")
            break
        
        # Flip frame for mirror effect
        frame = cv2.flip(frame, 1)
        
        # Convert BGR to HSV for better color detection
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Define HSV range for bright red
        # Red color wraps around in HSV, so we need two ranges
        
        # Lower red range (0-10 degrees)
        lower_red1 = np.array([0, 120, 70])
        upper_red1 = np.array([10, 255, 255])
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        
        # Upper red range (170-180 degrees)
        lower_red2 = np.array([170, 120, 70])
        upper_red2 = np.array([180, 255, 255])
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        
        # Combine both masks
        mask = mask1 + mask2
        
        # Refine the mask using morphological operations
        # Remove noise
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        
        # Fill holes and expand the detected regions
        mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel)
        
        # Create inverted mask
        mask_inv = cv2.bitwise_not(mask)
        
        # Segment the image
        # Part of the frame without the cloak
        res1 = cv2.bitwise_and(frame, frame, mask=mask_inv)
        
        # Part of the background that should show through the cloak
        res2 = cv2.bitwise_and(background, background, mask=mask)
        
        # Combine both parts to create the final invisibility effect
        final_output = cv2.add(res1, res2)
        
        # Display the result
        cv2.imshow('Invisibility Cloak', final_output)
        
        # Optional: Show the mask for debugging
        # cv2.imshow('Mask', mask)
        
        # Exit condition
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("Exiting...")
            break
    
    # Clean up
    cap.release()
    cv2.destroyAllWindows()
    print("Invisibility cloak closed successfully!")

def test_camera():
    """
    Test function to check if camera is working properly
    """
    print("Testing camera...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera")
        return False
    
    print("Camera test successful!")
    print("Press 'q' to close test window")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame")
            break
        
        frame = cv2.flip(frame, 1)
        cv2.imshow('Camera Test', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    return True

if __name__ == "__main__":
    print("=== Invisibility Cloak Project ===")
    print("1. Test Camera")
    print("2. Start Invisibility Cloak")
    
    choice = input("Enter your choice (1 or 2): ").strip()
    
    if choice == "1":
        test_camera()
    elif choice == "2":
        create_invisibility_cloak()
    else:
        print("Invalid choice. Starting invisibility cloak by default...")
        create_invisibility_cloak()