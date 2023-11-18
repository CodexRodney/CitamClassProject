from django.urls import path
from .views import ClassesAPIView

urlpatterns = [
    path("get-classes/", ClassesAPIView.as_view(), name="get_classes"),
]
