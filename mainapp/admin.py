from django.contrib import admin
from .models import SystemUser,Roles,Team,Member,TeamJoin,Category,Product,CategoryProduct,Department,Employee
from django.utils import timezone
from .models import Customer,PlaceOrder
# Register your models here.
# admin.site.register(SystemUser)
admin.site.register(Roles)
admin.site.register(Team)
admin.site.register(Member)
admin.site.register(TeamJoin)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(CategoryProduct)
admin.site.register(Department)
admin.site.register(Employee)
admin.site.register(Customer)
admin.site.register(PlaceOrder)
class SystemUserAdmin(admin.ModelAdmin):
    # Override the delete method to implement soft delete
    def delete_model(self, request, obj):
        obj.is_deleted = True
        obj.deleted_at = timezone.now()  # Optional: track when the user was soft-deleted
        obj.save()

    # Override the delete queryset method for bulk soft delete
    def delete_queryset(self, request, queryset):
        queryset.update(is_deleted=True, deleted_at=timezone.now())  # Optional: track when the users were soft-deleted

# Register the admin
admin.site.register(SystemUser, SystemUserAdmin)