import tkinter as tk
from datetime import datetime, timedelta
import mysql.connector

title_font = ("Helvetica", 16)
body_font = ("Helvetica", 12)

class HomePage:
    def __init__(self, root, db_connection, cursor):
        self.root = root
        self.db_connection = db_connection
        self.cursor = cursor

    def load_main(self):
        self.menu_frame = tk.Frame(self.root, background="silver")
        self.menu_frame.pack(side="left", fill="y")

        # The menu icon.
        menu_icon = tk.Label(self.menu_frame, text="☰", font=body_font, padx=5, pady=5, background="silver", anchor="w")
        menu_icon.pack(fill="x")
        menu_icon.bind("<Button-1>", self.toggle_menu)

        self.menu_options = tk.Frame(self.menu_frame, background="silver")
        self.menu_options.pack_forget()

        # Menu options.
        options = ["Option 1", "Option 2", "Option 3"]
        for option_text in options:
            option_label = tk.Label(self.menu_options, text=option_text, font=body_font, background="silver")
            option_label.pack(fill="x")

        self.calendar_frame = tk.Frame(self.root)

        self.month_label = tk.Label(self.root, background="silver", text="", font=title_font)
        # The month frame is placed, rather than packed so it is centered and not effected by the menu on the left side.
        self.month_label.place(x=220, y=10)

        # The calendar frame is placed, rather than packed so it is centered and not effected by the menu on the left side.
        self.create_calendar()
        self.calendar_frame.place(x=100, y=45)

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
                    day_box.pack(side=tk.LEFT, padx=0, pady=0)

        update_calendar()
