import requests
from openai import OpenAI
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh


DATA_FILE = Path("data.json")
APP_TIMEZONE = timezone(timedelta(hours=5, minutes=30), name="IST")


def default_data():
    return {
        "medicines": [],
        "health_logs": [],
    }


def load_data():
    if not DATA_FILE.exists():
        save_data(default_data())
        return default_data()

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        data = default_data()

    data.setdefault("medicines", [])
    data.setdefault("health_logs", [])
    return data


def save_data(data):
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def play_voice_reminder(message, component_key):
    safe_message = json.dumps(message)
    safe_component_key = json.dumps(component_key)
    components.html(
        f"""
        <div data-reminder-key={safe_component_key}></div>
        <script>
        const reminderMessage = {safe_message};

        function playReminder() {{
            try {{
                const audioContext = new (window.AudioContext || window.webkitAudioContext)();
                const oscillator = audioContext.createOscillator();
                const gainNode = audioContext.createGain();

                oscillator.type = "sine";
                oscillator.frequency.setValueAtTime(880, audioContext.currentTime);
                gainNode.gain.setValueAtTime(0.08, audioContext.currentTime);
                oscillator.connect(gainNode);
                gainNode.connect(audioContext.destination);
                oscillator.start();
                oscillator.stop(audioContext.currentTime + 0.35);
            }} catch (error) {{
                console.warn("Audio beep could not be played.", error);
            }}

            if ("speechSynthesis" in window) {{
                window.speechSynthesis.cancel();
                const utterance = new SpeechSynthesisUtterance(reminderMessage);
                utterance.rate = 0.9;
                utterance.pitch = 1;
                window.speechSynthesis.speak(utterance);
            }}
        }}

        playReminder();
        </script>
        """,
        height=0,
    )


def ask_ollama(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False,
            },
            timeout=60,
        )
        return response.json().get("response", "No response from Ollama.")
    except Exception:
        return "Ollama is not running. Please run: ollama run llama3"


def ask_openai(prompt, api_key):
    try:
        client = OpenAI(api_key=api_key.strip())
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a safe health assistant. Give general guidance only. Do not diagnose. Always suggest consulting a doctor for serious symptoms.",
                },
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"


def number_status(value, low, high):
    if value == 0:
        return "Not entered"
    if value < low:
        return "Low"
    if value > high:
        return "High"
    return "Normal"


def bp_status(systolic, diastolic):
    if systolic == 0 or diastolic == 0:
        return "Not entered"
    if systolic >= 180 or diastolic >= 120:
        return "Crisis"
    if systolic >= 140 or diastolic >= 90:
        return "High"
    if systolic < 90 or diastolic < 60:
        return "Low"
    return "Normal"


def calculate_bmi(weight, height_cm):
    if weight <= 0 or height_cm <= 0:
        return 0
    height_m = height_cm / 100
    return round(weight / (height_m * height_m), 1)


def bmi_status(bmi):
    if bmi == 0:
        return "Not entered"
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Normal"
    if bmi < 30:
        return "Overweight"
    return "Obese"


def analyze_health(log):
    warnings = []
    positives = []
    urgent = []

    temperature = float(log.get("temperature", 0) or 0)
    pulse = int(log.get("pulse", 0) or 0)
    systolic = int(log.get("systolic", 0) or 0)
    diastolic = int(log.get("diastolic", 0) or 0)
    sugar = int(log.get("sugar", 0) or 0)
    water = float(log.get("water", 0) or 0)
    sleep = float(log.get("sleep", 0) or 0)
    bmi = float(log.get("bmi", 0) or 0)

    if temperature >= 39.4:
        urgent.append("High fever range. Contact a healthcare professional promptly.")
    elif temperature >= 38:
        warnings.append("Fever range. Rest, fluids, and monitoring are recommended.")
    elif temperature:
        positives.append("Temperature is within a typical adult range.")

    if pulse and (pulse < 50 or pulse > 120):
        warnings.append("Pulse is outside a common resting range.")
    elif pulse:
        positives.append("Pulse looks within a common resting range.")

    pressure_status = bp_status(systolic, diastolic)
    if pressure_status == "Crisis":
        urgent.append("Blood pressure is in a crisis range. Seek urgent medical help.")
    elif pressure_status in {"High", "Low"}:
        warnings.append(f"Blood pressure is {pressure_status.lower()}. Recheck and consider medical guidance.")
    elif pressure_status == "Normal":
        positives.append("Blood pressure is in a common adult target range.")

    sugar_range = number_status(sugar, 70, 140)
    if sugar_range == "High":
        warnings.append("Blood sugar is above the simple reference range used by this app.")
    elif sugar_range == "Low":
        warnings.append("Blood sugar is below the simple reference range used by this app.")
    elif sugar_range == "Normal":
        positives.append("Blood sugar is within the simple reference range.")

    if water and water < 2:
        warnings.append("Water intake is low for the day.")
    elif water:
        positives.append("Water intake looks good.")

    if sleep and sleep < 6:
        warnings.append("Sleep is below a common recommended minimum.")
    elif sleep:
        positives.append("Sleep duration looks healthy.")

    body_status = bmi_status(bmi)
    if body_status in {"Underweight", "Overweight", "Obese"}:
        warnings.append(f"BMI category is {body_status.lower()}. Use this as a screening clue, not a diagnosis.")
    elif body_status == "Normal":
        positives.append("BMI is in the normal category.")

    score = max(0, 100 - len(warnings) * 12 - len(urgent) * 25)
    return {
        "score": score,
        "urgent": urgent,
        "warnings": warnings,
        "positives": positives,
    }


def medicine_status(medicine, current_time, today):
    taken_date = medicine.get("taken_date", "")
    med_time = medicine.get("time", "")

    if taken_date == today:
        return "Taken"
    if med_time == current_time:
        return "Due now"
    if med_time and med_time < current_time:
        return "Overdue"
    return "Upcoming"


st.set_page_config(
    page_title="Medicine Reminder and Health Tracker",
    page_icon="M",
    layout="wide",
)

st.sidebar.header("AI Settings")

ai_mode = st.sidebar.selectbox(
    "Choose AI Mode",
    ["Local AI - Ollama", "BYOK - OpenAI API Key / Tokens"],
)

st.sidebar.caption(
    "Use local inference with Ollama, or bring your own OpenAI API key/tokens."
)

api_key = ""

if ai_mode == "BYOK - OpenAI API Key / Tokens":
    api_key = st.sidebar.text_input(
        "Enter your OpenAI API Key / Token",
        type="password",
    )

st_autorefresh(interval=30000, key="real_time_refresh")

data = load_data()
now = datetime.now(APP_TIMEZONE)
current_time = now.strftime("%H:%M")
today = now.strftime("%Y-%m-%d")
default_reminder_time = now.replace(second=0, microsecond=0).time()

st.markdown(
    """
    <style>
    .main-title {
        font-size: 40px;
        font-weight: 800;
        color: #1f2937;
    }
    .subtitle {
        font-size: 17px;
        color: #6b7280;
        margin-bottom: 24px;
    }
    .notice {
        padding: 14px;
        border-radius: 8px;
        border: 1px solid #dbe3dd;
        background: #f8fafc;
        margin-bottom: 12px;
    }
    .danger {
        background: #fee2e2;
        color: #991b1b;
        border-color: #fecaca;
        font-weight: 700;
    }
    .success {
        background: #dcfce7;
        color: #166534;
        border-color: #bbf7d0;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">Medicine Reminder and Health Tracker</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Real-time medicine reminders, health logs, and analyzer dashboard</div>',
    unsafe_allow_html=True,
)

metric_1, metric_2, metric_3, metric_4 = st.columns(4)
metric_1.metric("Live Time (IST)", now.strftime("%I:%M:%S %p"))
metric_2.metric("Today", today)
metric_3.metric("Medicines", len(data["medicines"]))
metric_4.metric("Health Logs", len(data["health_logs"]))

due_medicines = [
    medicine
    for medicine in data["medicines"]
    if medicine_status(medicine, current_time, today) == "Due now"
]

if due_medicines:
    reminder_parts = []
    for medicine in due_medicines:
        med_name = medicine.get("name", "Medicine")
        dosage = medicine.get("dosage", "")
        reminder_parts.append(f"{med_name}, {dosage}".strip(", "))
        st.markdown(
            f'<div class="notice danger">Due now: {med_name} - {dosage}</div>',
            unsafe_allow_html=True,
        )

    reminder_text = f"Medicine reminder. It is time to take {'; '.join(reminder_parts)}."
    due_reminder_key = f"{today}_{current_time}_{'|'.join(reminder_parts)}"

    if st.session_state.get("last_spoken_due_reminder") != due_reminder_key:
        st.session_state["last_spoken_due_reminder"] = due_reminder_key
        play_voice_reminder(reminder_text, f"auto_voice_{due_reminder_key}")

    if st.button("Play reminder voice"):
        play_voice_reminder(reminder_text, f"manual_voice_{now.strftime('%H%M%S')}")
else:
    st.markdown('<div class="notice success">No medicine due at this exact minute.</div>', unsafe_allow_html=True)

tab_medicine, tab_health, tab_dashboard, tab_ai_checker = st.tabs(
    ["Medicine Reminder", "Health Tracker", "Health Analyzer", "AI Health Checker"]
)

with tab_medicine:
    st.header("Medicine Reminder")

    with st.form("medicine_form", clear_on_submit=True):
        med_name = st.text_input("Medicine Name")
        dosage = st.text_input("Dosage", placeholder="Example: 1 tablet after food")
        reminder_time = st.time_input(
            "Reminder Time (IST)",
            value=default_reminder_time,
            step=timedelta(minutes=1),
        )
        notes = st.text_area("Notes", placeholder="Example: Take after breakfast")
        submitted = st.form_submit_button("Add Medicine")

    if submitted:
        if not med_name.strip():
            st.error("Please enter medicine name.")
        else:
            data["medicines"].append(
                {
                    "name": med_name.strip(),
                    "dosage": dosage.strip(),
                    "time": str(reminder_time)[:5],
                    "notes": notes.strip(),
                    "taken_date": "",
                    "created_at": now.strftime("%Y-%m-%d %H:%M:%S"),
                }
            )
            save_data(data)
            st.success("Medicine reminder added successfully.")
            st.rerun()

    st.subheader("Saved Medicines")

    if data["medicines"]:
        medicine_rows = []
        for index, medicine in enumerate(data["medicines"]):
            medicine_rows.append(
                {
                    "No": index + 1,
                    "Name": medicine.get("name", ""),
                    "Dosage": medicine.get("dosage", ""),
                    "Time": medicine.get("time", ""),
                    "Notes": medicine.get("notes", ""),
                    "Status": medicine_status(medicine, current_time, today),
                }
            )
        st.dataframe(pd.DataFrame(medicine_rows), use_container_width=True, hide_index=True)

        for index, medicine in enumerate(data["medicines"]):
            col_a, col_b, col_c = st.columns([3, 1, 1])
            col_a.write(f'{medicine.get("time", "")} - {medicine.get("name", "")}')
            if col_b.button("Taken", key=f"taken_{index}"):
                data["medicines"][index]["taken_date"] = today
                save_data(data)
                st.rerun()
            if col_c.button("Delete", key=f"delete_med_{index}"):
                data["medicines"].pop(index)
                save_data(data)
                st.rerun()
    else:
        st.info("No medicines added yet.")

with tab_health:
    st.header("Daily Health Tracker")

    with st.form("health_form"):
        col_1, col_2 = st.columns(2)
        with col_1:
            temperature = st.number_input("Temperature (C)", min_value=0.0, max_value=45.0, step=0.1)
            pulse = st.number_input("Pulse (bpm)", min_value=0, max_value=220)
            systolic = st.number_input("BP Systolic", min_value=0, max_value=260)
            diastolic = st.number_input("BP Diastolic", min_value=0, max_value=180)
        with col_2:
            weight = st.number_input("Weight (kg)", min_value=0.0, max_value=350.0, step=0.1)
            height = st.number_input("Height (cm)", min_value=0.0, max_value=250.0, step=0.1)
            water = st.number_input("Water Intake (litres)", min_value=0.0, max_value=20.0, step=0.1)
            sleep = st.number_input("Sleep Hours", min_value=0.0, max_value=24.0, step=0.5)

        sugar = st.number_input("Blood Sugar (mg/dL)", min_value=0, max_value=600)
        mood = st.selectbox("Mood", ["Good", "Okay", "Tired", "Stressed", "Unwell"])
        save_log = st.form_submit_button("Save Health Log")

    if save_log:
        bmi = calculate_bmi(weight, height)
        log = {
            "date": today,
            "time": now.strftime("%H:%M:%S"),
            "temperature": temperature,
            "pulse": pulse,
            "weight": weight,
            "height": height,
            "bmi": bmi,
            "bmi_status": bmi_status(bmi),
            "water": water,
            "sleep": sleep,
            "systolic": systolic,
            "diastolic": diastolic,
            "bp_status": bp_status(systolic, diastolic),
            "sugar": sugar,
            "sugar_status": number_status(sugar, 70, 140),
            "mood": mood,
        }
        data["health_logs"].append(log)
        save_data(data)
        st.success("Health log saved successfully.")
        st.rerun()

    st.info("Reference ranges are simplified. This app is not a medical diagnosis tool.")

with tab_dashboard:
    st.header("Health Analyzer")

    if data["health_logs"]:
        df = pd.DataFrame(data["health_logs"])
        latest = data["health_logs"][-1]
        analysis = analyze_health(latest)

        score_col, bp_col, bmi_col, sugar_col = st.columns(4)
        score_col.metric("Wellness Score", f'{analysis["score"]}/100')
        bp_col.metric("BP Status", latest.get("bp_status", "N/A"))
        bmi_col.metric("BMI", f'{latest.get("bmi", 0)} ({latest.get("bmi_status", "N/A")})')
        sugar_col.metric("Sugar Status", latest.get("sugar_status", "N/A"))

        if analysis["urgent"]:
            st.error("Urgent attention suggested")
            for item in analysis["urgent"]:
                st.write(f"- {item}")

        if analysis["warnings"]:
            st.warning("Health warnings")
            for item in analysis["warnings"]:
                st.write(f"- {item}")

        if analysis["positives"]:
            st.success("Healthy signs")
            for item in analysis["positives"]:
                st.write(f"- {item}")

        st.subheader("Health Logs")
        st.dataframe(df, use_container_width=True, hide_index=True)

        chart_columns = [
            column
            for column in ["temperature", "pulse", "weight", "bmi", "water", "sleep", "sugar", "systolic", "diastolic"]
            if column in df.columns
        ]
        if chart_columns:
            st.subheader("Health Trends")
            st.line_chart(df[chart_columns])

        if st.button("Clear Health Logs"):
            data["health_logs"] = []
            save_data(data)
            st.rerun()
    else:
        st.info("No health logs added yet. Add one in the Health Tracker tab.")

with tab_ai_checker:
    st.header("🤖 AI Health Checker")

    st.warning(
        "This gives general health guidance only. It is not a replacement for a doctor."
    )

    age = st.number_input("Age", min_value=1, max_value=120, value=20)

    symptoms = st.text_area(
        "Enter your symptoms",
        placeholder="Example: fever, cough, headache for 2 days",
    )

    if st.button("Check Health"):
        if not symptoms.strip():
            st.error("Please enter your symptoms.")
        else:
            st.session_state["ai_health_answer"] = ""
            prompt = f"""
            Age: {age}
            Symptoms: {symptoms}

            Give:
            1. Possible general reasons
            2. Basic care tips
            3. Warning signs
            4. When to consult a doctor

            Do not give a final diagnosis.
            """

            with st.spinner("AI is checking..."):
                if ai_mode == "Local AI - Ollama":
                    answer = ask_ollama(prompt)
                else:
                    if not api_key:
                        answer = "Please enter your OpenAI API key in the sidebar."
                    else:
                        answer = ask_openai(prompt, api_key)

            st.session_state["ai_health_answer"] = answer

    if st.session_state.get("ai_health_answer"):
        st.subheader("AI Health Guidance")
        answer = st.session_state["ai_health_answer"]
        if answer.startswith("Error:") or answer.startswith("Please enter"):
            st.error(answer)
        else:
            st.write(answer)

st.caption(
    "This app provides reminders and simple wellness guidance only. It does not diagnose, treat, or replace medical advice."
)
