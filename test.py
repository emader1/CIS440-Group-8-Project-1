import tkinter as tk
from datetime import datetime, timedelta

class YourCalendarApp:
    def __init__(self):
        self.root = tk.Tk()
        self.calendar_frame = tk.Frame(self.root)
        self.calendar_frame.pack()

        self.month_label = tk.Label(self.root, text="")
        self.month_label.pack()

        # List to store selected days
        self.selected_days = []

        # Dictionary to store events
        self.events_dict = {}

        self.create_calendar()

        # Entry for custom events
        self.event_entry = tk.Entry(self.root)
        self.event_entry.pack()

        # Button to add custom events to selected days
        self.add_event_button = tk.Button(self.root, text="Add Event", command=self.add_event_to_selected)
        self.add_event_button.pack()

        # Button to save sessions
        self.save_button = tk.Button(self.root, text="Save Sessions", command=self.save_session)
        self.save_button.pack()

    def create_calendar(self):
        def update_calendar():
            for widget in self.calendar_frame.winfo_children():
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
                week_frame = tk.Frame(self.calendar_frame, padx=0, pady=0)
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

    def save_session(self):
        event_name = "Example Event"
        for day_number in self.selected_days:
            date = datetime.now().replace(day=day_number)
            date_str = date.strftime("%Y-%m-%d")

            if date_str in self.events_dict:
                self.events_dict[date_str].append(event_name)
            else:
                self.events_dict[date_str] = [event_name]

        print("Events Dictionary:", self.events_dict)

        self.selected_days = []

    def find_day_box(self, day_number):
        for widget in self.calendar_frame.winfo_children():
            for child_widget in widget.winfo_children():
                try:
                    if int(child_widget.cget("text")) == day_number:
                        return child_widget
                except ValueError:
                    # Handle the case where the text is not a valid integer
                    pass
        return None

# Create an instance of your calendar app
app = YourCalendarApp()

# Start the Tkinter main loop
app.root.mainloop()

