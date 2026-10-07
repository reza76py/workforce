from .models import Employee


def get_available_employees():
    """Return all active employees as a list."""
    return list(Employee.objects.filter(active=True))
