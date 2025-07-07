# Receipt Parser Web App

This project is a Django-based web application that uses OCR to extract key data from receipts.  
**Status:** Currently under development — more features coming soon!

## Features
- Upload receipt images and PDFs
- Extract vendor, date, total amount, and more
- Manual correction and data editing
- Secure user authentication

## Technologies
- Python, Django, Django REST Framework
- OCR processing libraries

## Getting Started
1. Install dependencies from `requirements.txt`.
2. Create a `.env` file in the project root based on `.env.example`.
3. Run migrations and start the development server.

### Environment Variables
The application reads configuration from environment variables. The most important ones are:

- `SECRET_KEY` – Django secret key
- `DEBUG` – set to `True` to enable debug mode
- `ALLOWED_HOSTS` – comma separated list of allowed hosts
- `CORS_ALLOWED_ORIGINS` – comma separated list of origins for CORS
- `POPPLER_PATH` – path to the `poppler` binaries for PDF processing
- `MEDIA_ROOT` – directory to store uploaded files (optional)
- `DB_NAME` – SQLite database file location (optional)

See `.env.example` for a full example.

---

Thank you for checking out the project! Stay tuned for updates.
