from django.urls import path

from . import views

app_name = 'shop'
urlpatterns = [
    path('checkout/<int:pk>/', views.CheckoutView.as_view(), name='checkout'),
]
