from rest_framework import serializers
from Schema.models import Employee, Attendance, Department

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"

class EmployeeSerializer(serializers.ModelSerializer):
    total_present_days = serializers.SerializerMethodField()
    monthly_attendance_percentage = serializers.SerializerMethodField()
    department_name = serializers.CharField(source="department.name", read_only=True)

    class Meta:
        model = Employee
        fields = "__all__"

    def get_total_present_days(self, obj):
        return obj.attendances.filter(status="Present").count()

    def get_monthly_attendance_percentage(self, obj):
        from datetime import date
        today = date.today()
        records = obj.attendances.filter(date__year=today.year, date__month=today.month)
        total = records.count()
        if total == 0:
            return 0
        present = records.filter(status="Present").count()
        return round((present / total) * 100)

class AttendanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source="employee.full_name", read_only=True)
    employee_id_code = serializers.CharField(source="employee.employee_id", read_only=True)

    class Meta:
        model = Attendance
        fields = ["id", "employee", "employee_name", "employee_id_code", "date", "status"]

    def validate(self, data):
        # Enforce unique together manually to give better error messages
        employee = data.get("employee")
        date = data.get("date")
        if Attendance.objects.filter(employee=employee, date=date).exists():
            raise serializers.ValidationError({"date": "Attendance for this employee on this date already exists."})
        return data
