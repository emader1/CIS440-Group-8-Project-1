import tkinter as tk
import tkinter.ttk
from datetime import datetime, timedelta
import mysql.connector

title_font = ("Helvetica", 16)
body_font = ("Helvetica", 12)
menu_font = ("Helvetica", 10)

class HomePage:
    def __init__(self, root, db_connection, cursor):
        self.root = root
        self.db_connection = db_connection
        self.cursor = cursor

        # Configures the title on each of the pages.
        self.title = tk.Label(self.root, background='silver', text="", font=title_font)
        # Frame for the top left menu icon.
        self.menu_frame = tk.Frame(self.root, borderwidth=2, relief='raised')
        # Frame for all the elements inside the left side menu.
        self.menu_options = tk.Frame(self.menu_frame)
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

        self.menu_frame.pack(side="left", fill="y")

        # The menu icon.
        menu_icon = tk.Label(self.menu_frame, text="☰", font=menu_font, anchor="w")
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

        self.title.config(text='Home')
        self.title.place(x=265, y=4)
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
        session_combobox = tkinter.ttk.Combobox(combobox_frame, values=session_list)
        session_combobox.pack(side='left', padx=5, pady=5)

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
                    box_color = "lightpink" if date and date.month != current_month else ("lightblue" if date and date.weekday() >= 5 else "lightgray")
                    day_box = tk.Label(week_frame, text=str(day_number) if date else "", width=6, height=3, relief=tk.GROOVE,
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

                    box_color = "lightpink" if date and date.month != current_month else ("lightblue" if date and date.weekday() >= 5 else "lightgray")
                    day_box = tk.Label(week_frame, text=str(day_number) if date else "", width=6, height=3, relief=tk.GROOVE,
                                    background=box_color, anchor="nw", padx=5, pady=5, justify=tk.LEFT)  # Set justify to LEFT

                    day_box.default_color = box_color  # Set the default color
                    day_box.bind("<Button-1>", lambda event, day_number=day_number: self.toggle_day_selection(event, day_number))

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
