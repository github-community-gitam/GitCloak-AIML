"""
Color Detection Demo for Invisibility Cloak
Demonstrates different color detection options
"""

import cv2
import numpy as np
import time

class ColorDetectionDemo:
    def __init__(self):
        self.cap = None
        self.colors = {
            'red': {
                'ranges': [
                    (np.array([0, 120, 70]), np.array([10, 255, 255])),
                    (np.array([170, 120, 70]), np.array([180, 255, 255]))
                ],
                'color': (0, 0, 255)
            },
            'blue': {
                'ranges': [
                    (np.array([100, 150, 50]), np.array([130, 255, 255]))
                ],
                'color': (255, 0, 0)
            },
            'green': {
                'ranges': [
                    (np.array([40, 50, 50]), np.array([80, 255, 255]))
                ],
                'color': (0, 255, 0)
            },
            'yellow': {
                'ranges': [
                    (np.array([20, 100, 100]), np.array([30, 255, 255]))
                ],
                'color': (0, 255, 255)
            },
            'purple': {
                'ranges': [
                    (np.array([130, 50, 50]), np.array([160, 255, 255]))
                ],
                'color': (128, 0, 128)
            }
        }
        self.current_color = 'red'
        
    def initialize_camera(self):
        """Initialize camera"""
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            return False
        
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        return True
    
    def create_color_mask(self, hsv_frame, color_name):
        """Create mask for specified color"""
        color_info = self.colors[color_name]
        masks = []
        
        for lower, upper in color_info['ranges']:
            mask = cv2.inRange(hsv_frame, lower, upper)
            masks.append(mask)
        
        # Combine masks
        if len(masks) == 1:
            combined_mask = masks[0]
        else:
            combined_mask = masks[0]
            for mask in masks[1:]:
                combined_mask = cv2.bitwise_or(combined_mask, mask)
        
        # Clean up mask
        kernel = np.ones((3, 3), np.uint8)
        combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_OPEN, kernel)
        combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_DILATE, kernel, iterations=2)
        
        return combined_mask
    
    def add_color_overlay(self, frame, mask, color_name):
        """Add colored overlay to detected regions"""
        color_info = self.colors[color_name]
        overlay = frame.copy()
        
        # Create colored overlay
        overlay[mask > 0] = color_info['color']
        
        # Blend with original frame
        result = cv2.addWeighted(frame, 0.7, overlay, 0.3, 0)
        
        return result
    
    def run_demo(self):
        """Run the color detection demo"""
        if not self.initialize_camera():
            print("Failed to initialize camera")
            return
        
        print("Color Detection Demo")
        print("Controls:")
        print("  '1' - Red detection")
        print("  '2' - Blue detection") 
        print("  '3' - Green detection")
        print("  '4' - Yellow detection")
        print("  '5' - Purple detection")
        print("  'q' - Quit")
        
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    break
                
                frame = cv2.flip(frame, 1)
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                
                # Create mask for current color
                mask = self.create_color_mask(hsv, self.current_color)
                
                # Add overlay
                result = self.add_color_overlay(frame, mask, self.current_color)
                
                # Add text information
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(result, f"Detecting: {self.current_color.upper()}", 
                           (10, 30), font, 1, (255, 255, 255), 2)
                cv2.putText(result, "Press 1-5 to change color, 'q' to quit", 
                           (10, 60), font, 0.6, (255, 255, 255), 1)
                
                # Show HSV ranges
                color_info = self.colors[self.current_color]
                y_pos = 90
                for i, (lower, upper) in enumerate(color_info['ranges']):
                    range_text = f"Range {i+1}: H({lower[0]}-{upper[0]}) S({lower[1]}-{upper[1]}) V({lower[2]}-{upper[2]})"
                    cv2.putText(result, range_text, (10, y_pos), font, 0.4, (200, 200, 200), 1)
                    y_pos += 20
                
                # Display windows
                cv2.imshow('Color Detection Demo', result)
                cv2.imshow('Mask', mask)
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q'):
                    break
                elif key == ord('1'):
                    self.current_color = 'red'
                    print("Switched to RED detection")
                elif key == ord('2'):
                    self.current_color = 'blue'
                    print("Switched to BLUE detection")
                elif key == ord('3'):
                    self.current_color = 'green'
                    print("Switched to GREEN detection")
                elif key == ord('4'):
                    self.current_color = 'yellow'
                    print("Switched to YELLOW detection")
                elif key == ord('5'):
                    self.current_color = 'purple'
                    print("Switched to PURPLE detection")
        
        finally:
            self.cap.release()
            cv2.destroyAllWindows()

def hsv_color_picker():
    """Interactive HSV color picker"""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        return
    
    def nothing(x):
        pass
    
    # Create trackbars
    cv2.namedWindow('HSV Color Picker')
    cv2.createTrackbar('H Min', 'HSV Color Picker', 0, 179, nothing)
    cv2.createTrackbar('S Min', 'HSV Color Picker', 0, 255, nothing)
    cv2.createTrackbar('V Min', 'HSV Color Picker', 0, 255, nothing)
    cv2.createTrackbar('H Max', 'HSV Color Picker', 179, 179, nothing)
    cv2.createTrackbar('S Max', 'HSV Color Picker', 255, 255, nothing)
    cv2.createTrackbar('V Max', 'HSV Color Picker', 255, 255, nothing)
    
    print("HSV Color Picker")
    print("Adjust trackbars to find the right HSV range for your color")
    print("Press 'q' to quit")
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # Get trackbar values
            h_min = cv2.getTrackbarPos('H Min', 'HSV Color Picker')
            s_min = cv2.getTrackbarPos('S Min', 'HSV Color Picker')
            v_min = cv2.getTrackbarPos('V Min', 'HSV Color Picker')
            h_max = cv2.getTrackbarPos('H Max', 'HSV Color Picker')
            s_max = cv2.getTrackbarPos('S Max', 'HSV Color Picker')
            v_max = cv2.getTrackbarPos('V Max', 'HSV Color Picker')
            
            # Create mask
            lower = np.array([h_min, s_min, v_min])
            upper = np.array([h_max, s_max, v_max])
            mask = cv2.inRange(hsv, lower, upper)
            
            # Apply mask
            result = cv2.bitwise_and(frame, frame, mask=mask)
            
            # Add range text
            font = cv2.FONT_HERSHEY_SIMPLEX
            range_text = f"Range: H({h_min}-{h_max}) S({s_min}-{s_max}) V({v_min}-{v_max})"
            cv2.putText(frame, range_text, (10, 30), font, 0.6, (255, 255, 255), 2)
            
            # Show windows
            cv2.imshow('Original', frame)
            cv2.imshow('Mask', mask)
            cv2.imshow('Result', result)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    finally:
        cap.release()
        cv2.destroyAllWindows()

def main():
    """Main function"""
    print("=== Color Detection Tools ===")
    print("1. Color Detection Demo")
    print("2. HSV Color Picker")
    
    choice = input("Enter your choice (1 or 2): ").strip()
    
    if choice == "1":
        demo = ColorDetectionDemo()
        demo.run_demo()
    elif choice == "2":
        hsv_color_picker()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()