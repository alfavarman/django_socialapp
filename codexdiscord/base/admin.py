from django.contrib import admin
from .models import User, Rooms, Topic, Messages
# socialadmin
# Register your models here.


admin.site.register((User, Rooms, Topic, Messages))
