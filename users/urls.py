
from users.views import UserAPIView, Login
from django.urls import path


urlpatterns = [

    path('', UserAPIView.as_view(), name='user'),
    path('login/', Login.as_view()),
]