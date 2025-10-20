from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from employees.views import (
    EmployeeViewSet, LeaveRequestViewSet, AttendanceViewSet,
    login_view, logout_view, current_user, register_view,csrf_token_view
)
from employees.views import admin_login_view
# 添加CSRF token视图
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from django.middleware.csrf import get_token
from employees.views import (
    AdminEmployeeListView, AdminEmployeeDetailView,
    UserLeaveRequestListView, UserLeaveRequestDetailView,
    AdminLeaveRequestListView, AdminLeaveRequestDetailView,
    UserAttendanceListView, UserAttendanceDetailView,
    AdminAttendanceListView, AdminAttendanceDetailView
)


router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'leave-requests', LeaveRequestViewSet)
router.register(r'attendance', AttendanceViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/login/', login_view),
    
    path('api/logout/', logout_view),
    path('api/register/', register_view),
    path('api/current-user/', current_user),
    # In your urls.py
    path('api/admin/login/', admin_login_view, name='admin_login'),
    path('api/admin/csrf-token/', csrf_token_view, name='csrf_token'),
    # 员工管理接口 (管理员)
    path('api/admin/employees/', AdminEmployeeListView.as_view(), name='admin-employee-list'),
    path('api/admin/employees/<int:pk>/', AdminEmployeeDetailView.as_view(), name='admin-employee-detail'),
    
    # 请假请求接口
    path('api/leave-requests/', UserLeaveRequestListView.as_view(), name='user-leave-request-list'),
    path('api/leave-requests/<int:pk>/', UserLeaveRequestDetailView.as_view(), name='user-leave-request-detail'),
    path('api/admin/leave-requests/', AdminLeaveRequestListView.as_view(), name='admin-leave-request-list'),
    path('api/admin/leave-requests/<int:pk>/', AdminLeaveRequestDetailView.as_view(), name='admin-leave-request-detail'),
    
    # 考勤接口
    path('api/attendance/', UserAttendanceListView.as_view(), name='user-attendance-list'),
    path('api/attendance/<int:pk>/', UserAttendanceDetailView.as_view(), name='user-attendance-detail'),
    path('api/admin/attendance/', AdminAttendanceListView.as_view(), name='admin-attendance-list'),
    path('api/admin/attendance/<int:pk>/', AdminAttendanceDetailView.as_view(), name='admin-attendance-detail'),
]