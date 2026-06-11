# Medicine Reminder and Health Tracker

## Project Overview

Medicine Reminder and Health Tracker is a Streamlit web app for managing medicine reminders and tracking daily health readings.

The app stores data locally in `data.json` and provides a simple health analyzer for temperature, pulse, blood pressure, blood sugar, BMI, water intake, sleep, and mood.

This project is for wellness tracking only. It is not a medical diagnosis tool.

## Features

- Add medicine name, dosage, reminder time, and notes.
- View real-time medicine due reminders.
- Mark medicines as taken.
- Delete saved medicines.
- Log temperature, pulse, blood pressure, blood sugar, weight, height, water intake, sleep, and mood.
- Calculate BMI automatically.
- Analyze latest health data with wellness score, urgent alerts, warnings, and healthy signs.
- View saved health logs in a table.
- Display health trend charts.
- Save data locally in `data.json`.

## Installation

Install Python 3, then install the required packages:

```bash
pip install -r requirements.txt
```

The required packages are:

- `streamlit`
- `pandas`
- `streamlit-autorefresh`

## How to Run

Start the app with:

```bash
streamlit run app.py
```

Open the Streamlit URL shown in the terminal. It is usually:

```text
http://localhost:8501
```
