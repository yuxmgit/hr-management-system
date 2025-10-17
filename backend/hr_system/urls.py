from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from employees.views import (
    EmployeeViewSet, LeaveRequestViewSet, AttendanceViewSet,
    login_view, logout_view, current_user, register_view
)

# 添加CSRF token视图
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from django.middleware.csrf import get_token

@ensure_csrf_cookie
def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({'csrfToken': token})

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
    path('api/csrf/', get_csrf_token),  # 添加CSRF token接口
]