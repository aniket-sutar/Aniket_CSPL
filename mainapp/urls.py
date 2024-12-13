from django.urls import path
from .views import LoginView,RoleCreateView
from mainapp import views

urlpatterns = [
    path('login/',LoginView.as_view(),name='login'),
    path('role-create/',RoleCreateView.as_view(),name='role-create'),

    path('user/<int:user_id>/',views.get_user, name='get_user'),
    path('user-create/',views.create_system_user,name='user-create'),
    path('user-update/<int:user_id>/',views.update_user,name='update-user'),
    path('user-delete/<int:user_id>',views.delete_user,name='delete-user'),

    path('user-roles-fetch',views.fetch_user_roles,name='user-roles-fetch'),
    path('role-category-users/<int:id>/',views.role_specific_fetch_users_byid,name='role-category-user-byid'),
    path('role-category-users/<str:name>/',views.role_specific_fetch_users_byname,name='role-category-users-byname'),
    # path('user/<int:user_id>/', views.get_user, name='get_user'),

    path('send-otp/',views.send_otp,name='send-otp'),
    path('verify-otp/',views.verify_otp,name='verify-otp'),
]
