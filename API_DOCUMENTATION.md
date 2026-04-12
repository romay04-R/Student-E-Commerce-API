# Student E-Commerce API Documentation

## Overview

This is a comprehensive REST API for a student e-commerce platform where users can buy and sell products. The API includes user authentication, product management, order processing, messaging, and administrative features.

**Base URL**: `http://localhost:8000/api`

**Authentication**: JWT (JSON Web Tokens) required for most endpoints

## Authentication

### How to Authenticate

1. **Register** a new user account
2. **Login** to get JWT tokens (access and refresh)
3. Include the access token in the `Authorization` header for authenticated requests:

```
Authorization: Bearer <access_token>
```

### Token Refresh

Access tokens expire after 7 days. Use the refresh token to get new access tokens.

---

## Authentication Endpoints

### POST /api/auth/register/
Register a new user account.

**Request:**
```bash
POST /api/auth/register/
Content-Type: application/json

{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePass123",
    "password2": "SecurePass123",
    "first_name": "John",
    "last_name": "Doe"
}
```

**Response (201 Created):**
```json
{
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI0NTQ2NDAwLCJpYXQiOjE3MjM5NDI4MDAsImp0aSI6IjFiMjM0NTY3ODkwMTIzNDUiLCJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImpvaG5kb2UiLCJlbWFpbCI6ImpvaG5AZXhhbXBsZS5jb20iLCJmaXJzdF9uYW1lIjoiSm9obiIsImxhc3RfbmFtZSI6IkRvZSIsImlzX3N0YWZmIjpmYWxzZSwiaXNfc3VwZXJ1c2VyIjpmYWxzZX0.N9aP9h7yKX8vZ1wL2mN3qR4tS5uV6wX7yZ8a1b2c3d4",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyNDU0NjQwMCwiaWF0IjoxNzIzOTQyODAwLCJqdGkiOiI5YThjMGRlZjQ1Njc4OTAxMjM0NTY3IiwidXNlcl9pZCI6MSwidXNlcm5hbWUiOiJqb2huZG9lIiwiZW1haWwiOiJqb2hlQGV4YW1wbGUuY29tIiwiZmlyc3RfbmFtZSI6IkpvaG4iLCJsYXN0X25hbWUiOiJEb2UiLCJpc19zdGFmZiI6ZmFsc2UsImlzX3N1cGVydXNlciI6ZmFsc2V9.A1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2"
}
```

**Error Response (400):**
```json
{
    "username": ["A user with that username already exists."],
    "email": ["A user with that email already exists."]
}
```

### POST /api/auth/login/
Authenticate user and get JWT tokens.

**Request:**
```bash
POST /api/auth/login/
Content-Type: application/json

{
    "username": "johndoe",
    "password": "SecurePass123"
}
```

**Response (200 OK):**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI0NTQ2NDAwLCJpYXQiOjE3MjM5NDI4MDAsImp0aSI6IjFiMjM0NTY3ODkwMTIzNDUiLCJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImpvaG5kb2UiLCJlbWFpbCI6ImpvaG5AZXhhbXBsZS5jb20iLCJmaXJzdF9uYW1lIjoiSm9obiIsImxhc3RfbmFtZSI6IkRvZSIsImlzX3N0YWZmIjpmYWxzZSwiaXNfc3VwZXJ1c2VyIjpmYWxzZX0.N9aP9h7yKX8vZ1wL2mN3qR4tS5uV6wX7yZ8a1b2c3d4",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyNDU0NjQwMCwiaWF0IjoxNzIzOTQyODAwLCJqdGkiOiI5YThjMGRlZjQ1Njc4OTAxMjM0NTY3IiwidXNlcl9pZCI6MSwidXNlcm5hbWUiOiJqb2huZG9lIiwiZW1haWwiOiJqb2hlQGV4YW1wbGUuY29tIiwiZmlyc3RfbmFtZSI6IkpvaG4iLCJsYXN0X25hbWUiOiJEb2UiLCJpc19zdGFmZiI6ZmFsc2UsImlzX3N1cGVydXNlciI6ZmFsc2V9.A1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2",
    "user_id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "is_staff": false,
    "is_superuser": false,
    "profile_id": "550e8400-e29b-41d4-a716-446655440000",
    "is_seller": false,
    "average_rating": "0.00",
    "total_sales": "0.00"
}
```

**Error Response (401):**
```json
{
    "detail": "No active account found with the given credentials"
}
```

### POST /api/auth/refresh/
Refresh access token using refresh token.

**Request:**
```bash
POST /api/auth/refresh/
Content-Type: application/json

{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyNDU0NjQwMCwiaWF0IjoxNzIzOTQyODAwLCJqdGkiOiI5YThjMGRlZjQ1Njc4OTAxMjM0NTY3IiwidXNlcl9pZCI6MSwidXNlcm5hbWUiOiJqb2huZG9lIiwiZW1haWwiOiJqb2hlQGV4YW1wbGUuY29tIiwiZmlyc3RfbmFtZSI6IkpvaG4iLCJsYXN0X25hbWUiOiJEb2UiLCJpc19zdGFmZiI6ZmFsc2UsImlzX3N1cGVydXNlciI6ZmFsc2V9.A1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2"
}
```

**Response (200 OK):**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI0NTQ2NDAwLCJpYXQiOjE3MjM5NDI4MDAsImp0aSI6IjFiMjM0NTY3ODkwMTIzNDUiLCJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImpvaG5kb2UiLCJlbWFpbCI6ImpvaG5AZXhhbXBsZS5jb20iLCJmaXJzdF9uYW1lIjoiSm9obiIsImxhc3RfbmFtZSI6IkRvZSIsImlzX3N0YWZmIjpmYWxzZSwiaXNfc3VwZXJ1c2VyIjpmYWxzZX0.N9aP9h7yKX8vZ1wL2mN3qR4tS5uV6wX7yZ8a1b2c3d4"
}
```

**Error Response (401):**
```json
{
    "detail": "Token is invalid or expired",
    "code": "token_not_valid"
}
```

---

## User Management Endpoints

### GET /api/users/profile/
Get current user's profile information.

**Request:**
```bash
GET /api/users/profile/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**
```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+1234567890",
    "address": "123 Main St, City, State 12345",
    "date_of_birth": "1995-01-01",
    "bio": "Computer science student passionate about web development",
    "profile_picture": "http://localhost:8000/media/profiles/john_doe_avatar.jpg",
    "is_seller": true,
    "average_rating": "4.50",
    "total_sales": "1250.00",
    "created_at": "2024-01-01T12:00:00Z"
}
```

**Error Response (401):**
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### PUT /api/users/profile/
Update current user's profile.

**Request:**
```bash
PUT /api/users/profile/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
    "first_name": "John",
    "last_name": "Smith",
    "phone": "+1234567890",
    "address": "456 Oak Ave, New City, NY 67890",
    "bio": "Updated bio: Experienced software developer",
    "date_of_birth": "1995-01-01",
    "is_seller": true
}
```

**Response (200 OK):**
```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Smith",
    "phone": "+1234567890",
    "address": "456 Oak Ave, New City, NY 67890",
    "date_of_birth": "1995-01-01",
    "bio": "Updated bio: Experienced software developer",
    "profile_picture": "http://localhost:8000/media/profiles/john_doe_avatar.jpg",
    "is_seller": true,
    "average_rating": "4.50",
    "total_sales": "1250.00",
    "created_at": "2024-01-01T12:00:00Z"
}
```

**Error Response (400):**
```json
{
    "phone": ["Enter a valid phone number."],
    "date_of_birth": ["Date has wrong format. Use one of these formats instead: YYYY-MM-DD."]
}
```

### GET /api/users/stats/
Get current user's statistics.

**Request:**
```bash
GET /api/users/stats/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**
```json
{
    "total_products": 15,
    "active_products": 12,
    "total_orders": 25,
    "completed_orders": 20,
    "total_sales": "2500.00",
    "average_rating": "4.50",
    "total_reviews": 18
}
```

**Error Response (401):**
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### GET /api/users/{userId}/
Get public user profile by user ID.

**Request:**
```bash
GET /api/users/550e8400-e29b-41d4-a716-446655440000/
```

**Response (200 OK):**
```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "bio": "Computer science student passionate about web development",
    "profile_picture": "http://localhost:8000/media/profiles/john_doe_avatar.jpg",
    "is_seller": true,
    "average_rating": "4.50",
    "total_sales": "1250.00",
    "created_at": "2024-01-01T12:00:00Z"
}
```

**Error Response (404):**
```json
{
    "detail": "Not found."
}
```

### GET /api/users/{userId}/rating/
Get user's rating information.

**Request:**
```bash
GET /api/users/550e8400-e29b-41d4-a716-446655440000/rating/
```

**Response (200 OK):**
```json
{
    "average_rating": 4.5,
    "total_reviews": 18
}
```

**Error Response (404):**
```json
{
    "detail": "Not found."
}
```

---

## Product Management Endpoints

### GET /api/products/
List all products with pagination and filtering.

**Request:**
```bash
GET /api/products/?page=1&page_size=10&category=Electronics&min_price=100&max_price=500&condition=good&is_active=true
```

**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)
- `category`: Filter by category name
- `search`: Search in product name and description
- `min_price`: Minimum price filter
- `max_price`: Maximum price filter
- `condition`: Filter by condition (new, like-new, good, fair, poor)
- `is_active`: Filter by active status (true/false)

**Response (200 OK):**
```json
{
    "count": 100,
    "next": "http://localhost:8000/api/products/?page=2&page_size=10&category=Electronics&min_price=100&max_price=500&condition=good&is_active=true",
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Dell Latitude Laptop",
            "description": "Dell Latitude 5400 laptop in excellent condition. Intel i5 processor, 8GB RAM, 256GB SSD. Perfect for students.",
            "price": "450.00",
            "category": 1,
            "category_name": "Electronics",
            "user": 1,
            "seller_username": "johndoe",
            "condition": "good",
            "location": "New York, NY",
            "image": "http://localhost:8000/media/products/dell_laptop_main.jpg",
            "stock": 1,
            "is_active": true,
            "views_count": 25,
            "average_rating": 4.5,
            "images": [
                {
                    "id": 1,
                    "image": "http://localhost:8000/media/products/dell_laptop_1.jpg",
                    "uploaded_at": "2024-01-01T12:00:00Z"
                },
                {
                    "id": 2,
                    "image": "http://localhost:8000/media/products/dell_laptop_2.jpg",
                    "uploaded_at": "2024-01-01T12:00:00Z"
                }
            ],
            "seller_info": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "username": "johndoe",
                "first_name": "John",
                "last_name": "Doe",
                "bio": "Computer science student passionate about web development",
                "profile_picture": "http://localhost:8000/media/profiles/john_doe_avatar.jpg",
                "is_seller": true,
                "average_rating": "4.50",
                "total_sales": "1250.00",
                "created_at": "2024-01-01T12:00:00Z"
            },
            "created_at": "2024-01-01T12:00:00Z",
            "updated_at": "2024-01-01T12:00:00Z"
        }
    ]
}
```

### POST /api/products/
Create a new product (requires authentication).

**Request:**
```bash
POST /api/products/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: multipart/form-data

name: "MacBook Pro 2020"
description: "MacBook Pro 13-inch 2020 model. M1 chip, 8GB RAM, 256GB SSD. Excellent condition with original box and charger."
price: "850.00"
category: 1
condition: "like-new"
location: "Los Angeles, CA"
stock: 1
is_active: true
images: [macbook_1.jpg, macbook_2.jpg, macbook_3.jpg]
```

**Response (201 Created):**
```json
{
    "id": 2,
    "name": "MacBook Pro 2020",
    "description": "MacBook Pro 13-inch 2020 model. M1 chip, 8GB RAM, 256GB SSD. Excellent condition with original box and charger.",
    "price": "850.00",
    "category": 1,
    "category_name": "Electronics",
    "user": 1,
    "seller_username": "johndoe",
    "condition": "like-new",
    "location": "Los Angeles, CA",
    "image": "http://localhost:8000/media/products/macbook_main.jpg",
    "stock": 1,
    "is_active": true,
    "views_count": 0,
    "average_rating": 0,
    "images": [
        {
            "id": 3,
            "image": "http://localhost:8000/media/products/macbook_1.jpg",
            "uploaded_at": "2024-01-15T10:30:00Z"
        },
        {
            "id": 4,
            "image": "http://localhost:8000/media/products/macbook_2.jpg",
            "uploaded_at": "2024-01-15T10:30:00Z"
        },
        {
            "id": 5,
            "image": "http://localhost:8000/media/products/macbook_3.jpg",
            "uploaded_at": "2024-01-15T10:30:00Z"
        }
    ],
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
}
```

**Error Response (401):**
```json
{
    "detail": "Authentication credentials were not provided."
}
```

**Error Response (400):**
```json
{
    "name": ["This field may not be blank."],
    "price": ["A valid number is required."],
    "category": ["This field is required."]
}
```

### GET /api/products/{id}/
Get product details by ID.

**Request:**
```bash
GET /api/products/1/
```

**Response (200 OK):**
```json
{
    "id": 1,
    "name": "Dell Latitude Laptop",
    "description": "Dell Latitude 5400 laptop in excellent condition. Intel i5 processor, 8GB RAM, 256GB SSD. Perfect for students.",
    "price": "450.00",
    "category": 1,
    "category_name": "Electronics",
    "user": 1,
    "seller_username": "johndoe",
    "condition": "good",
    "location": "New York, NY",
    "image": "http://localhost:8000/media/products/dell_laptop_main.jpg",
    "stock": 1,
    "is_active": true,
    "views_count": 26,
    "average_rating": 4.5,
    "images": [...],
    "seller_info": {...},
    "created_at": "2024-01-01T12:00:00Z",
    "updated_at": "2024-01-01T12:00:00Z"
}
```

**Error Response (404):**
```json
{
    "detail": "Not found."
}
```

### PUT /api/products/{id}/
Update product (requires authentication and ownership).

**Request:**
```bash
PUT /api/products/1/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: multipart/form-data

name: "Dell Latitude Laptop - Updated"
description: "Dell Latitude 5400 laptop in excellent condition. Intel i5 processor, 8GB RAM, 256GB SSD. Perfect for students. Price reduced!"
price: "400.00"
condition: "good"
location: "New York, NY"
stock: 1
is_active: true
```

**Response (200 OK):**
```json
{
    "id": 1,
    "name": "Dell Latitude Laptop - Updated",
    "description": "Dell Latitude 5400 laptop in excellent condition. Intel i5 processor, 8GB RAM, 256GB SSD. Perfect for students. Price reduced!",
    "price": "400.00",
    ...
    "updated_at": "2024-01-16T14:20:00Z"
}
```

**Error Response (403):**
```json
{
    "detail": "You do not have permission to perform this action."
}
```

### DELETE /api/products/{id}/
Delete product (requires authentication and ownership).

**Request:**
```bash
DELETE /api/products/1/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (204 No Content):** (Empty response body)

**Error Response (403):**
```json
{
    "detail": "You do not have permission to perform this action."
}
```

### GET /api/products/search/
Search products.

**Request:**
```bash
GET /api/products/search/?q=laptop&category=Electronics&min_price=300&max_price=1000
```

**Query Parameters:**
- `q`: Search query
- `category`: Filter by category
- Other filters same as list endpoint

**Response (200 OK):** Same format as product list

### GET /api/products/category/{category}/
Get products by category name.

**Request:**
```bash
GET /api/products/category/Electronics/?page=1&page_size=20
```

**Response (200 OK):** Same format as product list

### GET /api/products/user/{userId}/products/
Get products by user ID.

**Request:**
```bash
GET /api/products/user/550e8400-e29b-41d4-a716-446655440000/products/
```

**Response (200 OK):** Same format as product list

---

## Product Categories

### GET /api/products/categories/
List all product categories.

**Response (200):**
```json
[
    {
        "id": 1,
        "name": "Electronics",
        "description": "Electronic devices and accessories",
        "created_at": "2024-01-01T12:00:00Z"
    },
    {
        "id": 2,
        "name": "Books",
        "description": "Textbooks and novels",
        "created_at": "2024-01-01T12:00:00Z"
    }
]
```

### POST /api/products/categories/
Create new category (admin only).

**Headers:** `Authorization: Bearer <access_token>`

**Request Body:**
```json
{
    "name": "Furniture",
    "description": "Desks, chairs, and other furniture"
}
```

---

## Product Reviews

### GET /api/products/reviews/
List all product reviews with pagination.

### POST /api/products/reviews/
Create a product review (requires authentication).

**Headers:** `Authorization: Bearer <access_token>`

**Request Body:**
```json
{
    "product": 1,
    "rating": 5,
    "comment": "Great product, exactly as described!"
}
```

### GET /api/products/reviews/{id}/
Get review details.

### PUT /api/products/reviews/{id}/
Update review (requires authentication and ownership).

### DELETE /api/products/reviews/{id}/
Delete review (requires authentication and ownership).

---

## Order Management Endpoints

### GET /api/orders/
List user's orders (both purchases and sales).

**Request:**
```bash
GET /api/orders/?status=pending&page=1&page_size=10
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Query Parameters:**
- `status`: Filter by status (pending, accepted, rejected, completed, cancelled)
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)

**Response (200 OK):**
```json
{
    "count": 10,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "buyer": 2,
            "seller": 1,
            "buyer_username": "janedoe",
            "seller_username": "johndoe",
            "total_amount": "450.00",
            "status": "pending",
            "notes": "Please deliver to campus library, I'll be there at 3 PM",
            "items": [
                {
                    "id": 1,
                    "order": 1,
                    "product": {
                        "id": 1,
                        "name": "Dell Latitude Laptop",
                        "price": "450.00",
                        "description": "Dell Latitude 5400 laptop in excellent condition",
                        "images": [
                            {
                                "id": 1,
                                "image": "http://localhost:8000/media/products/dell_laptop_1.jpg",
                                "uploaded_at": "2024-01-01T12:00:00Z"
                            }
                        ]
                    },
                    "quantity": 1,
                    "price": "450.00"
                }
            ],
            "product": {
                "id": 1,
                "name": "Dell Latitude Laptop",
                "price": "450.00",
                "description": "Dell Latitude 5400 laptop in excellent condition",
                "images": [...]
            },
            "created_at": "2024-01-15T14:30:00Z",
            "updated_at": "2024-01-15T14:30:00Z"
        }
    ]
}
```

**Error Response (401):**
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### POST /api/orders/create/
Create a new order.

**Request:**
```bash
POST /api/orders/create/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
    "items": [
        {
            "product": 1,
            "quantity": 1
        }
    ],
    "notes": "Please deliver to campus library, I'll be there at 3 PM"
}
```

**Response (201 Created):**
```json
{
    "id": 1,
    "buyer": 2,
    "seller": 1,
    "total_amount": "450.00",
    "status": "pending",
    "notes": "Please deliver to campus library, I'll be there at 3 PM",
    "items": [
        {
            "id": 1,
            "order": 1,
            "product": {
                "id": 1,
                "name": "Dell Latitude Laptop",
                "price": "450.00",
                "description": "Dell Latitude 5400 laptop in excellent condition",
                "images": [...]
            },
            "quantity": 1,
            "price": "450.00"
        }
    ],
    "created_at": "2024-01-15T14:30:00Z",
    "updated_at": "2024-01-15T14:30:00Z"
}
```

**Error Response (400):**
```json
{
    "items": ["This field is required."],
    "non_field_errors": ["All items must be from the same seller"]
}
```

**Error Response (401):**
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### GET /api/orders/purchases/
Get current user's purchase orders.

**Request:**
```bash
GET /api/orders/purchases/?status=pending
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):** Same format as order list, filtered for purchases only

### GET /api/orders/sales/
Get current user's sales orders.

**Request:**
```bash
GET /api/orders/sales/?status=pending
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):** Same format as order list, filtered for sales only

### GET /api/orders/details/{orderId}/
Get detailed order information.

**Request:**
```bash
GET /api/orders/details/1/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):** Same format as single order object with full details

**Error Response (403):**
```json
{
    "detail": "You do not have permission to view this order."
}
```

### POST /api/orders/{orderId}/accept/
Accept an order (seller only).

**Request:**
```bash
POST /api/orders/1/accept/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**
```json
{
    "id": 1,
    "buyer": 2,
    "seller": 1,
    "total_amount": "450.00",
    "status": "accepted",
    "notes": "Please deliver to campus library, I'll be there at 3 PM",
    "items": [...],
    "created_at": "2024-01-15T14:30:00Z",
    "updated_at": "2024-01-15T15:45:00Z"
}
```

**Error Response (403):**
```json
{
    "detail": "Only the seller can accept this order."
}
```

**Error Response (400):**
```json
{
    "detail": "Order cannot be accepted in its current status."
}
```

### POST /api/orders/{orderId}/reject/
Reject an order (seller only).

**Request:**
```bash
POST /api/orders/1/reject/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
    "reason": "Product already sold to another buyer"
}
```

**Response (200 OK):**
```json
{
    "id": 1,
    "buyer": 2,
    "seller": 1,
    "total_amount": "450.00",
    "status": "rejected",
    "notes": "Please deliver to campus library, I'll be there at 3 PM",
    "items": [...],
    "created_at": "2024-01-15T14:30:00Z",
    "updated_at": "2024-01-15T15:45:00Z"
}
```

**Error Response (403):**
```json
{
    "detail": "Only the seller can reject this order."
}
```

### POST /api/orders/{orderId}/complete/
Mark order as completed (seller only).

**Request:**
```bash
POST /api/orders/1/complete/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**
```json
{
    "id": 1,
    "buyer": 2,
    "seller": 1,
    "total_amount": "450.00",
    "status": "completed",
    "notes": "Please deliver to campus library, I'll be there at 3 PM",
    "items": [...],
    "created_at": "2024-01-15T14:30:00Z",
    "updated_at": "2024-01-16T10:30:00Z"
}
```

**Error Response (403):**
```json
{
    "detail": "Only the seller can complete this order."
}
```

**Error Response (400):**
```json
{
    "detail": "Order must be accepted before it can be completed."
}
```

---

## Messaging Endpoints

### GET /api/conversations/
List user's conversations.

**Request:**
```bash
GET /api/conversations/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**
```json
[
    {
        "id": 1,
        "participant": {
            "id": 2,
            "username": "janedoe",
            "first_name": "Jane",
            "last_name": "Doe",
            "profile_picture": "http://localhost:8000/media/profiles/jane_doe_avatar.jpg"
        },
        "last_message": "Yes, it's still available! Would you like to see more photos?",
        "last_message_time": "2024-01-15T16:30:00Z",
        "unread_count": 2
    },
    {
        "id": 2,
        "participant": {
            "id": 3,
            "username": "mike_smith",
            "first_name": "Mike",
            "last_name": "Smith",
            "profile_picture": "http://localhost:8000/media/profiles/mike_smith_avatar.jpg"
        },
        "last_message": "Thanks for the quick response!",
        "last_message_time": "2024-01-14T10:15:00Z",
        "unread_count": 0
    }
]
```

**Error Response (401):**
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### GET /api/conversations/{conversationId}/messages/
Get messages in a conversation.

**Request:**
```bash
GET /api/conversations/1/messages/?page=1&page_size=20
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**
```json
{
    "count": 15,
    "next": "http://localhost:8000/api/conversations/1/messages/?page=2&page_size=20",
    "previous": null,
    "results": [
        {
            "id": 1,
            "sender": 2,
            "sender_username": "janedoe",
            "receiver": 1,
            "content": "Hi, is the Dell laptop still available?",
            "is_read": true,
            "created_at": "2024-01-15T14:00:00Z"
        },
        {
            "id": 2,
            "sender": 1,
            "sender_username": "johndoe",
            "receiver": 2,
            "content": "Yes, it's still available! Would you like to see more photos?",
            "is_read": false,
            "created_at": "2024-01-15T16:30:00Z"
        }
    ]
}
```

**Error Response (403):**
```json
{
    "detail": "You do not have permission to view this conversation."
}
```

### POST /api/messages/
Send a message.

**Request:**
```bash
POST /api/messages/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
    "receiver": 2,
    "content": "Sure! I can send you more photos of the laptop. Are you available this weekend to see it in person?"
}
```

**Response (201 Created):**
```json
{
    "id": 3,
    "sender": 1,
    "sender_username": "johndoe",
    "receiver": 2,
    "content": "Sure! I can send you more photos of the laptop. Are you available this weekend to see it in person?",
    "is_read": false,
    "created_at": "2024-01-15T17:45:00Z"
}
```

**Error Response (400):**
```json
{
    "receiver": ["This field is required."],
    "content": ["This field may not be blank."]
}
```

### POST /api/conversations/{conversationId}/mark-read/
Mark all messages in conversation as read.

**Request:**
```bash
POST /api/conversations/1/mark-read/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**
```json
{
    "message": "All messages marked as read",
    "marked_count": 2
}
```

**Error Response (403):**
```json
{
    "detail": "You do not have permission to modify this conversation."
}
```

### DELETE /api/conversations/{conversationId}/
Delete a conversation.

**Request:**
```bash
DELETE /api/conversations/1/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (204 No Content):** (Empty response body)

**Error Response (403):**
```json
{
    "detail": "You do not have permission to delete this conversation."
}
```

### GET /api/messages/user/{userId}/
Get all messages with a specific user.

**Request:**
```bash
GET /api/messages/user/2/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**
```json
{
    "count": 15,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "sender": 2,
            "sender_username": "janedoe",
            "receiver": 1,
            "content": "Hi, is the Dell laptop still available?",
            "is_read": true,
            "created_at": "2024-01-15T14:00:00Z"
        },
        {
            "id": 2,
            "sender": 1,
            "sender_username": "johndoe",
            "receiver": 2,
            "content": "Yes, it's still available! Would you like to see more photos?",
            "is_read": false,
            "created_at": "2024-01-15T16:30:00Z"
        }
    ]
}
```

---

## Notification Endpoints

### GET /api/notifications/
Get user's notifications.

**Request:**
```bash
GET /api/notifications/?is_read=false&page=1&page_size=10
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**
```json
{
    "count": 8,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "user": 1,
            "type": "order",
            "title": "Order Accepted",
            "message": "Your order for Dell Latitude Laptop has been accepted by johndoe",
            "related_object_id": 1,
            "is_read": false,
            "created_at": "2024-01-15T15:45:00Z"
        },
        {
            "id": 2,
            "user": 1,
            "type": "message",
            "title": "New Message",
            "message": "You have a new message from janedoe",
            "related_object_id": 1,
            "is_read": false,
            "created_at": "2024-01-15T16:30:00Z"
        },
        {
            "id": 3,
            "user": 1,
            "type": "review",
            "title": "New Review",
            "message": "Someone left a review on your product",
            "related_object_id": 1,
            "is_read": true,
            "created_at": "2024-01-14T11:20:00Z"
        }
    ]
}
```

**Error Response (401):**
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### POST /api/notifications/{notificationId}/read/
Mark notification as read.

**Request:**
```bash
POST /api/notifications/1/read/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**
```json
{
    "id": 1,
    "user": 1,
    "type": "order",
    "title": "Order Accepted",
    "message": "Your order for Dell Latitude Laptop has been accepted by johndoe",
    "related_object_id": 1,
    "is_read": true,
    "created_at": "2024-01-15T15:45:00Z"
}
```

**Error Response (403):**
```json
{
    "detail": "You do not have permission to modify this notification."
}
```

**Error Response (404):**
```json
{
    "detail": "Not found."
}
```

### POST /api/notifications/mark-all-read/
Mark all notifications as read.

**Request:**
```bash
POST /api/notifications/mark-all-read/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**
```json
{
    "message": "All notifications marked as read",
    "marked_count": 5
}
```

**Error Response (401):**
```json
{
    "detail": "Authentication credentials were not provided."
}
```

---

## Admin Panel Endpoints (Admin Only)

### GET /api/admin/statistics/
Get platform statistics.

**Request:**
```bash
GET /api/admin/statistics/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**
```json
{
    "total_users": 150,
    "total_products": 500,
    "total_orders": 200,
    "total_revenue": "25000.00",
    "active_products": 450,
    "pending_orders": 15,
    "pending_products": 8,
    "reported_users": 3,
    "reported_products": 5,
    "suspended_users": 2
}
```

**Error Response (403):**
```json
{
    "detail": "You do not have permission to access this endpoint. Admin access required."
}
```

### GET /api/admin/pending-products/
Get products pending approval.

**Request:**
```bash
GET /api/admin/pending-products/?page=1&page_size=20
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**
```json
{
    "count": 8,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 15,
            "name": "iPhone 12 Pro",
            "description": "iPhone 12 Pro in good condition, 128GB, Pacific Blue",
            "price": "650.00",
            "category_name": "Electronics",
            "seller_username": "newuser123",
            "condition": "good",
            "location": "Boston, MA",
            "images": [...],
            "created_at": "2024-01-15T09:30:00Z",
            "is_active": false
        }
    ]
}
```

**Error Response (403):**
```json
{
    "detail": "You do not have permission to access this endpoint. Admin access required."
}
```

### POST /api/admin/products/{productId}/approve/
Approve a product.

**Request:**
```bash
POST /api/admin/products/15/approve/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**
```json
{
    "message": "Product approved successfully",
    "product_id": 15,
    "is_active": true
}
```

**Error Response (403):**
```json
{
    "detail": "You do not have permission to approve products. Admin access required."
}
```

**Error Response (404):**
```json
{
    "detail": "Product not found."
}
```

### POST /api/admin/products/{productId}/reject/
Reject a product.

**Request:**
```bash
POST /api/admin/products/15/reject/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
    "reason": "Product violates our terms of service"
}
```

**Response (200 OK):**
```json
{
    "message": "Product rejected successfully",
    "product_id": 15,
    "reason": "Product violates our terms of service"
}
```

### GET /api/admin/reported-users/
Get reported users.

**Request:**
```bash
GET /api/admin/reported-users/?page=1&page_size=20
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**
```json
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 25,
            "username": "suspicious_user",
            "email": "suspicious@example.com",
            "first_name": "Suspicious",
            "last_name": "User",
            "report_count": 5,
            "is_suspended": false,
            "created_at": "2024-01-10T08:00:00Z",
            "reports": [
                {
                    "id": 1,
                    "reporter": "johndoe",
                    "reason": "Fraudulent activity",
                    "description": "User tried to sell fake items",
                    "created_at": "2024-01-14T15:30:00Z"
                }
            ]
        }
    ]
}
```

### GET /api/admin/reported-products/
Get reported products.

**Request:**
```bash
GET /api/admin/reported-products/?page=1&page_size=20
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**
```json
{
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 30,
            "name": "Fake Designer Bag",
            "seller_username": "suspicious_user",
            "report_count": 3,
            "is_active": true,
            "created_at": "2024-01-12T11:45:00Z",
            "reports": [
                {
                    "id": 2,
                    "reporter": "janedoe",
                    "reason": "Counterfeit item",
                    "description": "This is clearly a fake designer bag",
                    "created_at": "2024-01-14T16:20:00Z"
                }
            ]
        }
    ]
}
```

### POST /api/admin/users/{userId}/suspend/
Suspend a user.

**Request:**
```bash
POST /api/admin/users/25/suspend/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
    "reason": "Multiple reports of fraudulent activity",
    "duration_days": 30
}
```

**Response (200 OK):**
```json
{
    "message": "User suspended successfully",
    "user_id": 25,
    "suspension_reason": "Multiple reports of fraudulent activity",
    "suspension_end_date": "2024-02-14T15:30:00Z"
}
```

**Error Response (403):**
```json
{
    "detail": "You do not have permission to suspend users. Admin access required."
}
```

### POST /api/admin/users/{userId}/unsuspend/
Unsuspend a user.

**Request:**
```bash
POST /api/admin/users/25/unsuspend/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**
```json
{
    "message": "User unsuspended successfully",
    "user_id": 25,
    "is_active": true
}
```

**Error Response (403):**
```json
{
    "detail": "You do not have permission to unsuspend users. Admin access required."
}
```

### POST /api/admin/products/{productId}/report/
Report a product (admin action).

**Request:**
```bash
POST /api/admin/products/30/report/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
    "reason": "Violation of platform policies",
    "description": "This product violates our terms of service"
}
```

**Response (201 Created):**
```json
{
    "message": "Product reported successfully",
    "report_id": 10,
    "product_id": 30
}
```

### POST /api/admin/users/{userId}/report/
Report a user (admin action).

**Request:**
```bash
POST /api/admin/users/25/report/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
    "reason": "Suspicious activity",
    "description": "User showing signs of fraudulent behavior"
}
```

**Response (201 Created):**
```json
{
    "message": "User reported successfully",
    "report_id": 11,
    "user_id": 25
}
```

### DELETE /api/admin/products/{productId}/
Remove a product (admin action).

**Request:**
```bash
DELETE /api/admin/products/30/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (204 No Content):** (Empty response body)

**Error Response (403):**
```json
{
    "detail": "You do not have permission to remove products. Admin access required."
}
```

### GET /api/admin/users/
Get all users (admin view).

**Request:**
```bash
GET /api/admin/users/?page=1&page_size=20&is_suspended=true
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**
```json
{
    "count": 150,
    "next": "http://localhost:8000/api/admin/users/?page=2&page_size=20&is_suspended=true",
    "previous": null,
    "results": [
        {
            "id": 25,
            "username": "suspicious_user",
            "email": "suspicious@example.com",
            "first_name": "Suspicious",
            "last_name": "User",
            "is_suspended": true,
            "suspension_reason": "Multiple reports of fraudulent activity",
            "suspension_end_date": "2024-02-14T15:30:00Z",
            "report_count": 5,
            "created_at": "2024-01-10T08:00:00Z"
        }
    ]
}
```

---

## System Endpoints

### GET /api/health/
Health check endpoint.

**Response (200):**
```json
{
    "status": "healthy",
    "timestamp": "2024-01-01T12:00:00Z"
}
```

### GET /api/categories/
Get all categories (alternative endpoint).

---

## Error Responses

### 400 Bad Request
```json
{
    "error": "Bad Request",
    "message": "Invalid input data",
    "details": {
        "field_name": ["This field is required."]
    }
}
```

### 401 Unauthorized
```json
{
    "error": "Unauthorized",
    "message": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
    "error": "Forbidden",
    "message": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
    "error": "Not Found",
    "message": "The requested resource was not found."
}
```

### 500 Internal Server Error
```json
{
    "error": "Internal Server Error",
    "message": "An unexpected error occurred."
}
```

---

## Data Models

### User Profile
- `id`: UUID (primary key)
- `user`: Foreign key to User model
- `role`: buyer/seller/admin
- `phone`: Phone number (optional)
- `address`: Text address (optional)
- `date_of_birth`: Date (optional)
- `bio`: Text biography (optional)
- `profile_picture`: Image file (optional)
- `is_seller`: Boolean
- `average_rating`: Decimal (3, 2)
- `total_sales`: Decimal (10, 2)
- `created_at`: DateTime

### Product
- `id`: Integer (primary key)
- `name`: String (max 200)
- `description`: Text
- `price`: Decimal (10, 2)
- `category`: Foreign key to Category
- `user`: Foreign key to User (seller)
- `condition`: Choices (new/like-new/good/fair/poor)
- `location`: String (max 200, optional)
- `image`: Image file (optional)
- `images`: ManyToMany to ProductImage
- `stock`: Positive integer
- `is_active`: Boolean
- `views_count`: Positive integer
- `created_at`: DateTime
- `updated_at`: DateTime

### Order
- `id`: Integer (primary key)
- `buyer`: Foreign key to User
- `seller`: Foreign key to User
- `total_amount`: Decimal (10, 2)
- `status`: Choices (pending/accepted/rejected/completed/cancelled)
- `notes`: Text (optional)
- `created_at`: DateTime
- `updated_at`: DateTime

### Product Review
- `id`: Integer (primary key)
- `product`: Foreign key to Product
- `user`: Foreign key to User
- `rating`: Integer (1-5)
- `comment`: Text
- `created_at`: DateTime
- `updated_at`: DateTime

---

## Usage Examples

### Complete Purchase Flow

1. **Browse Products**
```bash
GET /api/products/?category=Electronics&min_price=100&max_price=500
```

2. **View Product Details**
```bash
GET /api/products/1/
```

3. **Create Order**
```bash
POST /api/orders/create/
Authorization: Bearer <access_token>
{
    "items": [{"product": 1, "quantity": 1}],
    "notes": "Meet at campus library"
}
```

4. **Check Order Status**
```bash
GET /api/orders/purchases/
Authorization: Bearer <access_token>
```

### Complete Selling Flow

1. **Create Product**
```bash
POST /api/products/
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
name: "iPhone 12"
description: "Used iPhone 12 in excellent condition"
price: "400.00"
category: 1
condition: "like-new"
images: [photo1.jpg, photo2.jpg]
```

2. **Manage Sales**
```bash
GET /api/orders/sales/
Authorization: Bearer <access_token>
```

3. **Accept Order**
```bash
POST /api/orders/1/accept/
Authorization: Bearer <access_token>
```

---

## Rate Limiting

- API requests are limited to 1000 requests per hour per user
- File uploads are limited to 10MB per file
- Maximum 5 images per product

## CORS

The API supports CORS for the following origins:
- `http://localhost:3000`
- `http://127.0.0.1:3000`

## Pagination

List endpoints use pagination with:
- Default page size: 20 items
- Maximum page size: 100 items
- Use `page` and `page_size` query parameters

## Search and Filtering

Most list endpoints support:
- Text search in relevant fields
- Filtering by various attributes
- Sorting by created_at, price, name, etc.

## File Uploads

- Profile pictures: Max 5MB, JPG/PNG
- Product images: Max 10MB each, JPG/PNG
- Max 5 images per product

---

## Support

For API support and questions, contact the development team or check the admin panel at `/admin/`.
