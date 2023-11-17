from django.urls import path
from .views import RegisterUsersApiView, LoginApiView, CreateClassAPI
from .views import PupilsAPI


urlpatterns = [
    path('signup/', RegisterUsersApiView.as_view(), name="administrator_signup"),
    path('login/', LoginApiView.as_view(), name="login"),
    path('classrooms/', CreateClassAPI.as_view(), name="classrooms"),
    path('pupils/', PupilsAPI.as_view(), name="pupils")
]
