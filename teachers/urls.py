from django.urls import path
from .views import ClassesAPIView, AttendanceAPIView, ListStudentsAPIView

urlpatterns = [
    path("get-classes/", ClassesAPIView.as_view(), name="get_classes"),
    path("mark-attendance/", AttendanceAPIView.as_view(), name="mark_attendance"),
    path("list-students/", ListStudentsAPIView.as_view(), name="list-students")
]
