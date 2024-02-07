import tkinter as tk

class HomePage:
    def __init__(self, root):
        self.root = root

        self.frame = tk.Frame(self.root, background="silver")
        self.frame.pack()

        self.label = tk.Label(self.frame, text="Welcome to the Home Page!", font=("Arial", 16))
        self.label.pack(pady=20)

        # Button to create study reminders
        self.create_reminders_button = tk.Button(self.frame, text="Create Study Reminders", command=self.create_reminders)
        self.create_reminders_button.pack(pady=10)

    def create_reminders(self):
        # Add functionality to create study reminders here
        print("Creating study reminders...")

def main():
    master = tk.Tk()
    app = HomePage(master)
    master.mainloop()

if __name__ == "__main__":
    main()
