import tkinter as tk
import tkinter.ttk
import mysql.connector
from home_page import HomePage

title_font = ("Arial", 16)
body_font = ("Arial", 12)

class ParentWindow():
    def __init__(self, root):
        self.root = root
        self.root.geometry("600x600")
        self.root.config(background="silver")
        self.feedback_label = tk.Label(root, background='silver')

    def load_main(self):
        login_window = LoginWindow(self.root)
        login_window.load_main()

    def exit_app(self, root):
        root.destroy()

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

        # User's email and password input label.
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

        create_account_button = tk.Button(button_frame, command=lambda: self.create_account(email_var.get(), password_var.get(), fname_var.get(), lname_var.get(), username_var.get()), text='Create Account', font=body_font, width=12)
        create_account_button.pack(padx=5, pady=5)

        login_window_button = tk.Button(button_frame, command=lambda: [self.login_frame.pack(), self.account_frame.pack_forget(), self.feedback_label.pack_forget()], text='Previous', font=body_font, width=12)
        login_window_button.pack(padx=5, pady=5)

        self.exit_button(button_frame, self.root)

        self.account_frame.pack()

    def login(self):
        query = "SELECT * FROM users WHERE email = %s AND password = %s"
        self.cursor.execute(query, (self.email_var.get(), self.password_var.get()))
        user = self.cursor.fetchone()

        if user:
            self.feedback_label.config(text='Login Successful!')
            self.login_frame.pack_forget()
            home_page = HomePage(self.root, self.db_connection, self.cursor)
            home_page.frame.pack()
        else:
            self.feedback_label.config(text='Invalid Email or Password.')


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

    def preference_window(self):
        def add_class():
            selected_item = class_combobox.get()
            if selected_item and selected_item not in class_listbox.get(0, tk.END):
                class_listbox.insert(tk.END, selected_item)

        def delete_class(event):
            selected_index = class_listbox.curselection()
            if selected_index:
                class_listbox.delete(selected_index)

        self.slider_frame = tk.Frame(self.root, borderwidth=2, relief='sunken')
        self.preference_frame = tk.Frame(self.root, borderwidth=2, relief='sunken')

        slider_var = tk.IntVar()
        slider = tk.Scale(self.slider_frame, from_=1, to=12, orient='horizontal', length=160, variable=slider_var)
        slider.pack(side=tk.LEFT, padx=5, pady=5)

        am_pm_var = tk.IntVar()
        am_radio = tk.Radiobutton(self.slider_frame, text='AM', value=0, variable=am_pm_var)
        pm_radio = tk.Radiobutton(self.slider_frame, text='PM', value=1, variable=am_pm_var)

        am_radio.pack(side=tk.LEFT)
        pm_radio.pack(side=tk.LEFT)

        add_button = tk.Button(self.slider_frame, text='Add', command=lambda: [self.button_click(slider_var.get(), am_pm_var.get())])
        add_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.slider_frame.pack(padx=5, pady=5)
        self.feedback_label.pack()

        frame = tk.Frame(self.preference_frame)
        frame.pack(padx=5, pady=5)

        class_list = ['CIS440', 'CIS430']
        class_combobox = tkinter.ttk.Combobox(frame, values=class_list)
        class_combobox.pack(side=tk.LEFT, padx=5, pady=5)

        add_button = tk.Button(frame, text='Add', command=add_class)
        add_button.pack(side=tk.LEFT, padx=5, pady=5)

        class_listbox = tk.Listbox(self.preference_frame, width=50)
        class_listbox.pack(padx=5, pady=5)
        class_listbox.bind('Double-Button-1', delete_class)

        self.preference_frame.pack(padx=5, pady=5)

        self.exit_button(self.root, self.root)

    def button_click(self, time, am_pm):
        am_pm = "AM" if am_pm == 0 else "PM"
        self.feedback_label.config(text=f'Added {time} {am_pm} to your preferred study hours.')

def main():
    master = tk.Tk()
    app = ParentWindow(master)
    app.load_main()
    master.mainloop()

if __name__ == "__main__":
    main()
