#!/usr/bin/env python3
"""
Harry Potter Invisibility Cloak - GUI Version
Real-time invisibility cloak using computer vision with a user-friendly GUI interface.

Features:
- Real-time video processing
- Color detection and masking
- GUI controls for HSV calibration
- Start/Stop functionality
- Background capture
"""

import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import threading
import time

class InvisibilityCloakGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Harry Potter Invisibility Cloak")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2c3e50')
        
        # Video capture variables
        self.cap = None
        self.background = None
        self.running = False
        self.thread = None
        
        # HSV color range for blue cloak (default values)
        self.lower_blue1 = np.array([100, 50, 50])
        self.upper_blue1 = np.array([130, 255, 255])
        self.lower_blue2 = np.array([100, 50, 50])  # Blue doesn't wrap around like red
        self.upper_blue2 = np.array([130, 255, 255])
        
        # Morphological operations kernel
        self.kernel = np.ones((3, 3), np.uint8)
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the GUI interface"""
        # Title
        title_frame = tk.Frame(self.root, bg='#2c3e50')
        title_frame.pack(fill='x', padx=10, pady=10)
        
        title_label = tk.Label(
            title_frame,
            text="🪄 Harry Potter Invisibility Cloak (Blue) 🪄",
            font=('Arial', 24, 'bold'),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Bring magic to life with computer vision!",
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
            text="Video Feed",
            font=('Arial', 14, 'bold'),
            fg='#ecf0f1',
            bg='#34495e'
        )
        video_label.pack(pady=5)
        
        self.video_display = tk.Label(video_frame, bg='black')
        self.video_display.pack(padx=10, pady=10)
        
        # Right panel for controls
        control_frame = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=2, width=300)
        control_frame.pack(side='right', fill='y', padx=(5, 0))
        control_frame.pack_propagate(False)
        
        control_label = tk.Label(
            control_frame,
            text="Controls",
            font=('Arial', 14, 'bold'),
            fg='#ecf0f1',
            bg='#34495e'
        )
        control_label.pack(pady=10)
        
        # Control buttons
        button_frame = tk.Frame(control_frame, bg='#34495e')
        button_frame.pack(fill='x', padx=10, pady=5)
        
        self.start_btn = tk.Button(
            button_frame,
            text="🎬 Start Magic",
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
        
        # HSV Controls
        hsv_frame = tk.LabelFrame(
            control_frame,
            text="Color Detection Settings",
            font=('Arial', 12, 'bold'),
            fg='#ecf0f1',
            bg='#34495e'
        )
        hsv_frame.pack(fill='x', padx=10, pady=10)
        
        # Lower HSV Range 1
        tk.Label(hsv_frame, text="Lower Blue Range:", fg='#ecf0f1', bg='#34495e').pack(anchor='w')
        
        self.lower_h1_scale = self.create_scale(hsv_frame, "H", 0, 179, self.lower_blue1[0])
        self.lower_s1_scale = self.create_scale(hsv_frame, "S", 0, 255, self.lower_blue1[1])
        self.lower_v1_scale = self.create_scale(hsv_frame, "V", 0, 255, self.lower_blue1[2])
        
        # Upper HSV Range 1
        tk.Label(hsv_frame, text="Upper Blue Range:", fg='#ecf0f1', bg='#34495e').pack(anchor='w', pady=(10, 0))
        
        self.upper_h1_scale = self.create_scale(hsv_frame, "H", 0, 179, self.upper_blue1[0])
        self.upper_s1_scale = self.create_scale(hsv_frame, "S", 0, 255, self.upper_blue1[1])
        self.upper_v1_scale = self.create_scale(hsv_frame, "V", 0, 255, self.upper_blue1[2])
        
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
            text="Camera not started",
            font=('Arial', 10),
            fg='#f39c12',
            bg='#34495e'
        )
        self.status_label.pack(anchor='w')
        
        # Instructions
        instructions_frame = tk.LabelFrame(
            control_frame,
            text="Instructions",
            font=('Arial', 10, 'bold'),
            fg='#ecf0f1',
            bg='#34495e'
        )
        instructions_frame.pack(fill='x', padx=10, pady=5)
        
        instructions = [
            "1. Click 'Start Magic' to begin",
            "2. Click 'Capture Background'",
            "3. Move away from camera",
            "4. Put on blue cloak/cloth",
            "5. Enjoy being invisible! ✨"
        ]
        
        for instruction in instructions:
            tk.Label(
                instructions_frame,
                text=instruction,
                font=('Arial', 9),
                fg='#bdc3c7',
                bg='#34495e',
                anchor='w'
            ).pack(fill='x', padx=5, pady=1)
    
    def create_scale(self, parent, label, from_val, to_val, initial_val):
        """Create a labeled scale widget"""
        frame = tk.Frame(parent, bg='#34495e')
        frame.pack(fill='x', pady=2)
        
        tk.Label(frame, text=f"{label}:", fg='#ecf0f1', bg='#34495e', width=3).pack(side='left')
        
        scale = tk.Scale(
            frame,
            from_=from_val,
            to=to_val,
            orient='horizontal',
            bg='#2c3e50',
            fg='#ecf0f1',
            highlightbackground='#34495e',
            troughcolor='#2c3e50'
        )
        scale.set(initial_val)
        scale.pack(side='left', fill='x', expand=True)
        
        return scale
    
    def update_hsv_values(self):
        """Update HSV values from scale widgets"""
        self.lower_blue1 = np.array([
            self.lower_h1_scale.get(),
            self.lower_s1_scale.get(),
            self.lower_v1_scale.get()
        ])
        self.upper_blue1 = np.array([
            self.upper_h1_scale.get(),
            self.upper_s1_scale.get(),
            self.upper_v1_scale.get()
        ])
    
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
            self.status_label.config(text="Camera started - Ready to capture background", fg='#27ae60')
            
            # Start video processing thread
            self.thread = threading.Thread(target=self.process_video)
            self.thread.daemon = True
            self.thread.start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start camera: {str(e)}")
    
    def capture_background(self):
        """Capture the background frame"""
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                self.background = np.flip(frame, axis=1).copy()
                self.status_label.config(text="Background captured - Put on your blue cloak!", fg='#3498db')
                messagebox.showinfo("Background Captured", 
                                  "Background captured successfully!\nNow put on your blue cloak and see the magic happen!")
    
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
        """Main video processing loop"""
        while self.running and self.cap and self.cap.isOpened():
            try:
                ret, frame = self.cap.read()
                if not ret:
                    break
                
                # Flip frame horizontally for mirror effect
                frame = np.flip(frame, axis=1)
                
                # Update HSV values from GUI
                self.update_hsv_values()
                
                if self.background is not None:
                    # Apply invisibility cloak effect
                    processed_frame = self.apply_invisibility_cloak(frame)
                else:
                    processed_frame = frame
                
                # Convert frame for tkinter display
                self.display_frame(processed_frame)
                
                # Small delay to prevent excessive CPU usage
                time.sleep(0.03)
                
            except Exception as e:
                print(f"Error in video processing: {e}")
                break
    
    def apply_invisibility_cloak(self, frame):
        """Apply the invisibility cloak effect"""
        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Create mask for blue color (cloak)
        mask1 = cv2.inRange(hsv, self.lower_blue1, self.upper_blue1)
        mask2 = cv2.inRange(hsv, self.lower_blue2, self.upper_blue2)
        mask = mask1 + mask2
        
        # Morphological operations to clean up the mask
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, self.kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, self.kernel)
        
        # Create inverse mask
        mask_inv = cv2.bitwise_not(mask)
        
        # Apply Gaussian blur to soften edges
        mask = cv2.GaussianBlur(mask, (5, 5), 0)
        mask_inv = cv2.GaussianBlur(mask_inv, (5, 5), 0)
        
        # Normalize masks to 0-1 range for blending
        mask_norm = mask.astype(float) / 255
        mask_inv_norm = mask_inv.astype(float) / 255
        
        # Apply the invisibility effect
        result = np.zeros_like(frame)
        
        for i in range(3):  # For each color channel
            result[:, :, i] = (mask_norm * self.background[:, :, i] + 
                              mask_inv_norm * frame[:, :, i])
        
        return result.astype(np.uint8)
    
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
    """Main function to run the application"""
    root = tk.Tk()
    app = InvisibilityCloakGUI(root)
    
    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Start the GUI main loop
    root.mainloop()

if __name__ == "__main__":
    main()
