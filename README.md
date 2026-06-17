# VisionLog Analytics

VisionLog Analytics is a log monitoring and analytics system developed for industrial vision inspection environments.

The application automatically monitors log folders, processes rejection logs, stores data in SQLite, and provides dashboards, analytics, filtering, and export tools for production analysis.

---

## Features

### Log Monitoring

* Automatic folder monitoring using Watchdog
* Real-time log detection
* Automatic log parsing
* SQLite database storage

### Dashboard

* Total rejections
* Main defect detection
* Critical camera identification
* Recent logs visualization
* Alarm system
* Manual log validation

### Analytics

* Global defect ranking
* Rejections by camera
* Rejections by date
* Rejections by hour
* Interactive charts

### Logs

* Complete log history
* Filters by:

  * Camera
  * Defect
  * Status
  * Filename
* CSV export

### Settings

* System status
* Database information
* Log folder information
* Language selection
* Portuguese / English support

---

## Technologies

### Backend

* Python
* SQLite
* Watchdog

### Frontend (Stable Version)

* Streamlit
* Plotly
* Pandas

### Experimental Frontend

* Flask
* HTML5
* CSS3
* JavaScript
* Chart.js

---

## Project Structure

```text
Back-End/
│
├── dashboard/
├── database/
├── logs/
├── models/
├── observer/
├── parser/
├── services/
│
├── main.py
├── config.py
├── requirements.txt
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/thlsslvg/VisionLog.git
cd VisionLog
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Environment

Windows:

```bash
.venv\Scripts\activate
```

Linux:

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Application

### Watchdog Service

```bash
python main.py
```

### Dashboard

```bash
streamlit run dashboard/App.py
```

---

## Current Status

### Stable Version

* Streamlit Dashboard
* SQLite Integration
* Watchdog Monitoring
* Analytics
* CSV Export
* Multi-language Support

### Experimental Version

* Flask Frontend
* Custom HTML/CSS Interface
* Modern Dashboard Design

---

## Future Improvements

* Excel Export
* PDF Report Generation
* User Authentication
* Advanced Analytics
* Email Notifications
* Production KPI Reports

---

## Author

Thales Silva

Industrial Vision Analytics Project

2026
