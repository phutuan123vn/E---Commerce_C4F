from pprint import pprint
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core import settings
from core.customToken import CustomRefreshToken
from core.models import User
from core.serializers import (LoginUserSerializer, RegisterUserSerializer,
                              UserSerializer)
from utils.encrypt import encrypt

def get_tokens_for_user(user: User):
    refresh:CustomRefreshToken = CustomRefreshToken.for_user(user)
    refresh['username'] = user.email
    pprint(refresh)
    return {
        'access': str(refresh.access_token),
        'secret': str(refresh.cookie_token),
        'refresh': str(refresh),
    }

def setCookie(response: Response, data:str, typeCookie:str):
    assert data is not None, "Data is required"
    assert typeCookie in ['refresh', 'secret'], "Invalid type cookie"
    if typeCookie == 'refresh':
        data = encrypt(data.encode()).decode()
        response.set_cookie(
            key = settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
            value = data,
            expires = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )
    else:
        response.set_cookie(
            key = settings.SIMPLE_JWT['AUTH_COOKIE_SECRET'],
            value = data,
            expires = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )
    

class LoginView(APIView):
    authentication_classes = ([])
    # permission_classes = (AllowAny,)
    serializer_class = LoginUserSerializer
    
    def post(self, request: Request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user: User = serializer.validated_data
            if user.is_active:
                data = get_tokens_for_user(user)
                response = Response()
                setCookie(response, data['refresh'], 'refresh')
                setCookie(response, data['secret'], 'secret')
                # csrf.get_token(request)
                response.data = {
                    "Success" : "Login successfully",
                    "access_token": data['access'],
                    "user": {
                        'id': user.id,
                        'username': user.email,
                    }
                }
                
                return response
            else:
                return Response({"No active" : "This account is not active!!"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"Invalid" : "Invalid username or password!!"}, status=status.HTTP_404_NOT_FOUND)

class CreateUsersView(generics.ListCreateAPIView):
    authentication_classes = ([])
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer

class LoginUserView(APIView):
    authentication_classes = ([])
    permission_classes = (AllowAny,)
    serializer_class = LoginUserSerializer

    def post(self, request: Request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            if user and user.is_active:
                data = get_tokens_for_user(user)
                response = Response()
                response.set_cookie(
                    key = settings.SIMPLE_JWT['AUTH_COOKIE'],
                    value = data["refresh"],
                    expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                    secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )
                # csrf.get_token(request)
                response.data = {"Success" : "Login successfully","access_token":data['access'], "user": {
                    'id': user.id,
                    'username': user.username,
                }}
                return response
            else:
                return Response({"No active" : "This account is not active!!"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"Invalid" : "Invalid username or password!!"}, status=status.HTTP_404_NOT_FOUND)

class LogoutUserView(APIView):
    def post(self,request: Request):
        response = Response()
        # response.delete_cookie('csrftoken')
        response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE_SECRET'])
        response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
        response.data = {"message":"Logout successfully"}
        return response
    
    
@api_view(["GET","POST"])
@permission_classes([IsAuthenticated])
def testAPI(request: Request):
    # print(request.data)
    # print(request.COOKIES)
    # pprint(request.auth)
    # pprint(request.COOKIES)
    return Response({"message":"Hello World"})
    
    
    