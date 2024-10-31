# Blood Bank Management API

This project is a RESTful API for a Blood Bank Management System, built using Django and Django REST Framework. It includes functionality for managing blood donors, blood inventory, and blood requests, with role-based permissions for admin and regular users.

## Features

- **Donor Management** (Admins only): Add, view, update, and delete donor information.
- **Blood Inventory Management** (Admins only): Add and update blood inventory. Low inventory levels trigger email alerts.
- **Blood Requests**:
  - Regular users can create and view their blood requests.
  - Admins can fulfill blood requests, update request status, and view all requests.

## Technologies

- **Backend**: Django, Django REST Framework
- **Authentication**: JSON Web Token (JWT) for secure API access
- **Database**: SQLite (for development and testing)
- **Testing**: Django’s `TestCase` and Django REST Framework’s `APITestCase`

## Prerequisites

- Python 3.12.0
- Django 5.1.2
- Django REST Framework
- SimpleJWT for JWT-based authentication

## Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>

2. **Set up a virtual environment**:
   python -m venv virt
   source virt/bin/activate  # On Windows: virt\Scripts\activate

3. **Install dependencies"":
   pip install -r requirements.txt

4. **Set up environment variables for email notifications (if using Gmail SMTP)**:
   EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   EMAIL_HOST = 'smtp.gmail.com'
   EMAIL_PORT = 587
   EMAIL_USE_TLS = True
   EMAIL_HOST_USER = 'your-email@gmail.com'
   EMAIL_HOST_PASSWORD = 'your-email-password'
   DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
   For local testing only email backend is set up

5. **Apply Migrations**:
   python manage.py migrate

6. **Create a superuser for admin access**:
   python manage.py createsuperuser

7. **Run the server**:
   python manage.py runserver

## API Endpoints

| Endpoint                          | Method | Description                                                | Access       |
|-----------------------------------|--------|------------------------------------------------------------|--------------|
| /api/token/                       | POST   | Obtain JWT access and refresh tokens                       | All users    |
| /api/token/refresh/               | POST   | Refresh JWT access token                                   | All users    |
| /api/register/                    | POST   | Register a new user                                        | All users    |
| /api/donors/                      | GET    | List all donors                                            | Admin only   |
| /api/donors/                      | POST   | Add a new donor                                            | Admin only   |
| /api/donors/<int:pk>/             | GET    | Retrieve a specific donor                                  | Admin only   |
| /api/donors/<int:pk>/             | PUT    | Update a specific donor                                    | Admin only   |
| /api/donors/<int:pk>/             | DELETE | Delete a specific donor                                    | Admin only   |
| /api/inventory/                   | GET    | List all blood inventory items                             | Admin only   |
| /api/inventory/                   | POST   | Add new inventory item                                     | Admin only   |
| /api/inventory/<int:pk>/          | PUT    | Update inventory item                                      | Admin only   |
| /api/requests/                    | GET    | List user’s blood requests                                 | Regular user |
| /api/requests/                    | POST   | Create a new blood request                                 | Regular user |
| /api/admin/requests/              | GET    | List all blood requests                                    | Admin only   |
| /api/admin/requests/<int:pk>/     | PUT    | Fulfill or update the status of a specific blood request   | Admin only   |

## Permissions
- Admin users can access and manage all resources, including donors, inventory, and requests.
- Regular users can only create and view their own blood requests and check blood availability.

## Testing
- Tests are included for the core features of the system, including:
1. **Authentication**: Tests for login, token retrieval, and token refresh.
2. **Donor Management (Admin only)**: Create, retrieve, and list donors.
3. **Blood Inventory Management (Admin only)**: Add and update inventory with low-inventory email alerts.
4. **Blood Request Management**:
   - Regular users can create and view their requests.
   - Admins can fulfill or update requests based on inventory.

## Running Tests
- To run all tests:
  python manage.py test

## Test Coverage:
   test.py includes tests for authentication, donor management, blood inventory management, and blood requests.

## Postman Collection
     To test the API with Postman:
     - Import the Postman collection provided with this project.
     - Set the base URL for your local server (e.g., http://127.0.0.1:8000/).
     - Use JWT authentication: Obtain a token from /api/token/ and set it in the Authorization header as Bearer <token>.
   
## Notes:
**Email Notifications**: When blood inventory levels are critically low, an email is sent to the specified address in settings.py.
**Database**: SQLite is used for development and testing. For production, consider switching to PostgreSQL or another robust database.

## License
This project is intended for interview purposes only. No permission is granted for further distribution or commercial use.
