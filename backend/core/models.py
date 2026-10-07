from django.core.validators import MaxValueValidator, MinValueValidator
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


class Demand(models.Model):
    class Source(models.TextChoices):
        MANAGER_ENTERED = 'manager_entered', 'Manager entered'
        ML_PREDICTED = 'ml_predicted', 'ML predicted'
        ESTIMATED = 'estimated', 'Estimated'

    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    date = models.DateField()
    hour = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(23)])
    expected_customers = models.IntegerField()
    cages_waiting = models.IntegerField()
    source = models.CharField(max_length=20, choices=Source.choices, default=Source.MANAGER_ENTERED)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['zone', 'date', 'hour'], name='unique_zone_date_hour'),
        ]

    def __str__(self):
        return f'{self.zone} {self.date} {self.hour:02d}:00'


class Task(models.Model):
    class TaskType(models.TextChoices):
        RECOVERY = 'recovery', 'Recovery'
        GAP = 'gap', 'Gap'
        TROLLEY = 'trolley', 'Trolley'

    class Source(models.TextChoices):
        MANAGER_ENTERED = 'manager_entered', 'Manager entered'
        ESTIMATED = 'estimated', 'Estimated'
        ML_PREDICTED = 'ml_predicted', 'ML predicted'

    # Blank zone means the task is store-wide.
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    task_type = models.CharField(max_length=10, choices=TaskType.choices)
    minutes_required = models.IntegerField()
    # Blank deadline_hour means no deadline.
    deadline_hour = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(23)]
    )
    source = models.CharField(max_length=20, choices=Source.choices, default=Source.MANAGER_ENTERED)

    def __str__(self):
        zone = self.zone or 'Store-wide'
        return f'{zone} {self.task_type} {self.date} ({self.minutes_required} min)'
