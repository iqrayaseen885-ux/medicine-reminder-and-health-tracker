# Contributing

Thank you for helping improve the Medicine Reminder and Health Tracker.

## Getting Started

1. Clone or download the project.
2. Install dependencies with `pip install -r requirements.txt`.
3. Run the app with `streamlit run app.py`.
4. Open the Streamlit URL shown in the terminal.

## Project Structure

- `app.py` contains the Streamlit UI, medicine reminders, health analyzer, charts, and JSON persistence.
- `requirements.txt` lists Python dependencies.
- `data.json` stores medicines and health logs.
- `README.md` explains how to run the app.
- `AGENTS.md` gives coding-agent instructions.
- `USER_MANUAL.md` explains how to use the app.

## Contribution Guidelines

- Keep the project simple and beginner-friendly.
- Store app data in `data.json` unless a database is explicitly requested.
- Keep health guidance cautious and non-diagnostic.
- Preserve the medical safety disclaimer.
- Test changes manually in Streamlit before submitting.

## Manual Testing Checklist

- Start the Streamlit app successfully.
- Add a medicine and confirm it appears in the schedule.
- Confirm real-time due reminders update.
- Mark a medicine as taken.
- Delete a medicine.
- Add a health log and confirm analyzer output updates.
- Confirm wellness score, warnings, and healthy signs display correctly.
- Confirm trend charts render when logs exist.

## Medical Safety

This app is for reminders and simple wellness tracking only. It must not claim to diagnose, treat, or replace professional medical advice.
