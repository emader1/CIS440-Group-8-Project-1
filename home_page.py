import tkinter as tk
import mysql.connector

class HomePage:
    def __init__(self, root, db_connection, cursor):
        self.root = root
        self.db_connection = db_connection
        self.cursor = cursor

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

        # Write SQL query to insert study reminders
        query = "INSERT INTO study_sessions (interests, reminder_time) VALUES (%s, %s)"
        data = (interests, reminder_time)

        # Execute the query
        self.cursor.execute(query, data)
        self.db_connection.commit()

        print("Study reminders saved successfully.")

def main():
    # Establish connection to MySQL server
    db_connection = mysql.connector.connect(
        host="107.180.1.16",
        port="3306",
        user="spring2024Cteam8",
        password="spring2024Cteam8",
        database="spring2024Cteam8"
    )
    cursor = db_connection.cursor()

    master = tk.Tk()
    app = HomePage(master, db_connection, cursor)
    master.mainloop()

    # Close the database connection when done
    cursor.close()
    db_connection.close()

if __name__ == "__main__":
    main()
