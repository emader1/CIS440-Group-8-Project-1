import tkinter as tk
import tkinter.font as tkfont
import tkinter.ttk as ttk
from datetime import datetime, timedelta

title_font = ("Helvetica", 16)
body_font = ("Helvetica", 12)


class HomePage:
    def __init__(self, root, db_connection, cursor, user_type):
        self.root = root
        self.db_connection = db_connection
        self.cursor = cursor
        self.user_type = user_type

        # Configures the title on each of the pages.
        self.title = tk.Label(self.root, background='silver', text="", font=title_font)
        # Frame for the top left menu icon.
        self.menu_frame = tk.Frame(self.root, borderwidth=2, relief='raised')
        # Frame for all the elements inside the left side menu.
        self.menu_options = tk.Frame(self.root)  # Initialize menu options frame separately.
        # Frame for the calendar on the home page.
        self.calendar_frame = tk.Frame(self.root)
        # Frame for the calendar that allows users to create a new session.
        self.session_calendar_frame = tk.Frame(self.root)
        # List to store the days selected by the user.
        self.selected_days = []
        # Frame that controls the current month and year.
        self.month_label = tk.Label(self.root, background="silver", text="")
        # Frame that controls the session portion of the window.
        self.join_session_frame = tk.Frame(self.root, background='silver')

    def load_main(self):
        # Loads the home page.
        def home(event):
            self.session_calendar_frame.place_forget()
            self.calendar_frame.place(x=100, y=35)
            self.month_label.place(x=255, y=332)
            self.join_session_frame.place(x=92, y=350)
            button_frame.place(x=370, y=350)

        # Loads the account info page.
        def account_info(event):
            self.calendar_frame.place_forget()
            self.month_label.place_forget()
            self.join_session_frame.place_forget()
            button_frame.place_forget()

        # Allows users to create a new session.
        def new_session(event):
            self.calendar_frame.place_forget()
            self.month_label.place_forget()
            self.join_session_frame.place_forget()
            button_frame.place_forget()

            self.session_calendar_frame.place(x=100, y=35)
            self.create_new_calendar()
            self.month_label.place(x=255, y=332)

        # Allows the user to logout.
        def logout(event):
            self.root.destroy()

        def admin_view(event):
            # Function to show admin view
            self.menu_frame.pack_forget()  # Hide the menu frame
            self.calendar_frame.pack_forget()  # Hide the calendar frame
            self.join_session_frame.pack_forget()  # Hide the join session frame

            # Create a new frame to display admin view
            admin_view_frame = tk.Frame(self.root, background="silver")
            admin_view_frame.pack()

            # Retrieve all users from the database
            query = "SELECT * FROM users"
            self.cursor.execute(query)
            users = self.cursor.fetchall()

            # Display user information in a listbox
            user_listbox = tk.Listbox(admin_view_frame, width=100)
            user_listbox.pack(padx=10, pady=10)

            # Add user information to the listbox
            for user in users:
                user_info = f"ID: {user[0]}, Email: {user[1]}, First Name: {user[3]}, Last Name: {user[4]}, Username: {user[5]}, User Type: {user[6]}"
                user_listbox.insert(tk.END, user_info)

            # Add a button to go back to the main page
            back_button = tk.Button(admin_view_frame, text="Back to Home", command=self.load_main, font=body_font)
            back_button.pack(pady=10)

        self.menu_frame = tk.Frame(self.root, background="silver")
        self.menu_frame.pack(side="left", fill="y")

        # The menu icon.
        menu_font = tkfont.Font(size=12)
        menu_icon = tk.Label(self.menu_frame, text="☰", font=menu_font, background="silver", anchor="w")
        menu_icon.pack(fill="x")
        menu_icon.bind("<Button-1>", self.toggle_menu)

        self.menu_options.pack_forget()

        # Menu options.
        home_label = tk.Label(self.menu_options, text='Home', font=menu_font, anchor="w")
        home_label.pack(fill="x")
        home_label.bind("<Button-1>", home)

        account_label = tk.Label(self.menu_options, text='Account', font=menu_font, anchor="w")
        account_label.pack(fill="x")
        account_label.bind("<Button-1>", account_info)

        new_session_label = tk.Label(self.menu_options, text='New Session', font=menu_font, anchor="w")
        new_session_label.pack(fill="x")
        new_session_label.bind("<Button-1>", new_session)

        logout_label = tk.Label(self.menu_options, text='Logout', font=menu_font, anchor="w")
        logout_label.pack(fill="x")
        logout_label.bind("<Button-1>", logout)

        # Add admin view option if the user is an admin
        if self.user_type == 'admin':
            admin_view_label = tk.Label(self.menu_options, text='Admin View', font=menu_font, background="silver",
                                        anchor="w")
            admin_view_label.pack(fill="x")
            admin_view_label.bind("<Button-1>", admin_view)

        self.calendar_frame = tk.Frame(self.root)
        self.month_label = tk.Label(self.root, background="silver", text="", font=menu_font)
        # The month frame is placed, rather than packed so it is centered and not affected by the menu on the left side.
        self.month_label.place(x=220, y=10)

        # The calendar frame is placed, rather than packed so it is centered and not affected by the menu on the left side.
        self.create_calendar()
        self.calendar_frame.place(x=100, y=35)

        # Adds sessions to the listbox.
        def add_session():
            selected_session = session_combobox.get()
            if selected_session:
                session_listbox.insert(tk.END, selected_session)

        # Deletes sessions from the listbox.
        def delete_session(event):
            selected_index = session_listbox.curselection()
            if selected_index:
                session_listbox.delete(selected_index)

        # Function that saves the sessions and adds them to the calendar.
        def save_session():
            print("button to save sessions to the calendar.")

        # Function that resets the listbox and combobox with all of the sessions available.
        def discard_session():
            print("button to reset the listbox and the values in the combobox.")

        self.month_label.place(x=255, y=332)
        self.join_session_frame.place(x=92, y=350)

        # Frame for the listbox entry.
        listbox_frame = tk.Frame(self.join_session_frame, borderwidth=2, relief='sunken')
        listbox_frame.pack(padx=5, pady=5, ipadx=10, ipady=10)

        # Frame for the combobox, as well as the button. Places the button to the right of the combobox.
        combobox_frame = tk.Frame(listbox_frame)
        combobox_frame.pack(padx=5, pady=5)

        # List of sessions.
        session_list = ['Session 1', 'Session 2']
        session_combobox = ttk.Combobox(combobox_frame, values=session_list)
        session_combobox.pack(side=tk.LEFT, padx=5, pady=5)

        add_button = tk.Button(combobox_frame, text='Add', command=add_session)
        add_button.pack(side='left', padx=5, pady=5)

        session_listbox = tk.Listbox(listbox_frame, width=40)
        session_listbox.pack()
        session_listbox.bind('<Double-Button-1>', delete_session)

        button_frame = tk.Frame(self.root, background='silver')
        button_frame.place(x=370, y=350)

        save_button = tk.Button(button_frame, text='Save', font=body_font, width=12, command=save_session)
        save_button.pack(padx=5, pady=5)

        discard_button = tk.Button(button_frame, text='Discard', font=body_font, width=12, command=discard_session)
        discard_button.pack(padx=5, pady=5)

    # Creates and destroys menu on the left side of home screen.
    def toggle_menu(self, event):
        print("Toggle menu called")
        if self.menu_options.winfo_ismapped():
            self.menu_options.pack_forget()
        else:
            self.menu_options.pack(anchor="nw")

    # Creates the calender for the current month.
    def create_calendar(self):
        def update_calendar():
            for widget in self.calendar_frame.winfo_children():
                widget.destroy()

            # Gets the current month and year.
            now = datetime.now()
            current_month = now.month
            current_year = now.year

            # Determine the first day of the month and the number of days in the month.
            first_day_of_month = datetime(current_year, current_month, 1)
            last_day_of_month = datetime(current_year, current_month + 1, 1) - timedelta(days=1)
            num_days_in_month = last_day_of_month.day
            # 0 = Monday, while 6 = Sunday.
            start_day = first_day_of_month.weekday()

            # Create labels for the current month and year.
            self.month_label.config(text=first_day_of_month.strftime("%B %Y"))

            # Create frames to make the calendar.
            for _ in range(5):
                week_frame = tk.Frame(self.calendar_frame, padx=0, pady=0)
                week_frame.pack(side=tk.TOP, fill=tk.X)

                for day in range(7):
                    day_number = (_ * 7) + day - start_day + 1
                    date = datetime(current_year, current_month, day_number) if 1 <= day_number <= num_days_in_month else None

                    # Create a label for each day.
                    # Light pink days are outside the current month. Light blue days are weekends. Light gray days are weekdays.
                    box_color = "lightpink" if date and date.month != current_month else (
                        "lightblue" if date and date.weekday() >= 5 else "lightgray")
                    day_box = tk.Label(week_frame, text=str(day_number) if date else "", width=6, height=3,
                                        relief=tk.GROOVE,
                                        background=box_color, anchor="nw", padx=5, pady=5)
                    day_box.pack(side="left", padx=0, pady=0)

        update_calendar()

    def create_new_calendar(self):
        def update_calendar():
            for widget in self.session_calendar_frame.winfo_children():
                widget.destroy()

            now = datetime.now()
            current_month = now.month
            current_year = now.year

            first_day_of_month = datetime(current_year, current_month, 1)
            last_day_of_month = datetime(current_year, current_month + 1, 1) - timedelta(days=1)
            num_days_in_month = last_day_of_month.day
            start_day = first_day_of_month.weekday()

            self.month_label.config(text=first_day_of_month.strftime("%B %Y"))

            for _ in range(5):
                week_frame = tk.Frame(self.session_calendar_frame, padx=0, pady=0)
                week_frame.pack(side=tk.TOP, fill=tk.X)

                for day in range(7):
                    day_number = (_ * 7) + day - start_day + 1
                    date = datetime(current_year, current_month, day_number) if 1 <= day_number <= num_days_in_month else None

                    box_color = "lightpink" if date and date.month != current_month else (
                        "lightblue" if date and date.weekday() >= 5 else "lightgray")
                    day_box = tk.Label(week_frame, text=str(day_number) if date else "", width=6, height=3,
                                        relief=tk.GROOVE,
                                        background=box_color, anchor="nw", padx=5, pady=5, justify=tk.LEFT)  # Set justify to LEFT

                    day_box.default_color = box_color  # Set the default color
                    day_box.bind("<Button-1>",
                                 lambda event, day_number=day_number: self.toggle_day_selection(event, day_number))

                    day_box.pack(side="left", padx=0, pady=0)

        update_calendar()

    def toggle_day_selection(self, event, day_number):
        day_box = event.widget

        # Toggle the day's selection status
        if day_number in self.selected_days:
            self.selected_days.remove(day_number)
            day_box.config(background=day_box.default_color)
        else:
            self.selected_days.append(day_number)
            day_box.config(background="lightgreen")

    def add_event_to_selected(self):
        event_text = self.event_entry.get()
        if not event_text or not self.selected_days:
            return

        # Add the event to the selected days
        for day_number in self.selected_days:
            day_box = self.find_day_box(day_number)
            if day_box:
                current_text = day_box.cget("text")
                updated_text = f"{day_number}\n{event_text}" if not current_text else f"{current_text}\n{event_text}"
                day_box.config(text=updated_text, background=day_box.default_color)  # Update the label text

        # Reset the list of selected days
        self.selected_days = []

    def find_day_box(self, day_number):
        for widget in self.session_calendar_frame.winfo_children():
            for child_widget in widget.winfo_children():
                try:
                    if int(child_widget.cget("text")) == day_number:
                        return child_widget
                except ValueError:
                    # Handle the case where the text is not a valid integer
                    pass
        return None
