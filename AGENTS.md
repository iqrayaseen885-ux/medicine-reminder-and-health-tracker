# Agent Instructions

This repository is a Streamlit app for medicine reminders and health tracking.

## App Type

- Python Streamlit web app.
- Local JSON persistence through `data.json`.
- Dependencies listed in `requirements.txt`.
- No separate frontend build step.

## Important Files

- `app.py`: Streamlit UI, data loading, form handling, medicine reminders, health analyzer, and charts.
- `requirements.txt`: Python packages required to run the app.
- `data.json`: local data store.
- `README.md`: project overview and setup.
- `CONTRIBUTING.md`: contribution process.
- `USER_MANUAL.md`: instructions for end users.

## Development Guidance

- Prefer Streamlit-native widgets and charts.
- Keep data readable and portable in `data.json`.
- Do not add cloud sync, authentication, or external health APIs unless explicitly requested.
- Preserve the medical safety disclaimer.
- Avoid presenting health output as a diagnosis.

## Testing Guidance

Manual Streamlit testing is expected.

Check these flows after changes:

- `streamlit run app.py` starts the app.
- Medicine form saves to `data.json`.
- Health tracker form saves to `data.json`.
- Analyzer displays the latest health status.
- Trend charts render when logs exist.
- Delete and taken buttons work.

## Safety Notes

This project is not a medical diagnosis tool. Any agent editing this app should preserve that limitation in user-facing text and documentation.
