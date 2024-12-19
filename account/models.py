import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    email=models.EmailField(unique=True, blank=True)
    phone = models.CharField(max_length=11, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    file=models.FileField(upload_to='files', blank=True)
    Reg_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


