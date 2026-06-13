# User Manual

## Overview

Medicine Reminder and Health Tracker helps you manage medicine schedules, log health readings, and review simple health analysis.

The app saves information in a local `data.json` file.

The app also includes an AI Health Checker for general guidance. It can use local AI inference with Ollama or BYOK with your own OpenAI API key/tokens.

## Start the App

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the app:

```bash
streamlit run app.py
```

3. Open the Streamlit URL shown in the terminal, usually:

```text
http://localhost:8501
```

## Medicine Reminder

1. Open the **Medicine Reminder** tab.
2. Enter the medicine name.
3. Enter the dosage.
4. Choose the reminder time.
5. Add optional notes.
6. Select **Add Medicine**.

When the current time matches a medicine time, the app shows a due reminder.

The app can also play a voice reminder with the medicine name and dosage. If your browser blocks automatic audio, select **Play reminder voice**.

You can also mark a medicine as **Taken** or delete it.

## Health Tracker

Open the **Health Tracker** tab and enter any of these values:

- Temperature in Celsius.
- Pulse in beats per minute.
- Blood pressure.
- Weight and height.
- Water intake.
- Sleep hours.
- Blood sugar.
- Mood.

Select **Save Health Log** to store the reading.

## Health Analyzer

Open the **Health Analyzer** tab to see:

- Wellness score.
- Blood pressure status.
- BMI and BMI category.
- Blood sugar status.
- Urgent alerts.
- Health warnings.
- Healthy signs.
- Health log table.
- Trend charts.

## AI Health Checker

Use the sidebar **AI Settings** area to choose an AI mode:

- **Local AI - Ollama**: start Ollama first with `ollama run llama3`.
- **BYOK - OpenAI API Key / Tokens**: enter your own OpenAI credential in the sidebar password field.

Open the **AI Health Checker** tab, enter your age and symptoms, then select **Check Health**.

The AI response gives general possible reasons, basic care tips, warning signs, and when to consult a doctor. It does not provide a final diagnosis.

## Data Storage

Data is stored in `data.json` on this computer. Deleting or editing that file changes the saved app data.

## Medical Disclaimer

This app is for reminders and simple wellness tracking only. For severe symptoms, concerning readings, or medical questions, contact a qualified healthcare professional.
