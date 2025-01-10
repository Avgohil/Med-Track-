import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import requests
import threading
import time
from plyer import notification
import pygame
from app import app
# import simpleaudio as sa
import datetime

class MedicineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Medicine Tracker")

        # Create tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)

        self.add_medicine_tab = tk.Frame(self.notebook)
        self.view_medicine_tab = tk.Frame(self.notebook)

        self.notebook.add(self.add_medicine_tab, text="Add Medicine")
        self.notebook.add(self.view_medicine_tab, text="View Medicine")

        # Add Medicine tab
        self.add_medicine_frame = tk.Frame(self.add_medicine_tab)
        self.add_medicine_frame.pack(pady=10, padx=10)

        # Labels
        tk.Label(self.add_medicine_frame, text="Medicine Name").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(self.add_medicine_frame, text="Dosage (mg)").grid(row=1, column=0, padx=10, pady=10)
        tk.Label(self.add_medicine_frame, text="Frequency (times/day)").grid(row=2, column=0, padx=10, pady=10)
        tk.Label(self.add_medicine_frame, text="Start Date (YYYY-MM-DD)").grid(row=3, column=0, padx=10, pady=10)
        tk.Label(self.add_medicine_frame, text="End Date (YYYY-MM-DD)").grid(row=4, column=0, padx=10, pady=10)
        tk.Label(self.add_medicine_frame, text="Time (HH:MM)").grid(row=5, column=0, padx=10, pady=10)

        # Entry fields
        self.name_entry = tk.Entry(self.add_medicine_frame)
        self.dosage_entry = tk.Entry(self.add_medicine_frame)
        self.frequency_entry = tk.Entry(self.add_medicine_frame)
        self.start_date_entry = tk.Entry(self.add_medicine_frame)
        self.end_date_entry = tk.Entry(self.add_medicine_frame)
        self.time_entry = tk.Entry(self.add_medicine_frame)

        self.name_entry.grid(row=0, column=1, padx=10, pady=10)
        self.dosage_entry.grid(row=1, column=1, padx=10, pady=10)
        self.frequency_entry.grid(row=2, column=1, padx=10, pady=10)
        self.start_date_entry.grid(row=3, column=1, padx=10, pady=10)
        self.end_date_entry.grid(row=4, column=1, padx=10, pady=10)
        self.time_entry.grid(row=5, column=1, padx=10, pady=10)

        # Add Medicine button
        tk.Button(self.add_medicine_frame, text="Add Medicine", command=self.add_medicine).grid(row=6, column=0, columnspan=2, pady=10)

        # Text area for displaying messages
        self.text_area = tk.Text(self.add_medicine_frame, height=10, width=50)
        self.text_area.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

        # View Medicine tab
        self.view_medicine_frame = tk.Frame(self.view_medicine_tab)
        self.view_medicine_frame.pack(pady=10, padx=10)

        # Text area for displaying medicines
        self.medicines_text_area = tk.Text(self.view_medicine_frame, height=20, width=50)
        self.medicines_text_area.pack(padx=10, pady=10)

        # Refresh button
        tk.Button(self.view_medicine_frame, text="Refresh", command=self.refresh_medicines).pack(pady=10)

    def add_medicine(self):
        # Retrieve data from entry fields
        name = self.name_entry.get().strip()
        dosage = self.dosage_entry.get().strip()
        frequency = self.frequency_entry.get().strip()
        start_date = self.start_date_entry.get().strip()
        end_date = self.end_date_entry.get().strip()
        time_str = self.time_entry.get().strip()

        # Check if any field is empty
        if not name or not dosage or not frequency or not start_date or not end_date or not time_str:
            messagebox.showwarning("Input Error", "All fields are required!")
            return

        # Validate integer inputs
        try:
            dosage = int(dosage)
            frequency = int(frequency)
        except ValueError:
            messagebox.showwarning("Input Error", "Dosage and Frequency must be integers!")
            return

        # Validate date format
        try:
            start_date_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            end_date_obj = datetime.datetime.strptime(end_date, "%Y-%m-%d")
            if start_date_obj > end_date_obj:
                raise ValueError("Start date must be before end date.")
        except ValueError:
            messagebox.showwarning("Input Error", "Dates must be in YYYY-MM-DD format and start date must be before end date!")
            return

        # Validate time format
        try:
            time_obj = datetime.datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            messagebox.showwarning("Input Error", "Time must be in HH:MM format!")
            return

        # Calculate the duration in days
        duration_days = (end_date_obj - start_date_obj).days + 1  # Include the end date

        # Prepare the medicine data
        medicine = {
            'name': name,
            'dosage': dosage,
            'frequency': frequency,
            'start_date': start_date,
            'end_date': end_date,
            'time': time_str
        }

        # Create a new thread for sending the POST request
        threading.Thread(target=self.send_post_request, args=(medicine,)).start()

        # Start notification thread
        threading.Thread(target=self.schedule_notifications, args=(name, time_obj, frequency, duration_days)).start()

    def send_post_request(self, medicine):
        try:
            # Send POST request to the server
            response = requests.post('http://127.0.0.1:5000/medicines', json=medicine)
            self.text_area.delete(1.0, tk.END)
            if response.status_code == 201:
                self.text_area.insert(tk.END, "Medicine added successfully!\n")
            else:
                self.text_area.insert(tk.END, f"Failed to add medicine. Status code: {response.status_code}\n")
        except Exception as e:
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, f"Error adding medicine: {e}\n")

    def schedule_notifications(self, name, time_obj, frequency, duration_days):
        for day in range(duration_days):
            for _ in range(frequency):
                # Calculate the time to notify
                notify_time = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=day), time_obj)
                while datetime.datetime.now() < notify_time:
                    time.sleep(1)  # Wait until the notify time
                self.send_notification(name)

    def send_notification(self, name):
        notification.notify(
            title="Medicine Tracker",
            message=f"It's time to take your: {name}",
            app_name="Medicine Tracker",
            timeout=10
        )
        self.play_notification_tone()  # Play custom notification tone

    def play_notification_tone(self):
        pygame.init()
        pygame.mixer.music.load("E:/OneDrive/Desktop/MedTrack/mixkit-happy-bells-notification-937.wav")
        pygame.mixer.music.play()

    def refresh_medicines(self):
        try:
            response = requests.get('http://127.0.0.1:5000/medicines')
            if response.status_code == 200:
                medicines = response.json()
                self.medicines_text_area.delete(1.0, tk.END)
                for med in medicines:
                    self.medicines_text_area.insert(tk.END, f"Name: {med['name']}, Dosage: {med['dosage']} mg, Frequency: {med['frequency']} times/day, Start Date: {med['start_date']}, End Date: {med['end_date']}, Time: {med['time']}\n")
            else:
                self.medicines_text_area.insert(tk.END, f"Failed to retrieve medicines. Status code:{response.status_code}\n")
        except Exception as e:
            self.medicines_text_area.insert(tk.END, f"Error retrieving medicines: {e}\n")

# Run the Flask server in a separate thread
if __name__ == '__main__':
    import threading
    flask_thread = threading.Thread(target=app.run, kwargs={'debug': False})
    flask_thread.daemon = True
    flask_thread.start()
    root = tk.Tk()
    app = MedicineApp(root)
    root.mainloop()