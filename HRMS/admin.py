from django.contrib import admin
from .models import Employee, Task, Position

admin.site.register(Employee)
admin.site.register(Position)
admin.site.register(Task)
