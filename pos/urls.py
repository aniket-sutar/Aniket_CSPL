from django.contrib import admin
from django.urls import path,include
from mainapp.views import ProductViewset,CategoryViewset,ProductModelViewset,DepartmentView,EmployeeView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'products',ProductViewset,basename='product')
router.register(r'category',CategoryViewset,basename='category')
router.register(r'prodmodel',ProductModelViewset,basename='prodmodel')
router.register(r'department',DepartmentView,basename='department')
router.register(r'employee',EmployeeView,basename='employee')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('mainapp.urls')),
    path('cat-prod/',include(router.urls)),
]
