from django.contrib import admin
from .models import SystemUser,Roles,Team,Member,TeamJoin,Category,Product,CategoryProduct,Department,Employee
from django.utils import timezone
from .models import Customer,PlaceOrder,Blog,ParentChildCategory,ParentChildProduct
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



@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    fields = ('title', 'slug', 'author', 'content', 'status', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    
    list_display = ('id', 'title', 'author', 'status', 'created_at', 'updated_at')
    list_filter = ('status','is_deleted',)
    search_fields = ('title', 'content', 'author__username') 
    ordering = ('id',)

@admin.register(ParentChildCategory)
class ParentChildCategoryAdmin(admin.ModelAdmin):
    fields = ('id','name','desc','parent','is_active')
    readonly_fields = ('id',)

    list_display = ('id','name','desc','parent','is_active')
    list_filter = ('is_active',)
    search_fields = ('name','parent',)
    ordering = ('id',)

@admin.register(ParentChildProduct)
class ParentChildProductAdmin(admin.ModelAdmin):
    fields = ('name','price','cat','is_active')
    readonly_fields = ('id',)

    list_display = ('id','name','price','cat','is_active')
    list_filter = ('price','is_active')
    search_fields = ('name','cat')
    ordering = ('id','price',)

@admin.register(SystemUser)
class SystemUserAdmin(admin.ModelAdmin):
    def delete_model(self, request, obj):
        obj.is_deleted = True
        obj.deleted_at = timezone.now()
        obj.save()
    def delete_queryset(self, request, queryset):
        queryset.update(is_deleted=True, deleted_at=timezone.now())