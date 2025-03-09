from django.urls import path
from customer import views

urlpatterns = [
    path("dashboard/", views.customer_dashboad ,name="customer_dashboard"),
    path("change_password/", views.change_password ,name="change_password"),
]