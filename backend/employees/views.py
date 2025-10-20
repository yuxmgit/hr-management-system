from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Employee, LeaveRequest, Attendance
from .serializers import EmployeeSerializer, LeaveRequestSerializer, AttendanceSerializer
from django.middleware.csrf import get_token
from django.http import JsonResponse

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
        print(f"Received data: {serializer.validated_data}")  # Debug log
        try:
            employee = Employee.objects.get(user=user)
            instance = serializer.save(employee=employee)
            print(f"Attendance record saved: {instance.id}")  # Debug log
            return Response({
                'success': True,
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        except Employee.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Employee profile not found'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Error saving attendance: {e}")  # Debug log
            return Response({
                'success': False,
                'message': str(e)
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
        print(f"Received data: {serializer.validated_data}")  # Debug log
        try:
            employee = Employee.objects.get(user=user)
            instance = serializer.save(employee=employee)
            print(f"Attendance record saved: {instance.id}")  # Debug log
            return Response({
                'success': True,
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        except Employee.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Employee profile not found'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Error saving attendance: {e}")  # Debug log
            return Response({
                'success': False,
                'message': str(e)
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
    
# In employees/views.py

@api_view(['POST'])
@permission_classes([AllowAny])
def admin_login_view(request):
    """
    Dedicated login endpoint for admin users
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    # Check if user exists and is staff/admin
    if user is not None and user.is_staff:
        login(request, user)
        return Response({
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser
            }
        })
    elif user is not None and not user.is_staff:
        return Response({
            'success': False,
            'message': 'User is not authorized to access admin panel'
        }, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({
            'success': False,
            'message': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['GET'])
@permission_classes([AllowAny])
def csrf_token_view(request):
    """
    Endpoint to get CSRF token
    """
    csrf_token = get_token(request)
    return Response({'csrfToken': csrf_token})

# 在文件末尾添加以下代码
class AdminEmployeeListView(APIView):
    """
    管理员查看和创建员工列表
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=403)
        
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=403)
        
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class AdminEmployeeDetailView(APIView):
    """
    管理员查看、更新和删除特定员工
    """
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            return None
    
    def get(self, request, pk):
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=403)
            
        employee = self.get_object(pk)
        if not employee:
            return Response({'error': 'Employee not found'}, status=404)
            
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)
    
    def put(self, request, pk):
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=403)
            
        employee = self.get_object(pk)
        if not employee:
            return Response({'error': 'Employee not found'}, status=404)
            
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, pk):
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=403)
            
        employee = self.get_object(pk)
        if not employee:
            return Response({'error': 'Employee not found'}, status=404)
            
        employee.delete()
        return Response(status=204)
    
class UserLeaveRequestListView(APIView):
    """
    用户查看和创建自己的请假请求
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        leave_requests = LeaveRequest.objects.filter(employee__user=request.user)
        serializer = LeaveRequestSerializer(leave_requests, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        try:
            employee = Employee.objects.get(user=request.user)
        except Employee.DoesNotExist:
            return Response({'error': 'Employee profile not found'}, status=404)
            
        serializer = LeaveRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(employee=employee)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class UserLeaveRequestDetailView(APIView):
    """
    用户查看、更新和删除自己的请假请求
    """
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk, user):
        try:
            return LeaveRequest.objects.get(pk=pk, employee__user=user)
        except LeaveRequest.DoesNotExist:
            return None
    
    def get(self, request, pk):
        leave_request = self.get_object(pk, request.user)
        if not leave_request:
            return Response({'error': 'Leave request not found'}, status=404)
            
        serializer = LeaveRequestSerializer(leave_request)
        return Response(serializer.data)
    
    def put(self, request, pk):
        leave_request = self.get_object(pk, request.user)
        if not leave_request:
            return Response({'error': 'Leave request not found'}, status=404)
            
        # 只能更新状态为pending的请假请求
        if leave_request.status != 'pending':
            return Response({'error': 'Cannot modify non-pending leave request'}, status=400)
            
        serializer = LeaveRequestSerializer(leave_request, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, pk):
        leave_request = self.get_object(pk, request.user)
        if not leave_request:
            return Response({'error': 'Leave request not found'}, status=404)
            
        # 只能删除状态为pending的请假请求
        if leave_request.status != 'pending':
            return Response({'error': 'Cannot delete non-pending leave request'}, status=400)
            
        leave_request.delete()
        return Response(status=204)

class AdminLeaveRequestListView(APIView):
    """
    管理员查看所有请假请求
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=403)
            
        leave_requests = LeaveRequest.objects.all()
        serializer = LeaveRequestSerializer(leave_requests, many=True)
        return Response(serializer.data)

class AdminLeaveRequestDetailView(APIView):
    """
    管理员审批请假请求
    """
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return LeaveRequest.objects.get(pk=pk)
        except LeaveRequest.DoesNotExist:
            return None
    
    def put(self, request, pk):
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=403)
            
        leave_request = self.get_object(pk)
        if not leave_request:
            return Response({'error': 'Leave request not found'}, status=404)
            
        # 只能审批状态为pending的请假请求
        if leave_request.status != 'pending':
            return Response({'error': 'Leave request already processed'}, status=400)
            
        serializer = LeaveRequestSerializer(leave_request, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
class UserAttendanceListView(APIView):
    """
    用户查看和创建自己的考勤记录
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # 支持按日期筛选
        date_param = request.GET.get('date', None)
        
        try:
            employee = Employee.objects.get(user=request.user)
        except Employee.DoesNotExist:
            return Response({'error': 'Employee profile not found'}, status=404)
        
        attendance_records = Attendance.objects.filter(employee=employee)
        
        if date_param:
            try:
                date_obj = datetime.strptime(date_param, '%Y-%m-%d').date()
                attendance_records = attendance_records.filter(date=date_obj)
            except ValueError:
                return Response({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=400)
        
        serializer = AttendanceSerializer(attendance_records, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        try:
            employee = Employee.objects.get(user=request.user)
        except Employee.DoesNotExist:
            return Response({'error': 'Employee profile not found'}, status=404)
            
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            # 检查是否已存在当天的考勤记录
            existing_attendance = Attendance.objects.filter(
                employee=employee,
                date=serializer.validated_data.get('date')
            ).first()
            
            if existing_attendance:
                return Response({'error': 'Attendance record already exists for this date'}, status=400)
                
            serializer.save(employee=employee)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class UserAttendanceDetailView(APIView):
    """
    用户查看和更新自己的考勤记录
    """
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk, user):
        try:
            return Attendance.objects.get(pk=pk, employee__user=user)
        except Attendance.DoesNotExist:
            return None
    
    def get(self, request, pk):
        attendance = self.get_object(pk, request.user)
        if not attendance:
            return Response({'error': 'Attendance record not found'}, status=404)
            
        serializer = AttendanceSerializer(attendance)
        return Response(serializer.data)
    
    def put(self, request, pk):
        attendance = self.get_object(pk, request.user)
        if not attendance:
            return Response({'error': 'Attendance record not found'}, status=404)
            
        serializer = AttendanceSerializer(attendance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

class AdminAttendanceListView(APIView):
    """
    管理员查看所有员工考勤记录
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=403)
            
        # 支持按日期筛选
        date_param = request.GET.get('date', None)
        
        attendance_records = Attendance.objects.all()
        
        if date_param:
            try:
                date_obj = datetime.strptime(date_param, '%Y-%m-%d').date()
                attendance_records = attendance_records.filter(date=date_obj)
            except ValueError:
                return Response({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=400)
        
        serializer = AttendanceSerializer(attendance_records, many=True)
        return Response(serializer.data)

class AdminAttendanceDetailView(APIView):
    """
    管理员查看特定考勤记录
    """
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return Attendance.objects.get(pk=pk)
        except Attendance.DoesNotExist:
            return None
    
    def get(self, request, pk):
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=403)
            
        attendance = self.get_object(pk)
        if not attendance:
            return Response({'error': 'Attendance record not found'}, status=404)
            
        serializer = AttendanceSerializer(attendance)
        return Response(serializer.data)