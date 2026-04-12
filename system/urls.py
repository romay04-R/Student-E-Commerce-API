from django.urls import path
from .views import health_check, get_categories

urlpatterns = [
    path('health/', health_check, name='health-check'),
    path('categories/', get_categories, name='get-categories'),
]
