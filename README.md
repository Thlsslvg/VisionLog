# VisionLog

VisionLog is a manufacturing quality monitoring system developed for industrial vision inspection environments.

The project automatically processes inspection logs, stores rejection data in a SQLite database, generates analytics dashboards, and provides monitoring tools for production quality analysis.

---

# Features

## Dashboard

* Total rejections counter
* Main defect identification
* Critical camera identification
* Daily alarm system
* Alarm acknowledgment
* Manual dashboard refresh
* Recent processed logs table
* Log file validation (.txt)

## Analytics

* Global defect ranking
* Rejections by camera
* Rejections by date
* Rejections by hour
* Defect trend by date (multi-line chart)
* Camera trend by date (multi-line chart)

## Logs

* Full rejection database visualization
* Filter by camera
* Filter by defect
* Filter by status
* Search by filename
* Export CSV
* Export Excel

## Settings

* Language selection
* Database status
* Log folder status
* TXT file count
* Database record count
* System paths visualization

---

# Technologies

## Backend

* Python
* Flask
* SQLite

## Frontend

* HTML5
* CSS3
* JavaScript
* Chart.js

## Data Processing

* Pandas
* OpenPyXL

---

# Database

SQLite database:

```text
visionlog.db
```

Main table:

```sql
rejections
```

Stored fields:

```text
id
camera
status
defect
time
filename
created_at
```

---

# Alarm System

The alarm system now operates using only the current day's rejections.

Behavior:

* Alarm threshold: 5 rejections
* Previous day rejections are ignored
* Alarm resets automatically each day
* User can acknowledge current day alarms

---

# Log Validation

Supported format:

```text
Camera: 5
Status: FAIL
Defect: Glue
Time: 16:29
```

Validation checks:

* Required fields
* Format verification
* Content preview

---

# Analytics

Available charts:

### Global Defect Ranking

Displays the most frequent defects.

### Rejections by Camera

Displays rejection distribution by inspection camera.

### Rejections by Date

Displays production rejection evolution.

### Rejections by Hour

Displays rejection distribution by hour.

### Defect Trend by Date

Multi-line chart displaying each defect type over time.

### Camera Trend by Date

Multi-line chart displaying each camera rejection trend.

---

# Export Functions

Supported formats:

* CSV
* XLSX (Excel)

Generated files:

```text
visionlog_logs.csv
visionlog_logs.xlsx
```

---

# Executable Version

The web dashboard can be distributed as a standalone executable using PyInstaller.

Build command:

```bash
pyinstaller --onedir --name VisionLogWeb --add-data "templates;templates" --add-data "static;static" run_web.py
```

Run:

```text
dist/VisionLogWeb/VisionLogWeb.exe
```

The executable launches:

```text
http://127.0.0.1:5000
```

automatically in the default browser.

---

# Current Status

Project status:

✅ Dashboard completed

✅ Analytics completed

✅ Logs completed

✅ Settings completed

✅ CSV export

✅ Excel export

✅ Daily alarm system

✅ Log validation

✅ Flask migration completed

✅ Executable generation completed

✅ Multi-line analytics charts
---

# Author

Thales Silva

Industrial Vision Monitoring Project
