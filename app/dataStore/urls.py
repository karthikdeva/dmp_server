# from .views import LoginAPI, RegisterAPI, UserAPI, ChangePasswordView
from django.urls import include, path

from app.dataStore.views import CitizenView, MyTokenObtainPairView, CustomTokenObtainView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', CitizenView.as_view(), name="citizen"),
    path('auth/', MyTokenObtainPairView.as_view(), name="auth"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    #  path('api/auth/', include('djoser.urls.authtoken')),
    # path('api/register/', RegisterAPI.as_view(), name='register'),
    # path('api/login/', LoginAPI.as_view(), name='login'),
    # path('api/user/', UserAPI.as_view(), name='user'),
    # path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
]
