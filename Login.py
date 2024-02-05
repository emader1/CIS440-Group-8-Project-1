import tkinter as tk
import tkinter.ttk

class LoginWindow():
    def __init__(self, root):
        self.root = root
        self.root.title("Login Page")
        self.root.geometry('800x600')
        self.root.config(background='silver')

    def load_main(self):
        frame = tk.Frame(self.root, borderwidth=2, relief='sunken')
        frame.pack(padx=5, pady=5, ipadx=10, ipady=10)
        

def main():
    root = tk.Tk()
    app = LoginWindow(root)
    LoginWindow.load_main(app)
    root.mainloop()

if __name__ == "__main__":
    main()