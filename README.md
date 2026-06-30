# Andromeda Database - IJCLab

Andromeda is a customized, web-based laboratory information management system (LIMS) engineered for the Laboratoire de Physique des 2 Infinis Irène Joliot-Curie (IJCLab). 

It is designed to modernize and digitize the tracking of TOF-SIMS research data, physical samples, user access, and laboratory equipment, replacing legacy flat-file Excel tracking with a fully normalized relational database architecture.

## 🚀 System Architecture
* **Backend Framework:** Django 4.x (Python)
* **Database:** PostgreSQL 14+ 
* **Frontend:** Server-side rendered HTML with Bootstrap 5 and custom institutional CSS.
* **Interactivity:** Vanilla JavaScript for zero-latency client-side data filtering.

## 🚀 Current Features
* **Normalized Relational Schema:** Data is structured around a central Acquisition "Hub", separating static equipment parameters from dynamic experimental runs to ensure strict data integrity.
* **Instant Search Filtering:** Administrative lists (Samples, Users) feature real-time, JavaScript-powered search bars that filter thousands of records instantly without server reloading.
* **UI/UX Design:** Implements a clean, high-contrast, academic interface with optimized typography (Inter), sticky-header data tables, and tactile form controls.
* **Automated Data Pipeline:** Includes customized Python ingestion scripts (`import_data.py`) to safely parse, clean, and migrate historical laboratory data from legacy spreadsheets into the new PostgreSQL schema.

## 🚀 Local Development Setup

**1. Clone the Repository**
```bash
git clone [https://gitlab.in2p3.fr/Web-IJCLab/andromede_database.git](https://gitlab.in2p3.fr/Web-IJCLab/andromede_database.git)
cd andromede_database