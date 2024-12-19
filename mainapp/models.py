from django.db import models
from django.contrib.auth.models import User,Group
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class NonDeletedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    objects = NonDeletedManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

class Roles(Group,SoftDeleteModel):
    is_active = models.BooleanField(default=True)

class SystemUser(User,SoftDeleteModel):
    mobile_no = models.PositiveBigIntegerField(
        validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)],
        unique=True
    )
    otp = models.IntegerField(default=0)
    expiry_time = models.DateTimeField(default=timezone.now)
    profile_image = models.ImageField(upload_to='profile_image/')
    role_id = models.ForeignKey(Roles, on_delete=models.DO_NOTHING) 

# class Tag(models.Model):
#     tag_name = models.CharField(max_length=80, unique=True)

#     def __str__(self):
#         return f"{self.tag_name}"

# class Product(models.Model):
#     prod_name = models.CharField(max_length=50)
#     prod_desc = models.TextField()

#     def __str__(self):
#         return self.prod_name

# class ProductTagJoin(models.Model):
#     tag = models.ForeignKey(Tag, on_delete=models.DO_NOTHING, related_name="product_tags")
#     product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name="tagged_products")
#     is_active = models.BooleanField(default=True)

#     def __str__(self):
#         return f"{self.product.prod_name} tagged with {self.tag.tag_name}"
    
class Member(SoftDeleteModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Team(SoftDeleteModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class TeamJoin(SoftDeleteModel):
    team = models.ForeignKey(Team, on_delete=models.PROTECT)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    points = models.IntegerField()

    class Meta:
        unique_together = ('team', 'member')

class Category(SoftDeleteModel):
    cat_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

class Product(SoftDeleteModel):
    prod_name = models.CharField(max_length=50)
    price = models.IntegerField()
    desc = models.CharField(max_length=250)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.prod_name
    
class CategoryProduct(SoftDeleteModel):
    cat_id = models.ForeignKey(Category,on_delete=models.DO_NOTHING)
    prod_id = models.ForeignKey(Product,on_delete=models.DO_NOTHING)

class Department(SoftDeleteModel):
    dept_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.dept_name

class Employee(SoftDeleteModel):
    emp_name = models.CharField(max_length=50)
    emp_age = models.IntegerField()
    dept_id = models.ForeignKey(Department,on_delete=models.DO_NOTHING,null=True,blank=True,related_name='employees')
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.emp_name
    
class Customer(SoftDeleteModel):
    cust_name = models.CharField(max_length=50)
    cust_email = models.EmailField()
    mobile_no = models.PositiveBigIntegerField(
        validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)],
        unique=True
    )
    cust_address = models.TextField()

    def __str__(self):
        return self.cust_name
    
class PlaceOrder(SoftDeleteModel):
    order_status = models.CharField(
    max_length=10,
    choices=[('PENDING', 'Pending'), ('COMPLETED', 'Completed'), ('CANCELED', 'Canceled')],
    default='PENDING'
    )
    payment_type = models.CharField(
    max_length=10,
    choices=[('ONLINE', 'Online'), ('COD', 'COD'), ('CASH', 'Cash')],
    default='CASH'
    )  
    cust_id = models.ForeignKey(Customer,on_delete=models.DO_NOTHING,null=True,blank=True)
    prod_id = models.ForeignKey(Product,on_delete=models.DO_NOTHING,null=True,blank=True)
    quantity = models.IntegerField()
    amount = models.IntegerField()
    total_amount = models.DecimalField(max_digits=9,decimal_places=2)
    delivery_charges = models.IntegerField()
    discount = models.DecimalField(max_digits=4,decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    

