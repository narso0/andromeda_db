````md
# Andromeda Database

A web-based Laboratory Information Management System (LIMS) developed for the **Laboratoire de Physique des 2 Infinis Irène Joliot-Curie (IJCLab)**.

The application replaces spreadsheet-based workflows with a centralized PostgreSQL database for managing TOF-SIMS experiments, laboratory samples, researchers, experimental acquisitions, and associated metadata.

---

## Features

- Laboratory and researcher management
- Sample registration and tracking
- TOF-SIMS acquisition management
- Equipment and spectrometer parameter records
- File uploads for proposals, spectra, logs, and experimental data
- Fast client-side search for laboratory records
- Relational database designed to preserve links between experiments, samples, and scientific results

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| Backend | Django |
| Database | PostgreSQL |
| Frontend | HTML, Bootstrap 5 |
| Styling | Custom CSS |
| Client-side Interactivity | Vanilla JavaScript |

---

## Getting Started

### Clone the repository

```bash
git clone https://gitlab.in2p3.fr/Web-IJCLab/andromede_database.git
cd andromede_database
```

### Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Linux / macOS**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure the database

Create a PostgreSQL database and update the database connection settings in `settings.py`.

### Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Start the development server

```bash
python manage.py runserver
```

The application will be available at:

```text
http://127.0.0.1:8000/
```

---

## Project Goals

- Replace legacy Excel-based laboratory records
- Improve data consistency and traceability
- Centralize TOF-SIMS experimental metadata
- Provide a scalable foundation for future laboratory workflows

---

## Future Development

Planned improvements include:

- Authentication and role-based permissions
- Advanced filtering and search
- Interactive dashboards
- Data import/export utilities
- Experimental reporting
- REST API for external integrations

---

## License

This project was developed for **IJCLab** as part of an internship project.
````
