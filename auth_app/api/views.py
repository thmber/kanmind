#from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

User = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'token': Token.objects.get(user__id=serializer.data['id']).key,
                'fullname': serializer.data['fullname'],
                'email': serializer.data['email'],
                'user_id': serializer.data['id']
                }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'fullname': getattr(user, 'fullname', None),
            'email': getattr(user, 'email', None),
            'user_id': user.id,
        }, status=status.HTTP_200_OK)
    

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete() 
        return Response({"message": "Logout successfull. Token deleted."}, status=status.HTTP_200_OK)


class EmailCheckView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        email = request.query_params.get('email')
        if not email: 
            return Response({'error': 'Email parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            validate_email(email)
        except ValidationError:
            return Response({'error': 'Invalid email format.'}, status=status.HTTP_400_BAD_REQUEST)

        founduser = User.objects.filter(email=email).first()
        if not founduser:
            return Response({'error': 'No user with this email found.'}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'id': founduser.id,
            'email': founduser.email,
            'fullname': founduser.fullname,
        }, status=status.HTTP_200_OK)

