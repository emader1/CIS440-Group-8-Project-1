import tkinter as tk
import mysql.connector
from home_page import HomePage

title_font = ("Arial", 16)
body_font = ("Arial", 12)

class Functions:
    def __init__(self, root):
        self.root = root
        self.feedback_label = tk.Label(root, background='silver')

    def exit_app(self, root):
        root.destroy()

    def exit_button(self, frame, root):
        exit_button = tk.Button(frame, command=lambda: self.exit_app(root), text='Exit', font=body_font, width=12)
        exit_button.pack(padx=5, pady=5)

class ParentWindow(Functions):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.root.geometry("600x600")
        self.root.config(background="silver")

    def load_main(self):
        login_window = LoginWindow(self.root)
        login_window.load_main()

class LoginWindow(ParentWindow):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.frame = tk.Frame(self.root, background="silver")

        # Connect to MySQL database
        self.db_connection = mysql.connector.connect(
            host="107.180.1.16",
            port="3306",
            user="spring2024Cteam8",
            password="spring2024Cteam8",
            database="spring2024Cteam8"
        )
        self.cursor = self.db_connection.cursor()

    def load_main(self):
        label_frame = tk.Frame(self.frame, borderwidth=2, relief='sunken')
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

        button_frame = tk.Frame(self.frame, background="silver")
        button_frame.pack(padx=5, pady=5, ipadx=10, ipady=10)

        self.feedback_label.pack()

        login_button = tk.Button(button_frame, command=self.login, text='Login', font=body_font, width=12)
        login_button.pack(padx=5, pady=5)

        create_account_button = tk.Button(button_frame, command=lambda: [self.frame.pack_forget(), self.account_window()], text='Create Account',
                                        font=body_font, width=12)
        create_account_button.pack(padx=5, pady=5)

        self.exit_button(button_frame, self.root)

        self.frame.pack()

    def account_window(self):
        self.frame2 = tk.Frame(self.root, background="silver")  # Create the frame2 attribute

        label_frame = tk.Frame(self.frame2, borderwidth=2, relief='sunken')
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

        button_frame = tk.Frame(self.frame2, background="silver")  # Changed self.frame to self.frame2
        button_frame.pack(padx=5, pady=5, ipadx=10, ipady=10)

        create_account_button = tk.Button(button_frame, command=lambda: self.create_account(email_var.get(), password_var.get(), fname_var.get(), lname_var.get(), username_var.get()), text='Create Account', font=body_font, width=12)
        create_account_button.pack(padx=5, pady=5)

        login_window_button = tk.Button(button_frame, command=lambda: [self.frame.pack(), self.frame2.pack_forget()], text='Previous', font=body_font, width=12)
        login_window_button.pack(padx=5, pady=5)

        self.exit_button(button_frame, self.root)

        # Pack the frame2 to display it
        self.frame2.pack()

    def login(self):
        query = "SELECT * FROM users WHERE email = %s AND password = %s"
        self.cursor.execute(query, (self.email_var.get(), self.password_var.get()))
        user = self.cursor.fetchone()

        if user:
            self.feedback_label.config(text='Login Successful!')
            self.frame.pack_forget()
            home_page = HomePage(self.root)
            home_page.frame.pack()
        else:
            self.feedback_label.config(text='Invalid Email or Password.')

    def create_account(self, email, password, fname, lname, username):
        query = "SELECT * FROM users WHERE email = %s"
        self.cursor.execute(query, (email,))
        existing_user = self.cursor.fetchone()
        
        if existing_user:
            self.feedback_label.config(text='Email is already linked to an account.')
        else:
            query = "INSERT INTO users (email, password, fname, lname, username) VALUES (%s, %s, %s, %s, %s)"
            self.cursor.execute(query, (email, password, fname, lname, username))
            self.db_connection.commit()
            self.feedback_label.config(text='Success! Account has been created.\nReturn to the home page to login.')

def main():
    master = tk.Tk()
    app = ParentWindow(master)
    app.load_main()
    master.mainloop()

if __name__ == "__main__":
    main()
