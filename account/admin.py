from django.contrib import admin
from .models import User
# Register your models here.
@admin.register(User)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [ 'username', 'email','password','phone','profile_pic', 'file','Reg_id']
