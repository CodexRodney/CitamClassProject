from django.urls import path
from .views import RegisterAdminApiView, LoginApiView, CreateClassAPI


urlpatterns = [
    path('signup/', RegisterAdminApiView.as_view(), name="administrator_signup"),
    path('login/', LoginApiView.as_view(), name="login"),
    path('classrooms/', CreateClassAPI.as_view(), name="classrooms"),
]
