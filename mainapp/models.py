from django.db import models
from django.contrib.auth.models import User,Group
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
class Roles(Group):
    is_active = models.BooleanField(default=True)

class SystemUser(User):
    mobile_no = models.PositiveBigIntegerField(
        validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)],
        unique=True
    )
    otp = models.IntegerField(default=0)
    expiry_time = models.DateTimeField(default=timezone.now)
    profile_image = models.ImageField(upload_to='profile_image/')
    role_id = models.ForeignKey(Roles, on_delete=models.DO_NOTHING)
    is_deleted = models.BooleanField(default=False)



