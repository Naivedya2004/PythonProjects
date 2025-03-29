import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class GreenScreenReplacer:
    def __init__(self):
        # Initialize the main window
        self.root = tk.Tk()
        self.root.title("🎬 Magic Green Screen Replacer")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2C3E50')

        # Style configuration
        self.style = {
            'bg': '#2C3E50',
            'fg': '#ECF0F1',
            'button_bg': '#3498DB',
            'button_active': '#2980B9'
        }

        self.setup_gui()
        
        # Initialize video capture
        self.cap = None
        self.background_image = None
        self.is_running = False

    def setup_gui(self):
        # Create main frame
        main_frame = tk.Frame(self.root, bg=self.style['bg'])
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Video display area
        self.video_label = tk.Label(main_frame, bg='black')
        self.video_label.pack(expand=True, fill='both', padx=10, pady=10)

        # Control panel
        control_frame = tk.Frame(main_frame, bg=self.style['bg'])
        control_frame.pack(fill='x', padx=10, pady=10)

        # Buttons
        tk.Button(
            control_frame,
            text="Start Camera",
            command=self.start_camera,
            bg=self.style['button_bg'],
            fg=self.style['fg'],
            font=('Arial', 12, 'bold'),
            padx=20,
            pady=10
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            control_frame,
            text="Select Background",
            command=self.select_background,
            bg=self.style['button_bg'],
            fg=self.style['fg'],
            font=('Arial', 12, 'bold'),
            padx=20,
            pady=10
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            control_frame,
            text="Stop",
            command=self.stop_camera,
            bg=self.style['button_bg'],
            fg=self.style['fg'],
            font=('Arial', 12, 'bold'),
            padx=20,
            pady=10
        ).pack(side=tk.LEFT, padx=5)

        # Sliders for HSV adjustment
        self.create_hsv_sliders(main_frame)

    def create_hsv_sliders(self, parent):
        slider_frame = tk.Frame(parent, bg=self.style['bg'])
        slider_frame.pack(fill='x', padx=10, pady=10)

        # Default HSV values for green color
        self.hsv_values = {
            'Lower Hue': tk.IntVar(value=35),
            'Upper Hue': tk.IntVar(value=85),
            'Lower Saturation': tk.IntVar(value=30),
            'Upper Saturation': tk.IntVar(value=255),
            'Lower Value': tk.IntVar(value=30),
            'Upper Value': tk.IntVar(value=255)
        }

        # Create sliders
        for name, var in self.hsv_values.items():
            frame = tk.Frame(slider_frame, bg=self.style['bg'])
            frame.pack(fill='x', pady=5)
            
            tk.Label(
                frame,
                text=name,
                bg=self.style['bg'],
                fg=self.style['fg'],
                font=('Arial', 10)
            ).pack(side=tk.LEFT, padx=5)
            
            tk.Scale(
                frame,
                from_=0,
                to=255,
                orient=tk.HORIZONTAL,
                variable=var,
                bg=self.style['button_bg'],
                fg=self.style['fg'],
                length=200
            ).pack(side=tk.LEFT, padx=5)

    def select_background(self):
        """Open file dialog to select background image"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.webp")]
        )
        if file_path:
            self.background_image = cv2.imread(file_path)
            if self.background_image is not None:
                print("Background image loaded successfully!")
            else:
                print("Error loading background image!")

    def start_camera(self):
        """Start the webcam capture"""
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)
            self.is_running = True
            self.update_frame()

    def stop_camera(self):
        """Stop the webcam capture"""
        self.is_running = False
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        self.video_label.configure(image='')

    def apply_green_screen(self, frame):
        """Apply the green screen effect to the frame"""
        if self.background_image is None:
            return frame

        # Resize background to match frame size
        background = cv2.resize(self.background_image, (frame.shape[1], frame.shape[0]))

        # Convert frame to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Create mask for green screen
        lower_green = np.array([
            self.hsv_values['Lower Hue'].get(),
            self.hsv_values['Lower Saturation'].get(),
            self.hsv_values['Lower Value'].get()
        ])
        upper_green = np.array([
            self.hsv_values['Upper Hue'].get(),
            self.hsv_values['Upper Saturation'].get(),
            self.hsv_values['Upper Value'].get()
        ])

        # Create mask and its inverse
        mask = cv2.inRange(hsv, lower_green, upper_green)
        mask_inv = cv2.bitwise_not(mask)

        # Extract foreground and background
        fg = cv2.bitwise_and(frame, frame, mask=mask_inv)
        bg = cv2.bitwise_and(background, background, mask=mask)

        # Combine foreground and background
        result = cv2.add(fg, bg)
        return result

    def update_frame(self):
        """Update the video frame"""
        if self.is_running and self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Apply green screen effect
                processed_frame = self.apply_green_screen(frame)

                # Convert to RGB for tkinter
                rgb_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
                
                # Convert to PhotoImage
                image = Image.fromarray(rgb_frame)
                photo = ImageTk.PhotoImage(image=image)
                
                # Update label
                self.video_label.configure(image=photo)
                self.video_label.image = photo
                
                # Schedule next update
                self.root.after(10, self.update_frame)

    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = GreenScreenReplacer()
    app.run() 