from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from datetime import date, timedelta

from Schema.models import Employee, Attendance, Department
from api.serializers import EmployeeSerializer, AttendanceSerializer, DepartmentSerializer

class DepartmentListCreateView(APIView):
    def get(self, request):
        departments = Department.objects.all().order_by("-created_at")
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DepartmentDetailView(APIView):
    def put(self, request, pk):
        department = get_object_or_404(Department, pk=pk)
        serializer = DepartmentSerializer(department, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        department = get_object_or_404(Department, pk=pk)
        if department.employees.exists():
            return Response({"error": "Cannot delete department with assigned employees."}, status=status.HTTP_400_BAD_REQUEST)
        department.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class EmployeeListCreateView(APIView):
    def get(self, request):
        employees = Employee.objects.filter(is_active=True).order_by("-created_at")

        search = request.query_params.get("search")
        department = request.query_params.get("department")

        if search:
            employees = employees.filter(
                Q(full_name__icontains=search) | 
                Q(email__icontains=search)
            )
        if department:
            employees = employees.filter(department__name__icontains=department)

        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeDetailView(APIView):
    def put(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk, is_active=True)
        # partial=True allows updates without sending all fields
        serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        hard_delete = request.query_params.get("hard_delete", "false").lower() == "true"

        if hard_delete:
            employee.delete()
        else:
            employee.is_active = False
            employee.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

class AttendanceListCreateView(APIView):
    def get(self, request):
        attendances = Attendance.objects.all().select_related("employee")

        # Optional filters
        employee_id = request.query_params.get("employee_id")
        filter_date = request.query_params.get("date")

        if employee_id:
            attendances = attendances.filter(employee_id=employee_id)
        if filter_date:
            attendances = attendances.filter(date=filter_date)

        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DashboardStatsView(APIView):
    def get(self, request):
        today = date.today()
        total_employees = Employee.objects.filter(is_active=True).count()
        present_today = Attendance.objects.filter(date=today, status="Present").count()
        absent_today = Attendance.objects.filter(date=today, status="Absent").count()

        return Response({
            "total_employees": total_employees,
            "present_today": present_today,
            "absent_today": absent_today,
            "date": today
        })

class AnalyticsDashboardView(APIView):
    def get(self, request):
        today = date.today()

        # 1. Today"s Attendance Pie
        present_today = Attendance.objects.filter(date=today, status="Present").count()
        absent_today = Attendance.objects.filter(date=today, status="Absent").count()
        today_attendance = [
            {"name": "Present", "value": present_today, "color": "#10B981"},
            {"name": "Absent", "value": absent_today, "color": "#EF4444"}
        ]

        # 2. Department Employee Distribution Bar
        dept_dist = Department.objects.annotate(employee_count=Count("employees", filter=Q(employees__is_active=True))).values("name", "employee_count")
        department_distribution = [{"name": d["name"], "count": d["employee_count"]} for d in dept_dist]

        # 3. Weekly Trend (Last 7 days)
        last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]
        weekly_trend = []
        for d in last_7_days:
            p_count = Attendance.objects.filter(date=d, status="Present").count()
            a_count = Attendance.objects.filter(date=d, status="Absent").count()
            weekly_trend.append({"date": d.strftime("%m/%d"), "present": p_count, "absent": a_count})

        return Response({
            "today_attendance": today_attendance,
            "department_distribution": department_distribution,
            "weekly_trend": weekly_trend
        })

class ReportSummaryView(APIView):
    def get(self, request):
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        department_name = request.query_params.get("department")

        employees = Employee.objects.filter(is_active=True)
        if department_name:
            employees = employees.filter(department__name__icontains=department_name)

        attendances = Attendance.objects.all()
        if start_date:
            attendances = attendances.filter(date__gte=start_date)
        if end_date:
            attendances = attendances.filter(date__lte=end_date)

        report_data = []
        for emp in employees:
            emp_attendances = attendances.filter(employee=emp)
            total_present = emp_attendances.filter(status="Present").count()
            total_absent = emp_attendances.filter(status="Absent").count()
            total_days = emp_attendances.count()
            attendance_percent = round((total_present / total_days * 100)) if total_days > 0 else 0

            report_data.append({
                "employee_id": emp.employee_id,
                "full_name": emp.full_name,
                "department": emp.department.name if emp.department else "None",
                "total_present": total_present,
                "total_absent": total_absent,
                "attendance_percent": attendance_percent
            })

        return Response(report_data)