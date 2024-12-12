from functools import cache
import json
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
from mainapp.serializers import RoleSerializer,SystemUserSerializer
from rest_framework.decorators import api_view,permission_classes
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.utils import timezone
from .models import SystemUser,Roles
from django.contrib.auth.hashers import make_password


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'email': user.email
        })

class RoleCreateView(APIView):
    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class SystemUserCreateView(APIView):
    def post(self, request):
        serializer = SystemUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "mobile_no": user.mobile_no,
                "role": user.role_id.name
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_system_user(request):
    if request.method == 'POST':
        username = request.data.get('username')
        email = request.data.get('email')
        mobile_no = request.data.get('mobile_no')
        profile_image = request.FILES.get('profile_image')
        role_id = request.data.get('role_id')
        password = request.data.get('password')

        # Basic validation
        if not all([username, email, mobile_no, role_id, password]):
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Check for existing email or mobile
        if SystemUser.objects.filter(email=email).exists() or SystemUser.objects.filter(mobile_no=mobile_no).exists():
            return Response({"error": "Email or mobile number already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # Get role object
        try:
            role = Roles.objects.get(id=role_id)
        except Roles.DoesNotExist:
            return Response({"error": "Invalid role ID."}, status=status.HTTP_400_BAD_REQUEST)

        # Create user
        user = SystemUser.objects.create(
            username=username,
            email=email,
            mobile_no=mobile_no,
            profile_image=profile_image,
            role_id=role,
            password=make_password(password)  # Hash the password
        )

        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "mobile_no": user.mobile_no,
            "profile_image": user.profile_image.url if user.profile_image else None,
            "role": user.role_id.name
        }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_user(request, user_id):
    try:
        user = SystemUser.objects.get(id=user_id)
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "mobile_no": user.mobile_no,
            "profile_image": user.profile_image.url if user.profile_image else None,
            "role": user.role_id.name
        })
    except SystemUser.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def update_user(request, user_id):
    try:
        user = SystemUser.objects.get(id=user_id)
        
        user.username = request.data.get('username', user.username)
        user.email = request.data.get('email', user.email)
        user.mobile_no = request.data.get('mobile_no', user.mobile_no)
        user.profile_image = request.FILES.get('profile_image', user.profile_image)
        
        password = request.data.get('password')
        if password:
            user.password = make_password(password)
        
        user.save()

        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "mobile_no": user.mobile_no,
            "profile_image": user.profile_image.url if user.profile_image else None,
            "role": user.role_id.name
        })
    except SystemUser.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_user(request, user_id):
    try:
        user = SystemUser.objects.get(id=user_id)
        user.delete()
        return Response({"message": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    except SystemUser.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    
    
# @api_view(['GET'])
# @permission_classes([permissions.IsAuthenticated])
# def get_user(request, user_id):
#     try:
#         user = User.objects.get(id=user_id)
#         print(user)
#         return Response(SystemUserSerializer(user).data)
#     except User.DoesNotExist:
#         return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
@csrf_exempt
def send_otp(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            if not email:
                return JsonResponse({'error': 'Email is required'}, status=400)

            # user = get_user_model().objects.filter(email=email).first()
            user = SystemUser.objects.filter(email=email).first()
            if not user:
                return JsonResponse({'error': 'User not found'}, status=404)

            otp = get_random_string(length=6, allowed_chars='0123456789')
            
            expiry_time = timezone.now() + timedelta(minutes=5)

            user.otp = otp
            user.expiry_time = expiry_time
            user.save()

            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp}. It is valid for 5 minutes.',
                'demomail1250@gmail.com',
                [email],
            )

            return JsonResponse({'message': 'OTP sent successfully'}, status=200)

        except Exception as e:
            return JsonResponse({'error': f'Failed to process request: {str(e)}'}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def verify_otp(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            otp = data.get('otp')

            if not email or not otp:
                return JsonResponse({'error': 'Email and OTP are required'}, status=400)

            user = SystemUser.objects.filter(email=email).first()
            if not user:
                return JsonResponse({'error': 'User not found'}, status=404)

            if user.otp != int(otp):
                return JsonResponse({'error': 'Invalid OTP'}, status=400)

            if timezone.now() > user.expiry_time:
                return JsonResponse({'error': 'OTP has expired'}, status=400)

            new_otp = get_random_string(length=6, allowed_chars='0123456789')
            expiry_time = timezone.now() + timedelta(minutes=5)

            user.otp = new_otp
            user.expiry_time = expiry_time
            user.save()

            return JsonResponse({'message': 'OTP verified successfully. New OTP generated.'}, status=200)

        except Exception as e:
            return JsonResponse({'error': f'Failed to process request: {str(e)}'}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)