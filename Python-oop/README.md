# Patient Management System

A modern web-based patient management system built with Python OOP principles and Flask.

## Features

- **Add Patients**: Create new patient records with full details
- **View Patients**: Display all patients in a responsive table
- **Edit Patients**: Update patient information through a modal interface
- **Delete Patients**: Remove patient records with confirmation
- **Modern UI**: Beautiful, responsive interface with Bootstrap 5
- **Real-time Updates**: Dynamic content updates without page refresh

## Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Storage**: In-memory storage (no database setup required)
- **Architecture**: RESTful API with OOP principles

## How to Run

### Prerequisites
- Python 3.7 or higher
- Virtual environment (recommended)

### Installation

1. **Activate your virtual environment:**
   ```bash
   # On Windows
   .venv\Scripts\activate
   
   # On macOS/Linux
   source .venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install Flask==2.3.3
   ```

3. **Run the application:**
   ```bash
   python web_app.py
   ```

4. **Access the application:**
   Open your web browser and navigate to: `http://localhost:5000`

## Application Structure

```
Python-oop/
├── web_app.py          # Main Flask application
├── templates/
│   └── index.html      # Frontend interface
├── models.py           # Original OOP Patient model
├── db.py              # Database connection (PostgreSQL)
├── main.py            # Original CLI application
└── requirements.txt   # Python dependencies
```

## API Endpoints

- `GET /` - Main application interface
- `GET /api/patients` - Get all patients
- `POST /api/patients` - Create a new patient
- `GET /api/patients/<id>` - Get a specific patient
- `PUT /api/patients/<id>` - Update a patient
- `DELETE /api/patients/<id>` - Delete a patient

## Patient Data Model

Each patient record contains:
- **ID**: Unique identifier (auto-generated)
- **First Name**: Patient's first name
- **Last Name**: Patient's last name
- **Date of Birth**: Patient's birth date
- **Gender**: Male, Female, or Other
- **Contact Number**: Phone number

## Features in Action

1. **Adding a Patient**: Fill out the form at the top of the page and click "Save Patient"
2. **Viewing Patients**: All patients are displayed in the table below the form
3. **Editing a Patient**: Click the edit button (pencil icon) next to any patient
4. **Deleting a Patient**: Click the delete button (trash icon) and confirm the action
5. **Refreshing Data**: Click the "Refresh" button to reload patient data

## Original Application

The original `main.py` file demonstrates the OOP Patient class with PostgreSQL database operations. The web interface provides the same functionality but with a user-friendly frontend and in-memory storage for easy setup.

## Screenshots

The application features:
- Gradient background with modern card-based design
- Responsive layout that works on all devices
- Interactive hover effects and animations
- Color-coded gender badges
- Professional medical-themed styling
- Real-time form validation
- Success/error notifications

## Development

To modify the application:
1. Edit `web_app.py` for backend changes
2. Edit `templates/index.html` for frontend changes
3. The application will automatically reload when you save changes (debug mode enabled)

## Troubleshooting

- **Port already in use**: Change the port in `web_app.py` (line 95)
- **Module not found**: Ensure Flask is installed: `pip install Flask`
- **Page not loading**: Check that the application is running on `http://localhost:5000` 