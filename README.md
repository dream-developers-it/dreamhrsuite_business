# DreamHR-AI: Intelligent HR Solutions

DreamHR-AI is a comprehensive employee monitoring and HR portal solution with real-time tracking, screenshots, productivity analysis, and employee engagement tools. Perfect for remote teams and workforce management.

## Features

- 👥 User Authentication & Management
  - Custom user model with email-based authentication
  - Secure registration and login system
  - Profile management

- 📊 Employee Monitoring
  - Real-time tracking
  - Screenshot capabilities
  - Productivity analysis
  - Employee engagement tools

- 🔔 Notifications
  - Slack integration for new user registrations
  - Contact form submission notifications
  - Email notifications

- 🎨 Modern UI/UX
  - Responsive design
  - Bootstrap-based interface
  - Clean and intuitive navigation

## Tech Stack

- **Backend**: Django 5.1.5
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite (default)
- **CSS Framework**: Bootstrap 4
- **Form Handling**: django-crispy-forms
- **Email**: SMTP (Gmail)
- **Notifications**: Slack Webhooks
- **Security**: python-dotenv for environment variables

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/dreamhrsuite_business.git
   cd dreamhrsuite_business
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with the following variables:
   ```env
   # Django Settings
   DJANGO_SECRET_KEY=your_secret_key
   DJANGO_DEBUG=False

   # Email Settings
   EMAIL_HOST_USER=your_email@gmail.com
   EMAIL_HOST_PASSWORD=your_app_password
   DEFAULT_FROM_EMAIL=your_email@gmail.com

   # Slack Webhooks
   SLACK_CONTACT_WEBHOOK=your_slack_webhook_url
   SLACK_REGISTRATION_WEBHOOK=your_slack_registration_webhook_url
   ```

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Environment Variables

The project uses environment variables for sensitive data. Make sure to set up the following in your `.env` file:

- `DJANGO_SECRET_KEY`: Django secret key
- `DJANGO_DEBUG`: Debug mode (True/False)
- `EMAIL_HOST_USER`: Gmail address
- `EMAIL_HOST_PASSWORD`: Gmail app password
- `DEFAULT_FROM_EMAIL`: Default sender email
- `SLACK_CONTACT_WEBHOOK`: Slack webhook for contact form notifications
- `SLACK_REGISTRATION_WEBHOOK`: Slack webhook for registration notifications

## Project Structure

```
dreamhrsuite_business/
├── dreamhrbusiness/        # Project settings
├── dreamhrbusinessweb/    # Main application
├── templates/             # HTML templates
│   └── iLanding/         # Landing page templates
├── static/               # Static files
├── media/               # User uploaded files
├── requirements.txt     # Project dependencies
└── manage.py           # Django management script
```

## Security Features

- Environment variables for sensitive data
- Custom user model with email authentication
- CSRF protection
- Secure password hashing
- Protected routes with authentication required
- Slack notifications for important events

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is proprietary and confidential. All rights reserved.

## Contact

DreamHR-AI Team - contact@dreamhrai.com
Website: https://dreamhrai.com
