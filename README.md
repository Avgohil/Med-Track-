## MedTrack - Medicine Tracker Application

## Description 
MedTrack is a desktop application designed to help users manage their medicine schedules efficiently. Users can:

Add medicines with details such as name, dosage, frequency, start date, end date, and time.
View a list of all added medicines.
Receive desktop notifications and sound alerts when it's time to take their medicine.
The backend is built using Flask (Python), and the frontend uses Tkinter for a simple and intuitive desktop interface.

## Features

## Add Medicine: Users can add medicines with details like name, dosage, frequency, start date, end date, and time.
## View Medicines: Users can view all added medicines in a list.
## Notifications: The application sends desktop notifications and plays a sound when it's time to take the medicine.
## Validation: Input fields are validated to ensure correct data formats (e.g., dates, times, and integers).
## Threading: Notifications and server requests are handled in separate threads to avoid blocking the main application.

## Technologies Used
## Backend: Flask (Python)
## Frontend: Tkinter (Python GUI library)
## Notifications: Plyer (for desktop notifications)
## Sound Alerts: Pygame (for playing notification sounds)
## Data Handling: Python datetime module for scheduling and validation
## Threading: Python threading module for asynchronous tasks
## Data Structures: Dictionary :
## Usage:
The medicine dictionary is created when a user adds a new medicine.
It is sent to the Flask backend via a POST request
## List:
Purpose: Used to store multiple medicines retrieved from the Flask backend.
## Strings:
Usage:
Strings are used for user input fields (e.g., medicine name, dates, and time).
They are also used to display messages in the text_area and medicines_text_area.


## Set-up Instructions

## Step-1 Clone the Repository
git clone https://github.com/your-username/medtrack.git
cd medtrack

# Set-up the Python Environment
# 1.Make sure you have Python installed (version 3.8 or higher recommended).
pip install python
python --version

# 2.Create a virtual environment
python -m venv venv

# 3.Activate the virtual environment
venv\Scripts\activate

# 4.Run the Application
-->start flask server 

python app.py
The application will run locally on
http://127.0.0.1:5000

-->Run Gui

python gui.py


## Project Structure
medtrack/
│
├── app.py                # Flask backend
├── README.md             # Project description (this file)
└──── notification.wav  # Notification sound file


## Usage Instructions
## Add Medicine:

Open the application.
Navigate to the "Add Medicine" tab.
Fill in the medicine details (name, dosage, frequency, start date, end date, and time).
Click the "Add Medicine" button to save the medicine.

## View Medicines:

Navigate to the "View Medicine" tab.
Click the "Refresh" button to load and display all added medicines.
Notifications:

The application will send a desktop notification and play a sound when it's time to take the medicine.


