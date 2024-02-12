import tkinter as tk

class HomePage:
    def __init__(self, root):
        self.root = root

        self.frame = tk.Frame(self.root, background="silver")
        self.frame.pack()

        self.label = tk.Label(self.frame, text="Welcome to the Home Page!", font=("Arial", 16))
        self.label.pack(pady=20)

        # Input field for academic interests
        self.interests_label = tk.Label(self.frame, text="Academic Interests:", font=("Arial", 12))
        self.interests_label.pack()
        self.interests_entry = tk.Entry(self.frame)
        self.interests_entry.pack(pady=5)

        # Input field for study reminder time
        self.reminder_label = tk.Label(self.frame, text="Study Reminder Time (HH:MM):", font=("Arial", 12))
        self.reminder_label.pack()
        self.reminder_entry = tk.Entry(self.frame)
        self.reminder_entry.pack(pady=5)

        # Button to save study reminders
        self.save_reminders_button = tk.Button(self.frame, text="Save Study Reminders", command=self.save_reminders)
        self.save_reminders_button.pack(pady=10)

    def save_reminders(self):
        # Get the values entered by the user
        interests = self.interests_entry.get()
        reminder_time = self.reminder_entry.get()

        # Add functionality to save study reminders here
        print("Academic Interests:", interests)
        print("Study Reminder Time:", reminder_time)

def main():
    master = tk.Tk()
    app = HomePage(master)
    master.mainloop()

if __name__ == "__main__":
    main()