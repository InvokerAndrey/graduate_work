from django.contrib import admin
from .models import Employee, Education, Experience, Task, Position

admin.site.register(Employee)
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(Position)
admin.site.register(Task)
