from django.contrib import admin

from .models import Aisle, Demand, Employee, EmployeeSkill, EmployeeTaskSpeed, Skill, Task, Zone

admin.site.register(Employee)
admin.site.register(Skill)
admin.site.register(EmployeeSkill)
admin.site.register(EmployeeTaskSpeed)
admin.site.register(Zone)
admin.site.register(Aisle)
admin.site.register(Demand)
admin.site.register(Task)
