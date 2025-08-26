#!/usr/bin/env python3
"""
Color Calibration Tool for Invisibility Cloak
Use this tool to find the perfect HSV values for your cloak color and lighting conditions.
"""

import cv2
import numpy as np

def nothing(x):
    """Dummy function for trackbar callbacks"""
    pass

def color_calibrator():
    """Interactive color calibration tool"""
    
    print("🎨 Color Calibration Tool for Invisibility Cloak")
    print("Use trackbars to adjust HSV values for perfect color detection")
    print("Press 'q' to quit and save values")
    
    # Initialize camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Error: Could not open camera!")
        return
    
    # Create window and trackbars
    cv2.namedWindow('Color Calibration Tool')
    cv2.namedWindow('Mask Preview')
    cv2.namedWindow('HSV Controls')
    
    # Create trackbars for HSV values
    cv2.createTrackbar('Lower H', 'HSV Controls', 0, 179, nothing)
    cv2.createTrackbar('Lower S', 'HSV Controls', 120, 255, nothing)
    cv2.createTrackbar('Lower V', 'HSV Controls', 70, 255, nothing)
    cv2.createTrackbar('Upper H', 'HSV Controls', 10, 179, nothing)
    cv2.createTrackbar('Upper S', 'HSV Controls', 255, 255, nothing)
    cv2.createTrackbar('Upper V', 'HSV Controls', 255, 255, nothing)
    
    # For second red range
    cv2.createTrackbar('Lower H2', 'HSV Controls', 170, 179, nothing)
    cv2.createTrackbar('Upper H2', 'HSV Controls', 180, 179, nothing)
    
    print("📸 Camera started! Adjust trackbars to detect your cloak color...")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Flip frame for mirror effect
        frame = np.flip(frame, axis=1)
        
        # Get trackbar values
        lower_h = cv2.getTrackbarPos('Lower H', 'HSV Controls')
        lower_s = cv2.getTrackbarPos('Lower S', 'HSV Controls')
        lower_v = cv2.getTrackbarPos('Lower V', 'HSV Controls')
        upper_h = cv2.getTrackbarPos('Upper H', 'HSV Controls')
        upper_s = cv2.getTrackbarPos('Upper S', 'HSV Controls')
        upper_v = cv2.getTrackbarPos('Upper V', 'HSV Controls')
        
        lower_h2 = cv2.getTrackbarPos('Lower H2', 'HSV Controls')
        upper_h2 = cv2.getTrackbarPos('Upper H2', 'HSV Controls')
        
        # Convert to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Create masks
        lower_range1 = np.array([lower_h, lower_s, lower_v])
        upper_range1 = np.array([upper_h, upper_s, upper_v])
        lower_range2 = np.array([lower_h2, lower_s, lower_v])
        upper_range2 = np.array([upper_h2, upper_s, upper_v])
        
        mask1 = cv2.inRange(hsv, lower_range1, upper_range1)
        mask2 = cv2.inRange(hsv, lower_range2, upper_range2)
        mask = mask1 + mask2
        
        # Apply morphological operations
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel)
        
        # Create result for visualization
        result = cv2.bitwise_and(frame, frame, mask=mask)
        
        # Display current HSV values on frame
        text_y = 30
        cv2.putText(frame, f"Lower HSV: [{lower_h}, {lower_s}, {lower_v}]", 
                   (10, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        text_y += 25
        cv2.putText(frame, f"Upper HSV: [{upper_h}, {upper_s}, {upper_v}]", 
                   (10, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        text_y += 25
        cv2.putText(frame, f"Red Range 2: [{lower_h2}-{upper_h2}]", 
                   (10, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        text_y += 35
        cv2.putText(frame, "Adjust trackbars for better detection", 
                   (10, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Show windows
        cv2.imshow('Color Calibration Tool', frame)
        cv2.imshow('Mask Preview', mask)
        
        # Check for quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("\n✅ Final HSV Values:")
            print(f"Lower Red Range 1: [{lower_h}, {lower_s}, {lower_v}]")
            print(f"Upper Red Range 1: [{upper_h}, {upper_s}, {upper_v}]")
            print(f"Lower Red Range 2: [{lower_h2}, {lower_s}, {lower_v}]")
            print(f"Upper Red Range 2: [{upper_h2}, {upper_s}, {upper_v}]")
            print("\nCopy these values to your main invisibility cloak program!")
            break
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    color_calibrator()
