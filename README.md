# Medicine Reminder and Health Tracker

## Overview

Medicine Reminder and Health Tracker is a Streamlit-based application that helps users manage medicine schedules and monitor daily health metrics from one local dashboard.

The app is designed for simple personal wellness tracking. It stores information in `data.json`, refreshes the dashboard in real time, and gives non-diagnostic health guidance based on common reference ranges.

## Features

- Add medicine reminders with name, dosage, time, and notes.
- Show real-time due medicine alerts.
- Play a voice reminder with the medicine name and dosage when a medicine is due.
- Mark medicines as taken for the current day.
- Delete medicines that are no longer needed.
- Track temperature, pulse, blood pressure, and blood sugar.
- Track weight, BMI, water intake, sleep, and mood.
- Calculate BMI automatically from height and weight.
- Show a health analyzer dashboard with wellness score, urgent alerts, warnings, and healthy signs.
- Visualize health trends with Streamlit charts.
- Use the AI Health Checker for general, non-diagnostic health guidance.
- Choose local AI inference with Ollama or BYOK with your own OpenAI API key/tokens.
- Store data locally in JSON format.

## Technology Stack

- Python 3.12
- Streamlit
- Pandas
- Streamlit Auto Refresh
- Ollama-compatible local inference through HTTP
- OpenAI BYOK support
- JSON file storage

## Project Structure

```text
app.py
data.json
requirements.txt
README.md
CONTRIBUTING.md
USER_MANUAL.md
AGENTS.md
CHANGELOG.md
LICENSE
.gitlab-ci.yml
.pre-commit-config.yaml
.specify/
specs/
```

## Installation

Install Python 3.12, then install the required packages:

```bash
pip install -r requirements.txt
```

Optional developer tools can be installed with:

```bash
pip install pre-commit ruff black mypy bandit vulture pyupgrade
pre-commit install
```

## How to Run

Start the app with:

```bash
streamlit run app.py
```

Open the Streamlit URL shown in the terminal. It is usually:

```text
http://localhost:8501
```

## Usage

1. Open the **Medicine Reminder** tab.
2. Add medicine details and reminder time.
3. Watch the top alert area for due medicines.
4. Mark medicines as taken after use.
5. Open the **Health Tracker** tab to save daily readings.
6. Open the **Health Analyzer** tab to review score, warnings, healthy signs, logs, and trend charts.
7. Open the **AI Health Checker** tab for AI-powered general guidance.

## AI Settings

Use the sidebar to choose the AI mode:

- **Local AI - Ollama**: runs inference locally through Ollama at `http://localhost:11434`. Start it with `ollama run llama3` before using the checker.
- **BYOK - OpenAI API Key / Tokens**: lets users bring their own OpenAI credential. The key is entered in the sidebar password field and is not saved to `data.json`.

AI guidance is general information only. It must not be treated as a diagnosis.

## Data Storage

All app data is saved locally in `data.json`.

Deleting `data.json` clears saved medicines and health logs. The app recreates the file when it starts again.

## Quality and Security

This project includes:

- GitLab CI checks for linting, formatting, type checking, tests, coverage, and security.
- Pre-commit hooks for Ruff, Black, mypy, Bandit, pyupgrade, Vulture, YAML checks, JSON checks, and whitespace cleanup.
- AGPLv3 license text in `LICENSE`.

## Medical Disclaimer

This app provides reminders and simple wellness guidance only. It does not diagnose, treat, or replace professional medical advice. For urgent symptoms or concerning readings, contact a qualified healthcare professional.
