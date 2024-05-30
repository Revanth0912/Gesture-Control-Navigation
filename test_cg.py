import tkinter as tk
from tkinter import messagebox, simpledialog
import subprocess
import threading
import os
import sys
from PIL import Image, ImageTk
import tkinter.filedialog

# Global dictionary to store gesture-application associations
gesture_applications = {
    "Open Instagram": None,
    "Open Notepad": None,
    "Click": None
}

# Function to start the gesture recognition script
def start_script():
    global process
    file_path = r"C:/project/Coustom_gesture.py"  # Replace with the actual path to your script
    if os.path.exists(file_path):
        try:
            process = subprocess.Popen([sys.executable, file_path], shell=True)
            messagebox.showinfo("Info", "Gesture recognition started!")
        except Exception as e:
            messagebox.showerror("Error", f"Error launching custom code: {e}")
    else:
        messagebox.showerror("Error", "File not found.")

# Function to stop the gesture recognition script
def stop_script():
    global process
    if is_running():
        process.terminate()
        process = None
        messagebox.showinfo("Info", "Gesture recognition stopped!")
    else:
        messagebox.showwarning("Warning", "Gesture recognition is not running.")

# Function to perform custom action
def custom_action():
    def change_gesture():
        def modify_gesture():
            def on_selection(event=None):  # Make event argument optional
                selected_gesture = gesture_option.get()
                selected_file = tkinter.filedialog.askopenfilename(title="Select Application", filetypes=[("Executable files", "*.exe")])
                if selected_file:
                    gesture_applications[selected_gesture] = selected_file  # Update the application association
                    messagebox.showinfo("Gesture Changed", f"Gesture '{selected_gesture}' changed. Application: {selected_file}")
                    
            gesture_options = list(gesture_applications.keys())  # Get gesture names from the dictionary
            custom_dialog = tk.Toplevel(root)
            custom_dialog.title("Modify Gesture")
            gesture_label = tk.Label(custom_dialog, text="Select Gesture:")
            gesture_label.pack()
            gesture_option = tk.StringVar()
            gesture_option.set(gesture_options[0])  # Set default option
            gesture_dropdown = tk.OptionMenu(custom_dialog, gesture_option, *gesture_options)
            gesture_dropdown.pack()
            confirm_button = tk.Button(custom_dialog, text="Confirm", command=on_selection)
            confirm_button.pack()

        modify_gesture()

    def add_gesture():
        messagebox.showinfo("Custom Action", "Adding a custom gesture...")
        # Add code to add custom gesture

    custom_dialog = tk.Toplevel(root)
    custom_dialog.title("Custom Action")

    change_button = tk.Button(custom_dialog, text="Change a default gesture", font=("Arial", 14), command=change_gesture)
    change_button.pack(pady=10)

    add_button = tk.Button(custom_dialog, text="Add a custom gesture", font=("Arial", 14), command=add_gesture)
    add_button.pack(pady=10)


def launch_application(gesture):
    if gesture_applications[gesture]:
        try:
            subprocess.Popen([gesture_applications[gesture]], shell=True)
        except Exception as e:
            messagebox.showerror("Error", f"Error launching application: {e}")
    else:
        messagebox.showerror("Error", f"No application associated with gesture '{gesture}'")

# Function to check if the process is running
def is_running():
    return process is not None and process.poll() is None

# Create the main window
root = tk.Tk()
root.title("Hand Gesture Recognition Interface")
root.geometry("750x700")

# Create and place the header
header = tk.Label(root, text="Hand Gesture Recognition App", font=("Arial", 24))
header.pack(pady=10)

# Create and place the demonstration section
demo = tk.Label(root, text="Gesture Demonstrations:", font=("Arial", 18))
demo.pack(pady=10)

# Create and place the image display area
image_frame = tk.Frame(root)
image_frame.pack(pady=10)

gesture_image_paths = [
    r"C:\project\assets\app.png",
    r"C:\project\assets\spider_man_pose.jpg",
    r"C:\project\assets\notepad_pose.jpg",
    r"C:\project\assets\click_pose.jpg"
]

gesture_texts = [
    "Move the cursor",
    "Spider-man Pose (right hand): Open Instagram",
    "All Fingers Up (except thumb): Open Notepad",
    "Thumb and Index Finger Pinch: Click"
]

current_slide = 0
image_label = tk.Label(image_frame)
text_label = tk.Label(root, font=("Arial", 14), justify="left")
image_label.pack(pady=10)
text_label.pack(pady=10)

def show_slide(index):
    global current_slide
    current_slide = index
    image_path = gesture_image_paths[current_slide]
    text = gesture_texts[current_slide]
    image = Image.open(image_path)
    image = image.resize((400, 400), Image.LANCZOS)
    image = ImageTk.PhotoImage(image)
    image_label.configure(image=image)
    image_label.image = image
    text_label.configure(text=text)

# Show the initial slide
show_slide(current_slide)

# Function to show next slide
def next_slide():
    global current_slide
    current_slide = (current_slide + 1) % len(gesture_image_paths)
    show_slide(current_slide)

# Function to show previous slide
def prev_slide():
    global current_slide
    current_slide = (current_slide - 1) % len(gesture_image_paths)
    show_slide(current_slide)

# Load arrow images
prev_button = tk.Button(root, text="<-", font=("Arial", 16), command=prev_slide)
prev_button.place(relx=0.05, rely=0.5, anchor=tk.CENTER)

next_button = tk.Button(root, text="->", font=("Arial", 16), command=next_slide)
next_button.place(relx=0.95, rely=0.5, anchor=tk.CENTER)

# Create and place the control buttons
control_frame = tk.Frame(root)
control_frame.pack(pady=20)

start_button = tk.Button(control_frame, text="Start", font=("Arial", 16), command=lambda: threading.Thread(target=start_script).start())
start_button.grid(row=0, column=0, padx=20)

custom_button = tk.Button(control_frame, text="Custom", font=("Arial", 16), command=custom_action)
custom_button.grid(row=0, column=1, padx=20)

stop_button = tk.Button(control_frame, text="Stop", font=("Arial", 16), command=stop_script)
stop_button.grid(row=0, column=2, padx=20)

# Initialize the process variable
process = None

# Start the Tkinter event loop
root.mainloop()
