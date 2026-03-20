from django.db import models

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    class Meta:
        abstract = True

class Department(BaseModel):
    name = models.CharField(max_length=100, unique=True, db_index=True)

    class Meta:
        db_table = "department"

    def __str__(self):
        return self.name

class Employee(BaseModel):
    employee_id = models.CharField(max_length=50, unique=True, db_index=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name="employees")
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "employee"

    def __str__(self):
        return f"{self.full_name} ({self.employee_id})"


class Attendance(BaseModel):
    STATUS_CHOICES = [
        ("Present", "Present"),
        ("Absent", "Absent"),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="attendances")
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        db_table = "attendance"
        unique_together = ("employee", "date")
        ordering = ["-date"]

    def __str__(self):
        return f"{self.employee.full_name} - {self.date} - {self.status}"
