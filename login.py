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

    def load_main(self):
        self.login_frame = tk.Frame(self.root, background="silver")

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

        create_account_button = tk.Button(button_frame, command=lambda: [self.login_frame.pack_forget(), self.account_window(), self.feedback_label.pack_forget()], text='Create Account', font=body_font, width=12)
        create_account_button.pack(padx=5, pady=5)

        self.exit_button(button_frame, self.root)

        self.login_frame.pack()

    # Uses the mySQL database to validate user's credentials.
    def login(self):
        query = "SELECT * FROM users WHERE email = %s AND password = %s"
        self.cursor.execute(query, (self.email_var.get(), self.password_var.get()))
        user = self.cursor.fetchone()

        if user:
            self.feedback_label.config(text='Login Successful!')
            self.login_frame.pack_forget()
            self.feedback_label.pack_forget()
            home_page = HomePage(self.root, self.db_connection, self.cursor)
            home_page.load_main()
        else:
            self.feedback_label.config(text='Invalid Email or Password.')

    # Window allowing users to create a new account.
    def account_window(self):
        self.account_frame = tk.Frame(self.root, background="silver")

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

        login_window_button = tk.Button(button_frame, command=lambda: [self.login_frame.pack(), self.account_frame.pack_forget(), self.feedback_label.pack_forget()], text='Previous', font=body_font, width=12)
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
                            query = "INSERT INTO users (email, password, fname, lname, username) VALUES (%s, %s, %s, %s, %s)"
                            self.cursor.execute(query, (email, password, fname, lname, username))
                            self.db_connection.commit()
                            self.feedback_label.config(text='Success! Account has been created.\nReturn to the home page to login.')
                            self.preference_window()
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
    def preference_window(self):
        def add_class():
            selected_item = class_combobox.get()
            if selected_item and selected_item not in class_listbox.get(0, tk.END):
                class_listbox.insert(tk.END, selected_item)

        def delete_class(event):
            selected_index = class_listbox.curselection()
            if selected_index:
                class_listbox.delete(selected_index)

        # Frame that controls the entire window.
        self.preference_frame = tk.Frame(self.root, background='silver')
        self.preference_frame.pack()

        # Frame that places the weekly calendar.
        self.calendar_frame = tk.Frame(self.preference_frame, background='silver')
        self.calendar_frame.pack(padx=5, pady=5)

        # Function that creates a weekly calendar.
        self.create_calendar()

        # Frame for the listbox entry.
        listbox_frame = tk.Frame(self.preference_frame, borderwidth=2, relief='sunken')
        listbox_frame.pack(padx=5, pady=5, ipadx=10, ipady=10)

        # Frame for the combobox, as well as the button. Places the button to the right of the combobox.
        combobox_frame = tk.Frame(listbox_frame)
        combobox_frame.pack(padx=5, pady=5)

        # List of classes.
        class_list = ['CIS440', 'CIS430']
        class_combobox = tkinter.ttk.Combobox(combobox_frame, values=class_list)
        class_combobox.pack(side=tk.LEFT, padx=5, pady=5)

        add_button = tk.Button(combobox_frame, text='Add', command=add_class)
        add_button.pack(side=tk.LEFT, padx=5, pady=5)

        class_listbox = tk.Listbox(listbox_frame, width=60)
        class_listbox.pack()
        class_listbox.bind('<Double-Button-1>', delete_class)

        # Frame for the buttons.
        button_frame = tk.Frame(self.preference_frame, background="silver")
        button_frame.pack(padx=5, pady=5, ipadx=10, ipady=10)

        save_changes_button = tk.Button(button_frame, command=lambda: [], text='Save Changes',font=body_font, width=12)
        save_changes_button.pack()

        self.exit_button(button_frame, self.root)

    def create_calendar(self):
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        # Create frames for the days of the week.
        week_frame = tk.Frame(self.root)
        week_frame.pack(side=tk.TOP, fill=tk.X)

        for day_name in days_of_week:
            day_frame = tk.Frame(week_frame)
            day_frame.pack(side=tk.LEFT)

            # Creates the calendar label for each day.
            day_label = tk.Label(day_frame, text=day_name, width=10, height=3, relief=tk.GROOVE, background="lightgray", anchor="nw", padx=5, pady=5)
            day_label.pack(side=tk.TOP)

            # Creates options for each day.
            hour_var = tk.StringVar()
            # Options to choose from. Default value is "".
            formatted_hours = ["", *["{:02d}:00".format(i) for i in range(1, 25)]]
            hours_menu = tk.OptionMenu(day_frame, hour_var, *formatted_hours)

            # Sets the background color and removes borders from the menu.
            hours_menu["highlightthickness"] = 0
            hours_menu.configure(bg="lightgray", borderwidth=0, relief=tk.FLAT)

            hours_menu.place(relx=0.5, rely=0.5, anchor='n')

def main():
    master = tk.Tk()
    app = ParentWindow(master)
    app.load_main()
    master.mainloop()

if __name__ == "__main__":
    main()
