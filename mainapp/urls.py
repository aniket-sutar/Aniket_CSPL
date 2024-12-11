from django.urls import path
from .views import LoginView,RoleCreateView,SystemUserCreateView
from mainapp import views

urlpatterns = [
    path('login/',LoginView.as_view(),name='login'),
    path('role-create/',RoleCreateView.as_view(),name='role-create'),
    path('user-create/',SystemUserCreateView.as_view(),name='user-create'),
    path('user/<int:user_id>/', views.get_user, name='get_user'),
]
