import tkinter as tk
import tkinter.ttk

from functions import Functions

title_font = ("Arial", 16)
body_font = ("Arial", 12)

class LoginFunctions(Functions):
    def __init__(self, root, user):
        super().__init__(root, user)
        self.root = root
        self.user = user

    # Allows users to login.
    def login(self):
        print("Add Code Here.")

    #Allows new users to open the create new account window.
    def create_account(self):
        print("Add Code Here.")

class LoginWindow(LoginFunctions):
    def __init__(self, root, user):
        super().__init__(root, user)

        self.root.title("Login Page")
        self.root.geometry('800x600')
        self.root.config(background='silver')

    def load_main(self):
        frame = tk.Frame(self.root, borderwidth=2, relief='sunken')
        frame.pack(padx=5, pady=5, ipadx=10, ipady=10)

        login_label = tk.Label(frame, text='Login', font=title_font)
        login_label.pack()

        # User's email and password input label.
        email_label = tk.Label(frame, text='Email:', font=body_font)
        email_label.pack(padx=5, pady=5)
        email_var = tk.StringVar()
        email_entry = tk.Entry(frame, textvariable=email_var)
        email_entry.pack()

        password_label = tk.Label(frame, text='Password:', font=body_font)
        password_label.pack(padx=5, pady=5)
        password_var = tk.StringVar()
        password_entry = tk.Entry(frame, show='*', textvariable=password_var)
        password_entry.pack()

        login_button = tk.Button(self.root, command=lambda: [], text='Login', font=body_font, width=12)
        login_button.pack(padx=5, pady=5)

        create_account_button = tk.Button(self.root, command=lambda: [self.create_account], text='Create Account', font=body_font, width=12)
        create_account_button.pack(padx=5, pady=5)

        self.exit(self.root)
        

def main():
    root = tk.Tk()
    app = LoginWindow(root, user=None)
    LoginWindow.load_main(app)
    root.mainloop()

if __name__ == "__main__":
    main()
