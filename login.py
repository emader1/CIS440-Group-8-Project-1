import tkinter as tk
import tkinter.ttk
import mysql.connector
from home_page import HomePage

title_font = ("Helvetica", 16)
body_font = ("Helvetica", 12)

# Class that configures the main window of the app. All windows are placed inside this window.
class ParentWindow():
    def __init__(self, root):
        self.root = root
        self.root.geometry("600x600")
        self.root.config(background="silver")
        self.feedback_label = tk.Label(root, background='silver')

    # Loads in the login window.
    def load_main(self):
        login_window = LoginWindow(self.root)
        login_window.load_main()

    # Closes the app.
    def exit_app(self, root):
        root.destroy()

    # Button to close the app.
    def exit_button(self, frame, root):
        exit_button = tk.Button(frame, command=lambda: self.exit_app(root), text='Exit', font=body_font, width=12)
        exit_button.pack(padx=5, pady=5)

class LoginWindow(ParentWindow):
    def __init__(self, root):
        super().__init__(root)
        self.root = root

        # Connection to MySQL database.
        self.db_connection = mysql.connector.connect(
            host="107.180.1.16",
            port="3306",
            user="spring2024Cteam8",
            password="spring2024Cteam8",
            database="spring2024Cteam8"
        )
        self.cursor = self.db_connection.cursor()

        # Frame containing login information.
        self.login_frame = tk.Frame(self.root, background="silver")
        # Frame for creating a new account.
        self.account_frame = tk.Frame(self.root, background="silver")
        # Frame for configuring a new user's preferences.
        self.preference_frame = tk.Frame(self.root, background='silver')
        # Frame for the weekly calendar in the preference window.
        self.calendar_frame = tk.Frame(self.root, background='silver')

    def load_main(self):
        for widget in self.login_frame.winfo_children():
            widget.destroy()

        label_frame = tk.Frame(self.login_frame, borderwidth=2, relief='sunken')
        label_frame.pack(padx=5, pady=5, ipadx=10, ipady=10)

        login_label = tk.Label(label_frame, text='Login', font=title_font)
        login_label.pack()

        # User's email and password input label.
        email_label = tk.Label(label_frame, text='Email:', font=body_font)
        email_label.pack(padx=5, pady=5)
        self.email_var = tk.StringVar()
        email_entry = tk.Entry(label_frame, textvariable=self.email_var)
        email_entry.pack()

        # User's password label. All inputs show in '*'.
        password_label = tk.Label(label_frame, text='Password:', font=body_font)
        password_label.pack(padx=5, pady=5)
        self.password_var = tk.StringVar()
        password_entry = tk.Entry(label_frame, show='*', textvariable=self.password_var)
        password_entry.pack()

        button_frame = tk.Frame(self.login_frame, background="silver")
        button_frame.pack(padx=5, pady=5, ipadx=10, ipady=10)

        self.feedback_label.pack()

        login_button = tk.Button(button_frame, command=self.login, text='Login', font=body_font, width=12)
        login_button.pack(padx=5, pady=5)

        create_account_button = tk.Button(button_frame, command=lambda: [self.login_frame.pack_forget(), self.account_window()], text='Create Account', font=body_font, width=12)
        create_account_button.pack(padx=5, pady=5)

        self.exit_button(button_frame, self.root)

        self.login_frame.pack()

    # Uses the mySQL database to validate user's credentials.
    def login(self):
        query = "SELECT user_type FROM users WHERE email = %s AND password = %s"
        self.cursor.execute(query, (self.email_var.get(), self.password_var.get()))
        user = self.cursor.fetchone()

        if user:
            user_type = user[0]  # Assuming user_type is the first column in the users table
            self.feedback_label.config(text='Login Successful!')
            self.login_frame.pack_forget()
            self.feedback_label.pack_forget()
            home_page = HomePage(self.root, self.db_connection, self.cursor, self.email_var.get(), user_type)
            home_page.load_main()
        else:
            self.feedback_label.config(text='Invalid Email or Password.')

    # Window allowing users to create a new account.
    def account_window(self):
        for widget in self.account_frame.winfo_children():
            widget.destroy()

        label_frame = tk.Frame(self.account_frame, borderwidth=2, relief='sunken')
        label_frame.pack(padx=5, pady=5, ipadx=10, ipady=10)

        login_label = tk.Label(label_frame, text='Create Account', font=title_font)
        login_label.pack()

        # User's first name label.
        fname_label = tk.Label(label_frame, text='First Name:', font=body_font)
        fname_label.pack(padx=5, pady=5)
        fname_var = tk.StringVar()
        fname_entry = tk.Entry(label_frame, textvariable=fname_var)
        fname_entry.pack()

        # User's last name label.
        lname_label = tk.Label(label_frame, text='Last Name:', font=body_font)
        lname_label.pack(padx=5, pady=5)
        lname_var = tk.StringVar()
        lname_entry = tk.Entry(label_frame, textvariable=lname_var)
        lname_entry.pack()

        # User's email label.
        email_label = tk.Label(label_frame, text='Email:', font=body_font)
        email_label.pack(padx=5, pady=5)
        email_var = tk.StringVar()
        email_entry = tk.Entry(label_frame, textvariable=email_var)
        email_entry.pack()

        # User's username label.
        username_label = tk.Label(label_frame, text='Username:', font=body_font)
        username_label.pack(padx=5, pady=5)
        username_var = tk.StringVar()
        username_entry = tk.Entry(label_frame, textvariable=username_var)
        username_entry.pack()

        # User's password label. All inputs show in '*'.
        password_label = tk.Label(label_frame, text='Password:', font=body_font)
        password_label.pack(padx=5, pady=5)
        password_var = tk.StringVar()
        password_entry = tk.Entry(label_frame, show='*', textvariable=password_var)
        password_entry.pack()

        button_frame = tk.Frame(self.account_frame, background="silver")
        button_frame.pack(padx=5, pady=5, ipadx=10, ipady=10)

        create_account_button = tk.Button(button_frame, command=lambda: [self.create_account(email_var.get(), password_var.get(), fname_var.get(), lname_var.get(), username_var.get())], text='Create Account', font=body_font, width=12)
        create_account_button.pack(padx=5, pady=5)

        login_window_button = tk.Button(button_frame, command=lambda: [self.login_frame.pack(), self.account_frame.pack_forget()], text='Previous', font=body_font, width=12)
        login_window_button.pack(padx=5, pady=5)

        self.exit_button(button_frame, self.root)

        self.account_frame.pack()

    # Uses mySQL database to create new accounts.
    def create_account(self, email, password, fname, lname, username):
        try:
            query = "SELECT * FROM users WHERE email = %s"
            self.cursor.execute(query, (email,))
            existing_user = self.cursor.fetchone()

            if existing_user:
                self.feedback_label.config(text='Email is already linked to an account.')
            else:
                if "@" in email and (email.endswith(".com") or email.endswith(".org") or email.endswith(".edu")):
                    allowed_characters = set("!@#$%^&*()-_=+[]{}|;:'\",.<>/?`~")
                    if len(password) >= 6:
                        if all(char.isalnum() or char in allowed_characters for char in password):
                            self.preference_window(email, password, fname, lname, username)
                            self.account_frame.pack_forget()
                        else:
                            self.feedback_label.config(text='Password contains invalid characters.')
                    else:
                        self.feedback_label.config(text='Password must be at least 6 characters.')
                else:
                    self.feedback_label.config(text='Invalid Email Address.')
        except mysql.connector.IntegrityError as e:
            self.feedback_label.config(text='Error: Email or username already exists. Please choose different credentials.')
            print(f"Error: {e}")
        except Exception as e:
            self.feedback_label.config(text='An unexpected error occurred. Please try again later.')
            print(f"Unexpected Error: {e}")

    # Window that allows users to enter preferences. Preferences include study times and classes.
    def preference_window(self, email, password, fname, lname, username):
        for widget in self.preference_frame.winfo_children():
            widget.destroy()

        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        def add_class():
            selected_item = class_combobox.get()
            if selected_item and selected_item not in self.class_listbox.get(0, tk.END):
                self.class_listbox.insert(tk.END, selected_item)

        def delete_class(event):
            selected_index = self.class_listbox.curselection()
            if selected_index:
                self.class_listbox.delete(selected_index)

        self.calendar_frame.pack(padx=5, pady=5)
        self.preference_frame.pack()

        # Function that creates a weekly calendar.
        self.create_calendar()

        # Frame for the listbox entry.
        listbox_frame = tk.Frame(self.preference_frame, borderwidth=2, relief='sunken')
        listbox_frame.pack(padx=5, pady=5, ipadx=10, ipady=10)

        # Frame for the combobox, as well as the button. Places the button to the right of the combobox.
        combobox_frame = tk.Frame(listbox_frame)
        combobox_frame.pack(padx=5, pady=5)

        # List of classes.
        class_list = ['Supply Chain', 'CIS', 'Biology','Physics', 'Math']
        class_combobox = tkinter.ttk.Combobox(combobox_frame, values=class_list)
        class_combobox.pack(side=tk.LEFT, padx=5, pady=5)

        add_button = tk.Button(combobox_frame, text='Add', command=add_class)
        add_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.class_listbox = tk.Listbox(listbox_frame, width=60)
        self.class_listbox.pack()
        self.class_listbox.bind('<Double-Button-1>', delete_class)

        # Frame for the buttons.
        button_frame = tk.Frame(self.preference_frame, background="silver")
        button_frame.pack(padx=5, pady=5, ipadx=10, ipady=10)

        save_changes_button = tk.Button(button_frame, command=lambda: [self.save_preferences(email, password, fname, lname, username), self.calendar_frame.pack_forget(), self.preference_frame.pack_forget(), self.login_frame.pack()], text='Save Changes',font=body_font, width=12)
        save_changes_button.pack()

        self.exit_button(button_frame, self.root)

    def save_preferences(self, email, password, fname, lname, username):
        try:
            days = ','.join([day_name for day_name, selected in self.selected_days.items() if selected])
            preferences = ",".join(self.class_listbox.get(0, tk.END)) if self.class_listbox else ""

            query = "INSERT INTO users (email, password, fname, lname, username, preferences, days) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            self.cursor.execute(query, (email, password, fname, lname, username, preferences, days))
            self.db_connection.commit()
            self.feedback_label.config(text='Success! Account has been created.\nReturn to the home page to login.')
        except Exception as e:
            self.feedback_label.config(text='An unexpected error occurred while saving preferences. Please try again later.')
            print(f"Unexpected Error: {e}")

    def create_calendar(self):
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        # Create frames for the days of the week.
        week_frame = tk.Frame(self.calendar_frame)
        week_frame.pack(side=tk.TOP, fill=tk.X)

        # Dictionary to store the selected state of each day
        self.selected_days = {day_name: False for day_name in days_of_week}

        def toggle_day_selection(day_name):
            self.selected_days[day_name] = not self.selected_days[day_name]
            update_day_colors()

        def update_day_colors():
            for day_name, selected in self.selected_days.items():
                color = "lightgreen" if selected else "lightgray"
                day_labels[day_name].config(background=color)

        day_labels = {}

        for day_name in days_of_week:
            day_frame = tk.Frame(week_frame)
            day_frame.pack(side=tk.LEFT)

            # Creates the calendar label for each day.
            day_label = tk.Label(day_frame, text=day_name, width=10, height=3, relief=tk.GROOVE, background="lightgray", anchor="nw", padx=5, pady=5)
            day_label.pack(side=tk.TOP)
            day_label.bind("<Button-1>", lambda event, day_name=day_name: toggle_day_selection(day_name))

            day_labels[day_name] = day_label

def main():
    master = tk.Tk()
    app = ParentWindow(master)
    app.load_main()
    master.mainloop()

if __name__ == "__main__":
    main()
