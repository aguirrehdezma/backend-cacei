from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from usuarios_y_acceso.views import (
    RegisterView,
    UserProfileView,
    ChangePasswordView,
    UserListView,
)

app_name = 'usuarios_y_acceso'

urlpatterns = [
    # Autenticación
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Perfil de usuario
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    
    # Administración de usuarios (solo admins)
    path('users/', UserListView.as_view(), name='user_list'),
]
