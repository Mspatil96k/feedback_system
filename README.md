# Student Feedback System

A modern web-based student feedback system built with Flask, featuring a beautiful UI and admin dashboard.

## Features

- Student feedback submission with:
  - Name and enrollment number
  - Subject selection
  - Teacher selection
  - 5-star rating system
  - Detailed feedback text
- Admin dashboard with:
  - View all feedback submissions
  - Export feedback to CSV
  - Secure login system
- Modern, responsive UI with animations
- Mobile-friendly design

## Setup Instructions

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python app.py
   ```
5. Access the application at `http://localhost:5000`

## Default Admin Credentials

- Username: admin
- Password: admin123

## Technologies Used

- Backend: Flask, SQLAlchemy
- Frontend: HTML5, CSS3, Font Awesome
- Database: SQLite
- Data Export: Pandas

## Security Notes

- Change the default admin credentials after first login
- Update the secret key in app.py for production use
- Implement proper security measures before deploying to production

## License

MIT License 