from django.urls import path
from seller import views

urlpatterns = [
    path("dashboard/", views.sller_dashboad, name="seller_dashboard"),
]
