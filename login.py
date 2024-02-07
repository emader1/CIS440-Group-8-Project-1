import tkinter as tk
import json

title_font = ("Arial", 16)
body_font = ("Arial", 12)

class Functions:
    def __init__(self, root):
        self.root = root

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

    def load_main(self):
        label_frame = tk.Frame(self.frame, borderwidth=2, relief='sunken')
        label_frame.pack(padx=5, pady=5, ipadx=10, ipady=10)

        login_label = tk.Label(label_frame, text='Login', font=title_font)
        login_label.pack()

        # User's email and password input label.
        email_label = tk.Label(label_frame, text='Email:', font=body_font)
        email_label.pack(padx=5, pady=5)
        email_var = tk.StringVar()
        email_entry = tk.Entry(label_frame, textvariable=email_var)
        email_entry.pack()

        # User's password label. All inputs show in '*'.
        password_label = tk.Label(label_frame, text='Password:', font=body_font)
        password_label.pack(padx=5, pady=5)
        password_var = tk.StringVar()
        password_entry = tk.Entry(label_frame, show='*', textvariable=password_var)
        password_entry.pack()

        button_frame = tk.Frame(self.frame, background="silver")
        button_frame.pack(padx=5, pady=5, ipadx=10, ipady=10)

        # This label provides feedback to the user across the entire app.
        self.feedback_label.pack()

        login_button = tk.Button(button_frame, command=lambda: [self.login(email_var.get(), password_var.get())], text='Login', font=body_font, width=12)
        login_button.pack(padx=5, pady=5)

        create_account_button = tk.Button(button_frame, command=lambda: [self.account_window()], text='Create Account',
                                        font=body_font, width=12)
        create_account_button.pack(padx=5, pady=5)

        self.exit_button(button_frame, self.root)

        self.frame.pack()

    # Allows users to login.
    def login(self, email, password):
        data = self.load_json_data('users.json')

        if email in data and data[email]["password"] == password:
            self.feedback_label.config(text='Login Successful!')
        else:
            self.feedback_label.config(text='Invalid Email or Password.')

    # Allows users to create accounts.
    def create_account(self, email, password):
        data = self.load_json_data('users.json')
        if email in data:
            self.feedback_label.config(text='Email is already linked to an account.')
        else:
            if "@" in email and (email.endswith(".com") or email.endswith(".org") or email.endswith(".edu")):
                allowed_characters = set("!@#$%^&*()-_=+[]{}|;:'\",.<>/?`~")
                if len(password) >= 6:
                    if all(char.isalnum() or char in allowed_characters for char in password):
                        data[email] = {}
                        data[email]['Password'] = password

                        self.save_json_data('users.json', data)

                        self.feedback_label.config(text='Success! Account has been created.\nReturn to the home page '
                                                        'to '
                                                   'login.')
                    else:
                        self.feedback_label.config(text='Password contains invalid characters.')
                else:
                    self.feedback_label.config(text='Password must be at least 6 characters.')
            else:
                self.feedback_label.config(text='Invalid Email Address.')
    
    def account_window(self):
        self.frame.pack_forget()

        self.frame2 = tk.Frame(self.root, background="silver")

        label_frame = tk.Frame(self.frame2, borderwidth=2, relief='sunken')
        label_frame.pack(padx=5, pady=5, ipadx=10, ipady=10)

        login_label = tk.Label(label_frame, text='Create Account', font=title_font)
        login_label.pack()

        # User's email and password input label.
        email_label = tk.Label(label_frame, text='Email:', font=body_font)
        email_label.pack(padx=5, pady=5)
        email_var = tk.StringVar()
        email_entry = tk.Entry(label_frame, textvariable=email_var)
        email_entry.pack()

        # User's password label. All inputs show in '*'.
        password_label = tk.Label(label_frame, text='Password:', font=body_font)
        password_label.pack(padx=5, pady=5)
        password_var = tk.StringVar()
        password_entry = tk.Entry(label_frame, show='*', textvariable=password_var)
        password_entry.pack()

        # This label provides feedback to the user across the entire app.
        self.feedback_label.pack()

        button_frame = tk.Frame(self.frame2, background="silver")
        button_frame.pack(padx=5, pady=5, ipadx=10, ipady=10)

        create_account_button = tk.Button(button_frame, command=lambda: [self.create_account(email_var.get(), password_var.get())], text='Create Account', font=body_font, width=12)
        create_account_button.pack(padx=5, pady=5)

        login_window_button = tk.Button(button_frame, command=lambda: [self.frame.pack(), self.frame2.pack_forget()], text='Previous', font=body_font, width=12)
        login_window_button.pack(padx=5, pady=5)

        self.exit_button(button_frame, self.root)

        self.frame2.pack()

def main():
    master = tk.Tk()
    app = ParentWindow(master)
    ParentWindow.load_main(app)
    master.mainloop()

if __name__ == "__main__":
    main()
