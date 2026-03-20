from django.urls import path
from api.views import (
    EmployeeListCreateView, 
    EmployeeDetailView, 
    DepartmentListCreateView,
    DepartmentDetailView,
    AttendanceListCreateView, 
    DashboardStatsView,
    AnalyticsDashboardView,
    ReportSummaryView
)

urlpatterns = [
    path("employees/", EmployeeListCreateView.as_view(), name="employee-list-create"),
    path("employees/<int:pk>/", EmployeeDetailView.as_view(), name="employee-detail"),
    path("departments/", DepartmentListCreateView.as_view(), name="department-list-create"),
    path("departments/<int:pk>/", DepartmentDetailView.as_view(), name="department-detail"),
    path("attendance/", AttendanceListCreateView.as_view(), name="attendance-list-create"),
    path("dashboard/stats/", DashboardStatsView.as_view(), name="dashboard-stats"),
    path("analytics/dashboard/", AnalyticsDashboardView.as_view(), name="analytics-dashboard"),
    path("reports/summary/", ReportSummaryView.as_view(), name="report-summary"),
]
