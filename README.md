Mini Resume Management API

A Django REST Framework-based API for collecting and managing candidate resumes with file upload support. Built on Ubuntu Linux as part of a technical assignment.

Features

- Upload Resumes - Support for PDF, DOC, DOCX, TXT files
- Store Candidate Details - Name, DOB, contact, education, skills
- Auto-Categorization - Automatically categorizes by technology stack
- Filtering - Filter by skill, experience, graduation year
- In-Memory Storage - No database required (uses Django cache)
- Full Validation - Input validation for all fields
- RESTful API - Clean, structured endpoints
- Health Check - Simple endpoint to verify service status

Technology Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.10+ | Core programming language |
| **Django** | 4.2.7 | Web framework |
| **Django REST Framework** | 3.14.0 | API building |
| **Ubuntu** | 22.04 LTS | Development platform |
| **SQLite** | In-memory | Temporary storage (no actual DB) |

Prerequisites

- Ubuntu Linux (20.04/22.04 LTS or newer)
- Python 3.8 or higher
- pip (Python package manager)
- Git

