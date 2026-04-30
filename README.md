# Student E-Commerce API

A Django REST Framework based e-commerce API for student projects with Paystack payment integration.

## Features

- User authentication and registration
- Product management with categories
- Order management system
- **Paystack payment integration**
- Product reviews and ratings
- Real-time messaging system
- Admin panel for management
- RESTful API endpoints
- Notification system

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

# Paystack Payment Settings
PAYSTACK_PUBLIC_KEY=your_paystack_public_key
PAYSTACK_SECRET_KEY=your_paystack_secret_key
```

**Getting Paystack Keys:**
1. Sign up at [Paystack](https://paystack.co)
2. Go to Settings → API Keys
3. Copy your Public and Secret keys
4. Add them to your `.env` file

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
- `POST /api/products/` - Create product (seller auth required)
- `GET /api/products/categories/` - List categories
- `POST /api/products/categories/` - Create single category
- `POST /api/products/categories/bulk_create/` - Create multiple categories
- `POST /api/products/{id}/add_review/` - Add product review (auth required)
- `GET /api/products/{id}/reviews/` - Get product reviews

### Orders
- `GET /api/orders/` - List user orders (auth required)
- `POST /api/orders/create_order/` - Create new order (auth required)
- `POST /api/orders/{id}/cancel/` - Cancel order (auth required)

### Payments (Paystack Integration)
- `POST /api/orders/payment/initialize/` - Initialize payment (auth required)
- `GET /api/orders/payment/verify/?reference=xxx` - Verify payment (auth required)
- `POST /api/orders/payment/webhook/` - Paystack webhook endpoint (no auth)

### Messaging
- `GET /api/messaging/conversations/` - List user conversations (auth required)
- `POST /api/messaging/conversations/` - Create new conversation (auth required)
- `GET /api/messaging/conversations/{id}/messages/` - Get conversation messages (auth required)
- `POST /api/messaging/conversations/{id}/messages/` - Send message (auth required)

### Notifications
- `GET /api/notifications/` - List user notifications (auth required)
- `PUT /api/notifications/{id}/mark-read/` - Mark notification as read (auth required)

### Admin Panel
Access at: `http://127.0.0.1:8000/admin/`

## Usage Examples

### Register User

**Buyer Registration:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "student", "email": "student@example.com", "password": "Password123", "password2": "Password123", "first_name": "John", "last_name": "Doe", "role": "buyer"}'
```

**Seller Registration:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "seller", "email": "seller@example.com", "password": "Password123", "password2": "Password123", "first_name": "Jane", "last_name": "Smith", "role": "seller"}'
```

### Login
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "student", "password": "password123"}'
```

### Create Single Category
```bash
curl -X POST http://127.0.0.1:8000/api/products/categories/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Electronics",
    "description": "Electronic devices and gadgets"
  }'
```

### Create Multiple Categories
```bash
curl -X POST http://127.0.0.1:8000/api/products/categories/bulk_create/ \
  -H "Content-Type: application/json" \
  -d '{
    "categories": [
      {
        "name": "Electronics",
        "description": "Electronic devices and gadgets"
      },
      {
        "name": "Books",
        "description": "Textbooks and novels"
      },
      {
        "name": "Clothing",
        "description": "Fashion and apparel"
      },
      {
        "name": "Sports Equipment",
        "description": "Sports and fitness gear"
      }
    ]
  }'
```

### Create Order
```bash
curl -X POST http://127.0.0.1:8000/api/orders/ \
  -H "Authorization: Token your-token-here" \
  -H "Content-Type: application/json" \
  -d '{"items": [{"product_id": 1, "quantity": 2}]}'
```

### Initialize Payment
```bash
curl -X POST http://127.0.0.1:8000/api/orders/payment/initialize/ \
  -H "Authorization: Token your-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": 1,
    "email": "buyer@example.com",
    "amount": 2500.00,
    "callback_url": "http://yourapp.com/payment/callback"
  }'
```

### Verify Payment
```bash
curl -X GET "http://127.0.0.1:8000/api/orders/payment/verify/?reference=pay_1234567890" \
  -H "Authorization: Token your-token-here"
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
|   |-- models.py       # Order, OrderItem, and Payment models
|   |-- views.py        # Order views
|   |-- payment_views.py # Payment views (Paystack integration)
|   |-- serializers.py  # Order and Payment serializers
|   |-- urls.py         # Order and payment URLs
|-- manage.py           # Django management script
|-- requirements.txt    # Python dependencies
```

## Payment Flow

The payment system follows this workflow:

1. **Order Creation**: Buyer creates an order with products
2. **Payment Initialization**: Buyer initiates payment via Paystack
3. **Payment Processing**: Buyer completes payment on Paystack's secure page
4. **Payment Verification**: System verifies payment status
5. **Order Confirmation**: Order auto-accepts on successful payment
6. **Notifications**: Both buyer and seller receive notifications

### Payment States

- **Pending**: Payment initialized but not completed
- **Processing**: Payment is being processed
- **Success**: Payment completed successfully
- **Failed**: Payment failed or was cancelled
- **Reversed**: Payment was reversed (refund)

### Webhook Configuration

To receive real-time payment updates:

1. Go to your Paystack dashboard
2. Navigate to Settings → Webhooks
3. Add your webhook URL: `https://yourdomain.com/api/orders/payment/webhook/`
4. Select events: `charge.success` and `charge.failed`

### Security Notes

- Always verify payment status before accepting orders
- Use HTTPS in production
- Keep your Paystack secret keys secure
- Implement proper error handling for failed payments

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request