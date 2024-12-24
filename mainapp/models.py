from django.db import models
from django.contrib.auth.models import User,Group
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.utils.text import slugify


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


class Blog(SoftDeleteModel):
    status_choice =[
        ('draft','Draft'),
        ('published','Published')
    ]

    title = models.CharField(max_length=150,unique=True)
    slug = models.SlugField(max_length=150,unique=True,blank=True)
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True,blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30,choices=status_choice,default='draft')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

class ParentChildCategory(SoftDeleteModel):
    name = models.CharField(max_length=50)
    desc = models.TextField()
    parent = models.ForeignKey('self',on_delete=models.DO_NOTHING,null=True,blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class ParentChildProduct(SoftDeleteModel):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    cat = models.ForeignKey(ParentChildCategory,on_delete=models.DO_NOTHING,null=True,blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name