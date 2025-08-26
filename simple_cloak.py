#!/usr/bin/env python3
"""
Simple Command-Line Version of Harry Potter Invisibility Cloak
A lightweight version for quick testing and demonstrations.
"""

import cv2
import numpy as np
import time

def create_invisibility_cloak():
    """Main function for the invisibility cloak effect"""
    
    # Initialize camera
    print("🪄 Starting Harry Potter Invisibility Cloak...")
    print("Press 'b' to capture background")
    print("Press 'q' to quit")
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Error: Could not open camera!")
        return
    
    # Variables
    background = None
    
    # HSV range for red color (cloak)
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])
    
    # Morphological operations kernel
    kernel = np.ones((3, 3), np.uint8)
    
    print("📸 Camera started! Press 'b' when ready to capture background...")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Flip frame horizontally for mirror effect
        frame = np.flip(frame, axis=1)
        
        key = cv2.waitKey(1) & 0xFF
        
        # Capture background
        if key == ord('b'):
            background = frame.copy()
            print("✅ Background captured! Put on your red cloak now...")
            time.sleep(2)
            continue
        
        # Quit
        if key == ord('q'):
            break
        
        # Apply invisibility cloak if background is captured
        if background is not None:
            # Convert to HSV
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # Create mask for red color
            mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
            mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
            mask = mask1 + mask2
            
            # Clean up the mask
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel)
            
            # Blur for smoother edges
            mask = cv2.GaussianBlur(mask, (5, 5), 0)
            
            # Create result
            mask_inv = cv2.bitwise_not(mask)
            
            # Convert masks for blending
            mask_3d = np.dstack([mask/255.0] * 3)
            mask_inv_3d = np.dstack([mask_inv/255.0] * 3)
            
            # Apply invisibility effect
            result = (mask_3d * background + mask_inv_3d * frame).astype(np.uint8)
            
            cv2.imshow('Harry Potter Invisibility Cloak - Magic Mode ✨', result)
            
        else:
            # Show normal video while waiting for background capture
            cv2.putText(frame, "Press 'b' to capture background", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.imshow('Harry Potter Invisibility Cloak - Setup Mode', frame)
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    print("🎬 Magic session ended. Thanks for using the Invisibility Cloak!")

if __name__ == "__main__":
    create_invisibility_cloak()
