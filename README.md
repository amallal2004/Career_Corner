# Event Management and Gamification Platform

This is a comprehensive event management and gamification platform built with Django and Django REST Framework. It provides a robust backend for managing user authentication, events, tasks, submissions, and a leaderboard system to encourage user engagement.

## Features

- **User Authentication:** Secure user registration and login with token-based authentication.
- **Gamified Levels:** Create and manage levels with tasks for users to complete and earn points.
- **Submissions System:** Users can submit their work for each level, which can be reviewed and graded by mentors.
- **Leaderboard:** A leaderboard to display the top-performing users based on their scores.
- **Session Management:** Create and manage sessions or events, and track user attendance.
- **User Profiles:** Each user has a profile with their details and score.
- **RESTful API:** A well-documented and easy-to-use REST API for all platform functionalities.

## Tech Stack

- **Backend:** Django, Django REST Framework
- **Database:** SQLite (default, can be configured for other databases)
- **Authentication:** Token-based authentication
- **Dependencies:** `django`, `djangorestframework`, `django-cors-headers`

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/your-project-name.git
   cd your-project-name
   ```

2. **Create a virtual environment and install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

The application will be available at `http://127.0.0.1:8000`.

## API Endpoints

| Method | Endpoint                       | Description                               |
|--------|--------------------------------|-------------------------------------------|
| POST   | `/api/signup/`                 | Register a new user.                      |
| POST   | `/api/login/`                  | Log in an existing user.                  |
| GET    | `/api/levels/`                 | Get a list of all levels.                 |
| POST   | `/api/submissions/`            | Submit a task for a level.                |
| PUT    | `/api/submissions/<int:pk>/`   | Update a submission (for mentors).        |
| GET    | `/api/leaderboard/`            | Get the leaderboard with top users.       |
| GET    | `/api/sessions/`               | Get a list of all sessions.               |
| POST   | `/api/sessions/create/`        | Create a new session (for mentors).       |
| POST   | `/api/sessions/<int:session_id>/attendance/` | Mark attendance for a session (for mentors). |
| GET    | `/api/profile/`                | Get the profile of the logged-in user.    |

## Testing

To run the tests for the application, use the following command:

```bash
python manage.py test
```

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

1. **Fork the repository.**
2. **Create a new branch:** `git checkout -b feature/your-feature-name`
3. **Make your changes and commit them:** `git commit -m 'Add some feature'`
4. **Push to the branch:** `git push origin feature/your-feature-name`
5. **Open a pull request.**
