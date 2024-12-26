from django.urls import path,include
from .views import LoginView,RoleCreateView,RolesCRUD,PlacedOrderView,OrderHistory,BlogViewSet,DisplayProductByCategory
from mainapp import views
from rest_framework import routers


blog_router = routers.DefaultRouter()
blog_router.register(r'blogs', BlogViewSet, basename='blog')


urlpatterns = [
    path('',views.Home,name='home'),

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

    path('role/',RolesCRUD.as_view(),name='roleread'),
    path('role/<int:id>/',RolesCRUD.as_view(),name='role-get-delete'),

    # path('tag-create/',Tagcreate.as_view(),name='tag-create'),
    # path('product-create/',ProductView.as_view(),name='product-create'),
    # path('product-update/<int:product_id>/',ProductView.as_view(),name='product-update'),
    path('update-team-members/',views.update_team_members,name='update-team-members'),
    path('alldata/',views.get_all_teams_and_members,name='alldata'),

    path('prod-fun-pagination/',views.ProductPaginationData,name='prod-fun-pagination'),

    path('place-order/',PlacedOrderView.as_view(),name='place-order'),
    path('order-history/',OrderHistory.as_view(),name='order-history'),

    path('blog/',include(blog_router.urls)),
    path('parentchild/<int:id>/',DisplayProductByCategory.as_view(),name='parentchild'),
]
