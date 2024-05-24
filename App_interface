import tkinter as tk
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

label = tk.Label(root, text="Welcome to my app!")
label.pack()

button_customize = tk.Button(root, text="Customize", command=navigate_to_custom_code)
button_customize.pack()

button_run = tk.Button(root, text="Run", command=run_custom_code)
button_run.pack()

root.mainloop()
