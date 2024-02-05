import tkinter as tk
import json

title_font = ("Arial", 16)
body_font = ("Arial", 12)

class Functions():
    def __init__(self, root, user):
        self.root = root
        self.user = user

        # A label used to provide feedback to user.
        self.feedback_label = tk.Label(root, background='silver')

    @staticmethod
    def load_json_data(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data

    @staticmethod
    def save_json_data(file_path, data):
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=2)

    @staticmethod
    def exit_app(root):
        root.destroy()

    # Button to exit the application.
    def exit(self, root):
        exit_button = tk.Button(root, command=lambda: self.exit_app(root), text='Exit', font=body_font, width=12)
        exit_button.pack(padx=5, pady=5)
