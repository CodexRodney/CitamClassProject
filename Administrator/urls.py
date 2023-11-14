from django.urls import path
from .views import RegisterAdminApiView


urlpatterns = [
    path('signup/', RegisterAdminApiView.as_view(), name="administrator_signup"),
]
