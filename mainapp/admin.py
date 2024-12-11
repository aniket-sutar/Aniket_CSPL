from django.contrib import admin
from .models import SystemUser,Roles
# Register your models here.
admin.site.register(SystemUser)
admin.site.register(Roles)