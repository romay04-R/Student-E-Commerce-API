# Student E-Commerce API

A Django REST Framework based e-commerce API for student projects.

## Features

- User authentication and registration
- Product management with categories
- Order management system
- Product reviews and ratings
- Admin panel for management
- RESTful API endpoints

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Setup

Create a `.env` file in the project root:

```
SECRET_KEY=your-secret-key-here
DEBUG=True
```

### 3. Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser

```bash
python manage.py createsuperuser
```

### 5. Run the Server

```bash
python manage.py runserver
```

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - User login
- `GET/PUT /api/auth/profile/` - User profile

### Products
- `GET /api/products/` - List all products
- `GET /api/products/{id}/` - Get product details
- `GET /api/products/categories/` - List categories
- `POST /api/products/{id}/add_review/` - Add product review (auth required)
- `GET /api/products/{id}/reviews/` - Get product reviews

### Orders
- `GET /api/orders/` - List user orders (auth required)
- `POST /api/orders/create_order/` - Create new order (auth required)
- `POST /api/orders/{id}/cancel/` - Cancel order (auth required)

### Admin Panel
Access at: `http://127.0.0.1:8000/admin/`

## Usage Examples

### Register User
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "student", "email": "student@example.com", "password": "password123", "first_name": "John", "last_name": "Doe"}'
```

### Login
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "student", "password": "password123"}'
```

### Create Order
```bash
curl -X POST http://127.0.0.1:8000/api/orders/create_order/ \
  -H "Authorization: Token your-token-here" \
  -H "Content-Type: application/json" \
  -d '{"items": [{"product_id": 1, "quantity": 2}]}'
```

## Project Structure

```
Student-E-Commerce-API/
|-- ecommerce/           # Main Django project
|   |-- settings.py     # Project settings
|   |-- urls.py         # Main URL configuration
|-- products/           # Products app
|   |-- models.py       # Product and Category models
|   |-- views.py        # Product views
|   |-- serializers.py  # Product serializers
|-- users/              # User management app
|   |-- models.py       # User profile model
|   |-- views.py        # Authentication views
|   |-- serializers.py  # User serializers
|-- orders/             # Orders app
|   |-- models.py       # Order and OrderItem models
|   |-- views.py        # Order views
|   |-- serializers.py  # Order serializers
|-- manage.py           # Django management script
|-- requirements.txt    # Python dependencies
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request