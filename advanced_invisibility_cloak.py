"""
Advanced Invisibility Cloak Project
Enhanced version with additional features and better error handling
"""

import cv2
import numpy as np
import time
import argparse
import sys

class InvisibilityCloak:
    def __init__(self, camera_index=0, width=640, height=480):
        """
        Initialize the Invisibility Cloak
        
        Args:
            camera_index (int): Camera index (default: 0)
            width (int): Camera width resolution
            height (int): Camera height resolution
        """
        self.camera_index = camera_index
        self.width = width
        self.height = height
        self.cap = None
        self.background = None
        
        # HSV ranges for red color detection
        self.red_ranges = [
            (np.array([0, 120, 70]), np.array([10, 255, 255])),
            (np.array([170, 120, 70]), np.array([180, 255, 255]))
        ]
        
        # Morphological kernel
        self.kernel = np.ones((3, 3), np.uint8)
        
    def initialize_camera(self):
        """Initialize the camera with error handling"""
        try:
            self.cap = cv2.VideoCapture(self.camera_index)
            
            if not self.cap.isOpened():
                raise Exception(f"Could not open camera at index {self.camera_index}")
            
            # Set camera properties
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            
            # Test frame capture
            ret, frame = self.cap.read()
            if not ret:
                raise Exception("Could not capture test frame")
            
            print(f"Camera initialized successfully!")
            print(f"Resolution: {int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}")
            return True
            
        except Exception as e:
            print(f"Error initializing camera: {e}")
            if self.cap:
                self.cap.release()
            return False
    
    def capture_background(self, frames_to_capture=60, countdown_time=3):
        """
        Capture the background frame
        
        Args:
            frames_to_capture (int): Number of frames to capture for background
            countdown_time (int): Countdown time before capturing
        """
        print(f"Background capture will start in {countdown_time} seconds...")
        print("Please move out of the camera view!")
        
        # Countdown
        for i in range(countdown_time, 0, -1):
            print(f"Starting in {i}...")
            time.sleep(1)
        
        print("Capturing background... Stay out of frame!")
        
        # Capture multiple frames to let camera adjust
        for i in range(frames_to_capture):
            ret, frame = self.cap.read()
            if not ret:
                raise Exception("Failed to capture background frame")
            
            # Show progress
            if i % 10 == 0:
                print(f"Progress: {i+1}/{frames_to_capture}")
            
            # Store the last frame as background
            self.background = cv2.flip(frame, 1)
        
        print("Background captured successfully!")
        return True
    
    def create_red_mask(self, hsv_frame):
        """
        Create a mask for red color detection
        
        Args:
            hsv_frame: Frame in HSV color space
            
        Returns:
            Combined mask for red regions
        """
        masks = []
        
        # Create masks for both red ranges
        for lower, upper in self.red_ranges:
            mask = cv2.inRange(hsv_frame, lower, upper)
            masks.append(mask)
        
        # Combine masks
        combined_mask = cv2.bitwise_or(masks[0], masks[1])
        
        # Refine mask using morphological operations
        # Remove noise
        combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_OPEN, self.kernel)
        
        # Fill holes and expand regions
        combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_DILATE, self.kernel, iterations=2)
        
        # Optional: Gaussian blur for smoother edges
        combined_mask = cv2.medianBlur(combined_mask, 5)
        
        return combined_mask
    
    def apply_invisibility_effect(self, frame, mask):
        """
        Apply the invisibility effect
        
        Args:
            frame: Current frame
            mask: Red color mask
            
        Returns:
            Frame with invisibility effect applied
        """
        # Create inverted mask
        mask_inv = cv2.bitwise_not(mask)
        
        # Segment the image
        # Part without the cloak
        frame_no_cloak = cv2.bitwise_and(frame, frame, mask=mask_inv)
        
        # Background part to show through cloak
        background_cloak = cv2.bitwise_and(self.background, self.background, mask=mask)
        
        # Combine both parts
        final_frame = cv2.add(frame_no_cloak, background_cloak)
        
        return final_frame
    
    def add_info_overlay(self, frame):
        """Add informational overlay to the frame"""
        # Add text overlay
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, "Invisibility Cloak Active", (10, 30), font, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, "Press 'q' to quit, 'r' to recapture background", (10, 60), font, 0.5, (255, 255, 255), 1)
        return frame
    
    def run_invisibility_cloak(self, show_debug=False):
        """
        Main loop for the invisibility cloak effect
        
        Args:
            show_debug (bool): Show debug windows
        """
        if not self.initialize_camera():
            return False
        
        try:
            # Capture background
            self.capture_background()
            
            print("Starting invisibility cloak effect...")
            print("Controls:")
            print("  'q' - Quit")
            print("  'r' - Recapture background")
            print("  's' - Save current frame")
            print("\nWear something bright red to become invisible!")
            
            frame_count = 0
            
            while True:
                # Read frame
                ret, frame = self.cap.read()
                if not ret:
                    print("Failed to capture frame")
                    break
                
                # Flip for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Convert to HSV
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                
                # Create red mask
                mask = self.create_red_mask(hsv)
                
                # Apply invisibility effect
                result = self.apply_invisibility_effect(frame, mask)
                
                # Add info overlay
                result = self.add_info_overlay(result)
                
                # Display result
                cv2.imshow('Invisibility Cloak', result)
                
                # Debug windows
                if show_debug:
                    cv2.imshow('Original', frame)
                    cv2.imshow('Mask', mask)
                    cv2.imshow('Background', self.background)
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q'):
                    print("Quitting...")
                    break
                elif key == ord('r'):
                    print("Recapturing background...")
                    self.capture_background(frames_to_capture=30, countdown_time=2)
                elif key == ord('s'):
                    filename = f"invisibility_frame_{frame_count:04d}.jpg"
                    cv2.imwrite(filename, result)
                    print(f"Frame saved as {filename}")
                
                frame_count += 1
            
            return True
            
        except KeyboardInterrupt:
            print("\nInterrupted by user")
            return True
        except Exception as e:
            print(f"Error during execution: {e}")
            return False
        finally:
            self.cleanup()
    
    def test_camera(self):
        """Test camera functionality"""
        if not self.initialize_camera():
            return False
        
        print("Camera test mode - Press 'q' to exit")
        
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    print("Failed to capture frame")
                    break
                
                frame = cv2.flip(frame, 1)
                
                # Add test overlay
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, "Camera Test Mode", (10, 30), font, 1, (0, 255, 0), 2)
                cv2.putText(frame, "Press 'q' to exit", (10, 70), font, 0.7, (255, 255, 255), 2)
                
                cv2.imshow('Camera Test', frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            print("Camera test completed successfully!")
            return True
            
        except Exception as e:
            print(f"Camera test failed: {e}")
            return False
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        print("Resources cleaned up successfully")

def main():
    """Main function with command line argument parsing"""
    parser = argparse.ArgumentParser(description='Invisibility Cloak using OpenCV')
    parser.add_argument('--camera', type=int, default=0, help='Camera index (default: 0)')
    parser.add_argument('--width', type=int, default=640, help='Camera width (default: 640)')
    parser.add_argument('--height', type=int, default=480, help='Camera height (default: 480)')
    parser.add_argument('--test', action='store_true', help='Run camera test only')
    parser.add_argument('--debug', action='store_true', help='Show debug windows')
    
    args = parser.parse_args()
    
    # Create invisibility cloak instance
    cloak = InvisibilityCloak(
        camera_index=args.camera,
        width=args.width,
        height=args.height
    )
    
    print("=== Advanced Invisibility Cloak ===")
    
    if args.test:
        print("Running camera test...")
        success = cloak.test_camera()
    else:
        print("Starting invisibility cloak...")
        success = cloak.run_invisibility_cloak(show_debug=args.debug)
    
    if success:
        print("Application completed successfully!")
    else:
        print("Application encountered errors!")
        sys.exit(1)

if __name__ == "__main__":
    main()