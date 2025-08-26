#!/usr/bin/env python3
"""
Harry Potter Full Body Invisibility Cloak - Enhanced GUI Version
Complete invisibility using person detection + color detection for full body coverage.
"""

import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import threading
import time

class FullInvisibilityCloakGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Harry Potter Full Body Invisibility Cloak")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2c3e50')
        
        # Video capture variables
        self.cap = None
        self.background = None
        self.running = False
        self.thread = None
        
        # Detection mode: 'color', 'person', or 'hybrid'
        self.detection_mode = tk.StringVar(value='hybrid')
        
        # HSV color range for blue cloak (default values)
        self.lower_blue1 = np.array([100, 50, 50])
        self.upper_blue1 = np.array([130, 255, 255])
        self.lower_blue2 = np.array([100, 50, 50])
        self.upper_blue2 = np.array([130, 255, 255])
        
        # Morphological operations kernel
        self.kernel = np.ones((5, 5), np.uint8)  # Larger kernel for better coverage
        
        # Background subtractor for motion detection
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(detectShadows=False)
        
        # Person detection using contour area threshold
        self.min_person_area = 5000  # Minimum area to consider as person
        self.max_person_area = 100000  # Maximum area to consider as person
        
        # Expansion parameters for full body coverage
        self.expansion_factor = 1.5  # How much to expand the detected region
        self.blur_kernel_size = 15   # Larger blur for smoother edges
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the enhanced GUI interface"""
        # Title
        title_frame = tk.Frame(self.root, bg='#2c3e50')
        title_frame.pack(fill='x', padx=10, pady=10)
        
        title_label = tk.Label(
            title_frame,
            text="🪄 Harry Potter Full Body Invisibility Cloak 🪄",
            font=('Arial', 22, 'bold'),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Complete invisibility with advanced person detection!",
            font=('Arial', 12),
            fg='#bdc3c7',
            bg='#2c3e50'
        )
        subtitle_label.pack()
        
        # Main content frame
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Left panel for video
        video_frame = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=2)
        video_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        video_label = tk.Label(
            video_frame,
            text="Full Body Magic Feed",
            font=('Arial', 14, 'bold'),
            fg='#ecf0f1',
            bg='#34495e'
        )
        video_label.pack(pady=5)
        
        self.video_display = tk.Label(video_frame, bg='black')
        self.video_display.pack(padx=10, pady=10)
        
        # Right panel for controls
        control_frame = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=2, width=320)
        control_frame.pack(side='right', fill='y', padx=(5, 0))
        control_frame.pack_propagate(False)
        
        control_label = tk.Label(
            control_frame,
            text="Enhanced Controls",
            font=('Arial', 14, 'bold'),
            fg='#ecf0f1',
            bg='#34495e'
        )
        control_label.pack(pady=10)
        
        # Detection Mode Selection
        mode_frame = tk.LabelFrame(
            control_frame,
            text="Detection Mode",
            font=('Arial', 12, 'bold'),
            fg='#ecf0f1',
            bg='#34495e'
        )
        mode_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Radiobutton(
            mode_frame,
            text="🎯 Hybrid (Best)",
            variable=self.detection_mode,
            value='hybrid',
            fg='#ecf0f1',
            bg='#34495e',
            selectcolor='#2c3e50',
            font=('Arial', 10)
        ).pack(anchor='w', padx=5)
        
        tk.Radiobutton(
            mode_frame,
            text="👤 Person Detection",
            variable=self.detection_mode,
            value='person',
            fg='#ecf0f1',
            bg='#34495e',
            selectcolor='#2c3e50',
            font=('Arial', 10)
        ).pack(anchor='w', padx=5)
        
        tk.Radiobutton(
            mode_frame,
            text="🎨 Color Only",
            variable=self.detection_mode,
            value='color',
            fg='#ecf0f1',
            bg='#34495e',
            selectcolor='#2c3e50',
            font=('Arial', 10)
        ).pack(anchor='w', padx=5)
        
        # Control buttons
        button_frame = tk.Frame(control_frame, bg='#34495e')
        button_frame.pack(fill='x', padx=10, pady=5)
        
        self.start_btn = tk.Button(
            button_frame,
            text="🎬 Start Full Magic",
            command=self.start_camera,
            font=('Arial', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='raised',
            bd=2
        )
        self.start_btn.pack(fill='x', pady=2)
        
        self.capture_bg_btn = tk.Button(
            button_frame,
            text="📸 Capture Background",
            command=self.capture_background,
            font=('Arial', 12, 'bold'),
            bg='#3498db',
            fg='white',
            relief='raised',
            bd=2,
            state='disabled'
        )
        self.capture_bg_btn.pack(fill='x', pady=2)
        
        self.stop_btn = tk.Button(
            button_frame,
            text="⏹️ Stop Magic",
            command=self.stop_camera,
            font=('Arial', 12, 'bold'),
            bg='#e74c3c',
            fg='white',
            relief='raised',
            bd=2,
            state='disabled'
        )
        self.stop_btn.pack(fill='x', pady=2)
        
        # Advanced Settings
        advanced_frame = tk.LabelFrame(
            control_frame,
            text="Advanced Settings",
            font=('Arial', 12, 'bold'),
            fg='#ecf0f1',
            bg='#34495e'
        )
        advanced_frame.pack(fill='x', padx=10, pady=10)
        
        # Expansion Factor
        tk.Label(advanced_frame, text="Body Coverage:", fg='#ecf0f1', bg='#34495e').pack(anchor='w')
        self.expansion_scale = tk.Scale(
            advanced_frame,
            from_=1.0,
            to=3.0,
            resolution=0.1,
            orient='horizontal',
            bg='#2c3e50',
            fg='#ecf0f1',
            highlightbackground='#34495e',
            troughcolor='#2c3e50'
        )
        self.expansion_scale.set(self.expansion_factor)
        self.expansion_scale.pack(fill='x', padx=5)
        
        # Blur Amount
        tk.Label(advanced_frame, text="Edge Smoothness:", fg='#ecf0f1', bg='#34495e').pack(anchor='w')
        self.blur_scale = tk.Scale(
            advanced_frame,
            from_=5,
            to=31,
            resolution=2,
            orient='horizontal',
            bg='#2c3e50',
            fg='#ecf0f1',
            highlightbackground='#34495e',
            troughcolor='#2c3e50'
        )
        self.blur_scale.set(self.blur_kernel_size)
        self.blur_scale.pack(fill='x', padx=5)
        
        # HSV Controls (simplified)
        hsv_frame = tk.LabelFrame(
            control_frame,
            text="Blue Detection (if needed)",
            font=('Arial', 10, 'bold'),
            fg='#ecf0f1',
            bg='#34495e'
        )
        hsv_frame.pack(fill='x', padx=10, pady=5)
        
        self.lower_h1_scale = self.create_scale(hsv_frame, "H", 0, 179, self.lower_blue1[0])
        self.lower_s1_scale = self.create_scale(hsv_frame, "S", 0, 255, self.lower_blue1[1])
        self.lower_v1_scale = self.create_scale(hsv_frame, "V", 0, 255, self.lower_blue1[2])
        
        # Status frame
        status_frame = tk.Frame(control_frame, bg='#34495e')
        status_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(
            status_frame,
            text="Status:",
            font=('Arial', 12, 'bold'),
            fg='#ecf0f1',
            bg='#34495e'
        ).pack(anchor='w')
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready for full body magic",
            font=('Arial', 10),
            fg='#f39c12',
            bg='#34495e'
        )
        self.status_label.pack(anchor='w')
        
        # Enhanced Instructions
        instructions_frame = tk.LabelFrame(
            control_frame,
            text="Full Body Magic Instructions",
            font=('Arial', 10, 'bold'),
            fg='#ecf0f1',
            bg='#34495e'
        )
        instructions_frame.pack(fill='x', padx=10, pady=5)
        
        instructions = [
            "1. Click 'Start Full Magic'",
            "2. Stand still for 3 seconds",
            "3. Click 'Capture Background'",
            "4. Move away completely",
            "5. Come back with blue cloth",
            "6. Enjoy FULL invisibility! ✨"
        ]
        
        for instruction in instructions:
            tk.Label(
                instructions_frame,
                text=instruction,
                font=('Arial', 8),
                fg='#bdc3c7',
                bg='#34495e',
                anchor='w'
            ).pack(fill='x', padx=5, pady=1)
    
    def create_scale(self, parent, label, from_val, to_val, initial_val):
        """Create a compact labeled scale widget"""
        frame = tk.Frame(parent, bg='#34495e')
        frame.pack(fill='x', pady=1)
        
        tk.Label(frame, text=f"{label}:", fg='#ecf0f1', bg='#34495e', width=2).pack(side='left')
        
        scale = tk.Scale(
            frame,
            from_=from_val,
            to=to_val,
            orient='horizontal',
            bg='#2c3e50',
            fg='#ecf0f1',
            highlightbackground='#34495e',
            troughcolor='#2c3e50',
            font=('Arial', 8)
        )
        scale.set(initial_val)
        scale.pack(side='left', fill='x', expand=True)
        
        return scale
    
    def start_camera(self):
        """Start the camera and video processing"""
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                messagebox.showerror("Error", "Could not open camera!")
                return
            
            self.running = True
            self.start_btn.config(state='disabled')
            self.capture_bg_btn.config(state='normal')
            self.stop_btn.config(state='normal')
            self.status_label.config(text="Camera started - Stand still and capture background", fg='#27ae60')
            
            # Start video processing thread
            self.thread = threading.Thread(target=self.process_video)
            self.thread.daemon = True
            self.thread.start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start camera: {str(e)}")
    
    def capture_background(self):
        """Capture the background frame and initialize background subtractor"""
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                self.background = np.flip(frame, axis=1).copy()
                
                # Reset and train background subtractor
                self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(detectShadows=False)
                
                # Feed several frames to the background subtractor for training
                for _ in range(30):
                    ret, train_frame = self.cap.read()
                    if ret:
                        train_frame = np.flip(train_frame, axis=1)
                        self.bg_subtractor.apply(train_frame)
                
                self.status_label.config(text="Background captured - Full body magic ready!", fg='#3498db')
                messagebox.showinfo("Background Captured", 
                                  "Background captured successfully!\nNow put on your blue cloth and experience FULL BODY invisibility!")
    
    def stop_camera(self):
        """Stop the camera and video processing"""
        self.running = False
        if self.cap:
            self.cap.release()
            self.cap = None
        
        self.start_btn.config(state='normal')
        self.capture_bg_btn.config(state='disabled')
        self.stop_btn.config(state='disabled')
        self.status_label.config(text="Camera stopped", fg='#e74c3c')
        
        # Clear video display
        self.video_display.config(image='')
        self.video_display.image = None
    
    def process_video(self):
        """Enhanced video processing loop with full body detection"""
        while self.running and self.cap and self.cap.isOpened():
            try:
                ret, frame = self.cap.read()
                if not ret:
                    break
                
                # Flip frame horizontally for mirror effect
                frame = np.flip(frame, axis=1)
                
                if self.background is not None:
                    # Apply enhanced invisibility cloak effect
                    processed_frame = self.apply_full_invisibility_cloak(frame)
                else:
                    processed_frame = frame
                
                # Convert frame for tkinter display
                self.display_frame(processed_frame)
                
                # Small delay to prevent excessive CPU usage
                time.sleep(0.03)
                
            except Exception as e:
                print(f"Error in video processing: {e}")
                break
    
    def apply_full_invisibility_cloak(self, frame):
        """Apply the enhanced full body invisibility cloak effect"""
        mode = self.detection_mode.get()
        
        # Update parameters from GUI
        self.expansion_factor = self.expansion_scale.get()
        self.blur_kernel_size = int(self.blur_scale.get())
        if self.blur_kernel_size % 2 == 0:  # Ensure odd kernel size
            self.blur_kernel_size += 1
        
        # Initialize final mask
        final_mask = np.zeros(frame.shape[:2], dtype=np.uint8)
        
        if mode in ['color', 'hybrid']:
            # Color-based detection (blue cloth)
            color_mask = self.create_color_mask(frame)
            final_mask = cv2.bitwise_or(final_mask, color_mask)
        
        if mode in ['person', 'hybrid']:
            # Person/motion detection
            person_mask = self.create_person_mask(frame)
            final_mask = cv2.bitwise_or(final_mask, person_mask)
        
        # Expand the mask to cover entire body
        if np.any(final_mask):
            final_mask = self.expand_mask_for_full_body(final_mask, frame.shape[:2])
        
        # Apply morphological operations
        final_mask = cv2.morphologyEx(final_mask, cv2.MORPH_CLOSE, self.kernel)
        final_mask = cv2.morphologyEx(final_mask, cv2.MORPH_DILATE, self.kernel)
        
        # Apply strong Gaussian blur for very smooth edges
        final_mask = cv2.GaussianBlur(final_mask, (self.blur_kernel_size, self.blur_kernel_size), 0)
        
        # Create inverse mask
        mask_inv = cv2.bitwise_not(final_mask)
        
        # Normalize masks to 0-1 range for blending
        mask_norm = final_mask.astype(float) / 255
        mask_inv_norm = mask_inv.astype(float) / 255
        
        # Apply the invisibility effect
        result = np.zeros_like(frame)
        
        for i in range(3):  # For each color channel
            result[:, :, i] = (mask_norm * self.background[:, :, i] + 
                              mask_inv_norm * frame[:, :, i])
        
        return result.astype(np.uint8)
    
    def create_color_mask(self, frame):
        """Create mask based on blue color detection"""
        # Update HSV values from GUI
        self.lower_blue1 = np.array([
            self.lower_h1_scale.get(),
            self.lower_s1_scale.get(),
            self.lower_v1_scale.get()
        ])
        self.upper_blue1 = np.array([
            self.lower_h1_scale.get() + 30,  # Wider range
            255,
            255
        ])
        
        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Create mask for blue color
        mask = cv2.inRange(hsv, self.lower_blue1, self.upper_blue1)
        
        return mask
    
    def create_person_mask(self, frame):
        """Create mask based on person/motion detection"""
        # Apply background subtraction
        fg_mask = self.bg_subtractor.apply(frame)
        
        # Find contours
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Create mask from person-sized contours
        person_mask = np.zeros(frame.shape[:2], dtype=np.uint8)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if self.min_person_area < area < self.max_person_area:
                cv2.fillPoly(person_mask, [contour], 255)
        
        return person_mask
    
    def expand_mask_for_full_body(self, mask, frame_shape):
        """Expand the detected region to cover the entire body"""
        # Find the bounding box of all detected regions
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return mask
        
        # Get overall bounding rectangle
        x_coords = []
        y_coords = []
        
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            x_coords.extend([x, x + w])
            y_coords.extend([y, y + h])
        
        if not x_coords or not y_coords:
            return mask
        
        min_x, max_x = min(x_coords), max(x_coords)
        min_y, max_y = min(y_coords), max(y_coords)
        
        # Expand the bounding box
        center_x, center_y = (min_x + max_x) // 2, (min_y + max_y) // 2
        width, height = max_x - min_x, max_y - min_y
        
        # Apply expansion factor
        new_width = int(width * self.expansion_factor)
        new_height = int(height * self.expansion_factor)
        
        # Calculate new coordinates
        new_min_x = max(0, center_x - new_width // 2)
        new_max_x = min(frame_shape[1], center_x + new_width // 2)
        new_min_y = max(0, center_y - new_height // 2)
        new_max_y = min(frame_shape[0], center_y + new_height // 2)
        
        # Create expanded mask
        expanded_mask = np.zeros(frame_shape, dtype=np.uint8)
        expanded_mask[new_min_y:new_max_y, new_min_x:new_max_x] = 255
        
        return expanded_mask
    
    def display_frame(self, frame):
        """Convert frame to tkinter format and display"""
        # Resize frame for display
        height, width = frame.shape[:2]
        display_width = 640
        display_height = int(height * display_width / width)
        
        frame_resized = cv2.resize(frame, (display_width, display_height))
        
        # Convert BGR to RGB
        frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
        
        # Convert to PIL Image
        image_pil = Image.fromarray(frame_rgb)
        
        # Convert to tkinter PhotoImage
        photo = ImageTk.PhotoImage(image_pil)
        
        # Update display (must be done in main thread)
        self.root.after(0, self.update_display, photo)
    
    def update_display(self, photo):
        """Update the video display widget"""
        if self.running:
            self.video_display.config(image=photo)
            self.video_display.image = photo
    
    def on_closing(self):
        """Handle window closing"""
        self.running = False
        if self.cap:
            self.cap.release()
        self.root.destroy()

def main():
    """Main function to run the enhanced application"""
    root = tk.Tk()
    app = FullInvisibilityCloakGUI(root)
    
    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Start the GUI main loop
    root.mainloop()

if __name__ == "__main__":
    main()
