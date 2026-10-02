from django.db import models


class Speed(models.TextChoices):
    FAST = 'fast', 'Fast'
    MEDIUM = 'medium', 'Medium'
    SLOW = 'slow', 'Slow'


class Employee(models.Model):
    class ExperienceLevel(models.TextChoices):
        SENIOR = 'senior', 'Senior'
        MEDIUM = 'medium', 'Medium'
        BEGINNER = 'beginner', 'Beginner'

    class EmploymentType(models.TextChoices):
        FULL_TIME = 'full_time', 'Full time'
        PART_TIME = 'part_time', 'Part time'
        CASUAL = 'casual', 'Casual'

    name = models.CharField(max_length=100)
    experience_level = models.CharField(max_length=10, choices=ExperienceLevel.choices)
    employment_type = models.CharField(max_length=10, choices=EmploymentType.choices)
    active = models.BooleanField(default=True)
    max_hours_per_week = models.IntegerField()

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class EmployeeSkill(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    allowed = models.BooleanField()
    customer_speed = models.CharField(max_length=10, choices=Speed.choices)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['employee', 'skill'], name='unique_employee_skill'),
        ]

    def __str__(self):
        return f'{self.employee} - {self.skill}'


class EmployeeTaskSpeed(models.Model):
    class TaskType(models.TextChoices):
        CAGE = 'cage', 'Cage'
        RECOVERY = 'recovery', 'Recovery'
        GAP = 'gap', 'Gap'
        TROLLEY = 'trolley', 'Trolley'

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    task_type = models.CharField(max_length=10, choices=TaskType.choices)
    speed = models.CharField(max_length=10, choices=Speed.choices)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['employee', 'task_type'], name='unique_employee_task_type'),
        ]

    def __str__(self):
        return f'{self.employee} - {self.task_type}'


class Zone(models.Model):
    name = models.CharField(max_length=100, unique=True)
    base_staff = models.IntegerField()

    def __str__(self):
        return self.name


class Aisle(models.Model):
    class DemandLevel(models.TextChoices):
        VERY_BUSY = 'very_busy', 'Very busy'
        MEDIUM = 'medium', 'Medium'
        QUIET = 'quiet', 'Quiet'

    name = models.CharField(max_length=100, unique=True)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    demand_level = models.CharField(max_length=10, choices=DemandLevel.choices)

    def __str__(self):
        return self.name
