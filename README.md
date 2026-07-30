# Andromeda Database

A web-based Laboratory Information Management System developed for the **Laboratoire de Physique des 2 Infinis Irène Joliot-Curie (IJCLab)**.

The application replaces spreadsheet-based workflows with a centralized PostgreSQL database for managing TOF-SIMS experiments, laboratory samples, researchers, experimental acquisitions, and associated metadata.

---

## Features

- Laboratory, researcher, and sample management
- TOF-SIMS acquisition tracking, built around a central "hub" linking each run to its sample, primary beam, and spectrometer settings
- Equipment and spectrometer parameter records
- Role-based access: researchers see only their own samples and acquisitions, IT/admin accounts see everything through the Django admin panel
- UI-level confidentiality masking for sensitive researcher/project data
- Web login for researchers (separate from Django admin access)
- File uploads and downloads for proposals, spectra, logs, and experimental data
- Fast client-side search on sample and researcher list pages
- Relational schema designed to preserve links between experiments, samples, and scientific results
- Excel-based data import script (`import_data.py`) for bulk-loading laboratory datasets

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| Backend | Django |
| Database | PostgreSQL (Dockerized) |
| Deployment | Docker Compose |
| Frontend | HTML, Bootstrap 5 |
| Styling | Custom CSS |
| Client-side Interactivity | Vanilla JavaScript |
| Data Ingestion | pandas / openpyxl |

---

## Getting Started

This project runs via Docker Compose. All Django management commands should be run inside the container, not on the host machine.

### Clone the repository

```bash
git clone https://gitlab.in2p3.fr/Web-IJCLab/andromede_database.git
cd andromede_database
```

### Configure environment variables

Copy or create a `.env` file with the database credentials and Django secret key expected by `docker-compose.yml` and `settings.py`. Any value containing a `$` character must be escaped as `$$`.

### Build and start the containers

```bash
docker compose up -d
```

This starts both the PostgreSQL database and the Django web server. A healthcheck ensures the web container waits for the database to be ready before starting.

### Run migrations

```bash
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
```

### Import laboratory data (optional)

If loading from an Excel dataset:

```bash
docker compose exec web python import_data.py
```

### Access the application

```text
http://127.0.0.1:8000/
```

Django admin is available at `/admin/`, and is intended for IT/superuser accounts only. Researcher accounts log in at `/login/` and only have access to the standard web interface.

### Stopping the containers

```bash
docker compose down
```

This stops the containers without deleting data — the database lives in a named Docker volume. Do **not** add the `-v` flag unless you intentionally want to wipe the database.

---

## User Roles

- **Superuser (IT)** — full access via Django admin, unrestricted data visibility.
- **Lab Researchers** — a Django permission group with scoped access to add/view their own samples through the web interface. Researchers do not have Django admin access (`is_staff=False`) and cannot add or manage other researchers' accounts.

New accounts are created manually by IT through the Django admin panel; there is no public self-registration.

---

## Known Limitations / Open Items

- `PreProcessingSpectra` and `Spectra` records are not yet populated — this data is still being compiled by the lab and was not available at the time of writing.
- `Equipment.reflectron_state` is a known modeling gap: per domain-expert feedback, it should describe the acquisition mode (direct vs. reflectron) of an individual spectrum/run, not a fixed property of the equipment itself. This needs a schema change (moving the field, likely to `AcquisitionTOFSIMS` or `SpectrometerParameters`) that has not yet been implemented.
- Metadata export (a single combined file generated from all related tables for a given acquisition) is a planned future feature, scope to be defined later with the lab.

---

## Project Goals

- Replace legacy Excel-based laboratory records
- Improve data consistency and traceability
- Centralize TOF-SIMS experimental metadata
- Provide a scalable foundation for future laboratory workflows

---

## Future Development

Planned improvements include:

- Advanced/technical-parameter search and filtering
- Interactive dashboards
- Metadata export utilities
- Experimental reporting
- REST API for external integrations
- Row-level data scoping (e.g. django-guardian) if finer-grained permissions are needed beyond group-level access

---

## License

This project was developed for **IJCLab** as part of an internship project.