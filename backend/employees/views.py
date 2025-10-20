from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Employee, LeaveRequest, Attendance
from .serializers import EmployeeSerializer, LeaveRequestSerializer, AttendanceSerializer

class EmployeeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

class LeaveRequestViewSet(viewsets.ModelViewSet):
    queryset = LeaveRequest.objects.none() 
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            # HR or admin can see all requests
            return LeaveRequest.objects.all()
        else:
            # Regular employees can only see their own requests
            try:
                employee = Employee.objects.get(user=user)
                return LeaveRequest.objects.filter(employee=employee)
            except Employee.DoesNotExist:
                return LeaveRequest.objects.none()
    
    def perform_create(self, serializer):
        user = self.request.user
        try:
            employee = Employee.objects.get(user=user)
            serializer.save(employee=employee)
        except Employee.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Employee profile not found'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        if not request.user.is_staff:
            return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        leave_request = self.get_object()
        leave_request.status = 'approved'
        leave_request.reviewed_by = request.user
        leave_request.review_date = timezone.now()
        leave_request.save()
        
        serializer = self.get_serializer(leave_request)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        if not request.user.is_staff:
            return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        leave_request = self.get_object()
        leave_request.status = 'rejected'
        leave_request.reviewed_by = request.user
        leave_request.review_date = timezone.now()
        leave_request.save()
        
        serializer = self.get_serializer(leave_request)
        return Response(serializer.data)

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.none()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Attendance.objects.all()
        else:
            try:
                employee = Employee.objects.get(user=user)
                return Attendance.objects.filter(employee=employee)
            except Employee.DoesNotExist:
                return Attendance.objects.none()
    
    def perform_create(self, serializer):
        user = self.request.user
        try:
            employee = Employee.objects.get(user=user)
            serializer.save(employee=employee)
        except Employee.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Employee profile not found'
            }, status=status.HTTP_400_BAD_REQUEST)

# Authentication views
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_staff': user.is_staff
            }
        })
    else:
        return Response({
            'success': False,
            'message': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({'success': True})

@api_view(['GET'])
def current_user(request):
    if request.user.is_authenticated:
        try:
            employee = Employee.objects.get(user=request.user)
            employee_data = EmployeeSerializer(employee).data
        except Employee.DoesNotExist:
            employee_data = None
            
        return Response({
            'user': {
                'id': request.user.id,
                'username': request.user.username,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'is_staff': request.user.is_staff
            },
            'employee': employee_data
        })
    else:
        return Response({'user': None})
    
# 在文件末尾添加以下代码

from django.contrib.auth.models import User
from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    try:
        with transaction.atomic():
            # 创建用户
            user = User.objects.create_user(
                username=request.data.get('username'),
                email=request.data.get('email'),
                password=request.data.get('password'),
                first_name=request.data.get('first_name'),
                last_name=request.data.get('last_name')
            )
            
            # 创建员工档案
            employee = Employee.objects.create(
                user=user,
                employee_id=request.data.get('employee_id'),
                department=request.data.get('department'),
                position=request.data.get('position'),
                hire_date=request.data.get('hire_date')
            )
            
            return Response({
                'success': True,
                'message': 'User registered successfully'
            })
    except Exception as e:
        return Response({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
# 在 employees/views.py 中添加
from rest_framework.decorators import action

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]
    
    # 只允许管理员访问
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]