# Hospital Information System (HIS) - Odoo ERP

**Authors:**  Fanomezana Sarobidy Michelle RAZAFINDRAKOTO & Elie Kokou Mokpokpo ETOVENA  
**Supervised by:** Prof. Samir AMRI  
**Academic Year:** 2025–2026  
**GitHub Repository:** [https://github.com/Fanomezana401/odoo-hospital](https://github.com/Fanomezana401/odoo-hospital)

---

## Table of Contents
- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Security and Access Control](#security-and-access-control)
- [Future Enhancements](#future-enhancements)
- [References](#references)

---

## Project Overview
This project is a **Hospital Information System (HIS)** built using **Odoo ERP** and designed according to the **TOGAF ADM framework**.  
It provides a fully integrated platform to manage patient data, appointments, medical consultations, and invoicing, while ensuring strict access control.

The main objective is to **bridge the gap between clinical operations and administrative workflows** in a hospital environment, providing a secure, modular, and scalable solution.

---

## Architecture
The system follows a **3-tier architecture**:
1. **Presentation Layer:** Odoo XML views (Form, Tree, Calendar)  
2. **Logic Layer:** Python models and controllers managing business rules  
3. **Data Layer:** PostgreSQL database accessed through Odoo ORM

We applied the **TOGAF ADM methodology**:
- **Phase A:** Architecture Vision – Define scope and stakeholders  
- **Phase B:** Business Architecture – Model core hospital processes  
- **Phase C:** Information Systems Architecture – Define data and application models  
- **Phase D:** Technology Architecture – Select Odoo ERP (Python/PostgreSQL)

---

## Features
- Centralized **Electronic Health Record (EHR)**  
- Appointment scheduling with **conflict detection**  
- **Automated billing** based on consultations  
- **Role-Based Access Control (RBAC)** for secure data access  
- Modular design for future extensions (Laboratory, Pharmacy, Reporting)

---

## Project Structure
odoo-hospital/
├── hospital/
│ ├── init.py
│ ├── models/
│ │ ├── init.py
│ │ ├── patient.py
│ │ ├── appointment.py
│ │ └── planning.py
│ ├── views/
│ │ ├── patient_views.xml
│ │ ├── appointment_views.xml
│ │ └── menuitems.xml
│ ├── security/
│ │ ├── ir.model.access.csv
│ │ └── record_rules.xml
│ └── manifest.py
├── README.md
└── requirements.txt

yaml
Copier le code
- **models/**: Python classes defining data models and business logic  
- **views/**: XML files for forms, lists, and menus  
- **security/**: Access control rules and record permissions  
- **__manifest__.py**: Module metadata and dependencies

---

## Installation
1. **Clone the repository**:
```bash
git clone https://github.com/Fanomezana401/odoo-hospital.git
cd odoo-hospital
Install Odoo 17 (or compatible version)

Install Python dependencies:

bash
Copier le code
pip install -r requirements.txt
Start Odoo server:

bash
Copier le code
odoo-bin -c odoo.conf
Activate the module in Odoo Apps

Usage
Log in as Administrator

Create roles and assign permissions (Secretary, Doctor, Manager)

Register patients and schedule appointments

Perform medical consultations and generate invoices

Ensure doctors cannot access unauthorized appointments

Generate reports using the built-in Odoo reporting engine

Security and Access Control
Secretary: Manage appointments and invoices, no access to medical records

Doctor: Access own appointments and patient medical records

Manager: Full system access and configuration rights

Constraints implemented:

Prevent overlapping appointments

Role-based access enforcement

Data privacy and audit logging

Future Enhancements
Laboratory and pharmacy management

Advanced analytics and dashboards

Interoperability with external healthcare systems (HL7, FHIR)

Mobile interface for doctors and nurses

References
TOGAF Standard, 10th Edition

Odoo Official Documentation
