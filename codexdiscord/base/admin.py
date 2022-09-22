from django.contrib import admin
from .models import Rooms ,Topic, Messages
# socialadmin
# Register your models here.


admin.site.register((Rooms, Topic, Messages))
