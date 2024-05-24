import tkinter as tk
from PIL import Image, ImageTk
import os
import subprocess

def greet():
    print("Hello, Tkinter!")

def navigate_to_custom_code():
    # Path to the document containing code
    file_path = "C:/project/Coustom_gesture.py"  # Replace with the actual path to your document

    # Check if the file exists
    if os.path.exists(file_path):
        # Open the document using the default application
        os.startfile(file_path)
    else:
        print("File not found.")

def run_custom_code():
    # Path to the document containing code
    file_path = r"C:\project\Coustom_gesture.py"  # Replace with the actual path to your document

    # Check if the file exists
    if os.path.exists(file_path):
        # Run the Python script
        subprocess.Popen(["python", file_path], shell=True)
    else:
        print("File not found.")

root = tk.Tk()
root.title("My Application")

# Set the size of the window
root.geometry("577x397")  # Set the width and height as desired

# Load the image
image_path = "C:/project/app.png"  # Replace with the path to your image
if os.path.exists(image_path):
    image = Image.open(image_path)
    background_image = ImageTk.PhotoImage(image)

    # Create a label with the background image
    background_label = tk.Label(root, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
else:
    print("Image not found.")

label = tk.Label(root, text="Welcome to our app!", bg="white")
label.pack()

# Create a frame for the buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=20)  # Add padding between the buttons and other widgets

button_customize = tk.Button(button_frame, text="Customize", command=navigate_to_custom_code)
button_customize.grid(row=0, column=0, padx=10)  # Add padding between the buttons
button_run = tk.Button(button_frame, text="Run", command=run_custom_code)
button_run.grid(row=0, column=1, padx=10)  # Add padding between the buttons

# Add credit text
credit_text = "Credits:\nM Revanth\nV Revanth\nSiddaratha"
credit_label = tk.Label(root, text=credit_text, bg="white", justify="right")
credit_label.place(relx=1, rely=1, anchor="se", x=-10, y=-10)  # Place at the bottom right corner with a margin

root.mainloop()
