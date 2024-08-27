from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import authentication
from rest_framework import exceptions as rest_exceptions
from rest_framework.request import Request
from rest_framework_simplejwt import authentication as jwt_authentication
from rest_framework_simplejwt.settings import api_settings


def enforce_csrf(request):
    check = authentication.CSRFCheck(request)
    reason = check.process_view(request, None, (), {})
    if reason:
        raise rest_exceptions.PermissionDenied('CSRF Failed: %s' % reason)


class CustomAuthentication(jwt_authentication.JWTAuthentication):
    def authenticate(self, request: Request):
        header = self.get_header(request)
        cookie_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE_SECRET']) or None
        # access_token = None # 3
        if header is None:
            # access_token = None
            return None # 1
        access_token = self.get_raw_token(header) # or None # 2
        if access_token is None and cookie_token is None:
            return None
        token = {
            "access": access_token,
            "cookie": cookie_token
        }
        validated_token = self.get_validated_token(token)
        # validated_token = self.get_validated_token(access_token)
        # print("validated_token",validated_token)
        # enforce_csrf(request)
        return self.get_user(validated_token), validated_token
        
    def get_class_AuthToken(self):
        list_AuthTokenCls = api_settings.AUTH_TOKEN_CLASSES
        AuthTokenCls = {}
        for Cls in list_AuthTokenCls:
            AuthTokenCls[Cls.token_type] = Cls
        return AuthTokenCls
        
        
    def get_validated_token(self, token:dict) -> jwt_authentication.Token:
        """
        Validates an encoded JSON web token and returns a validated token
        wrapper object.
        """
        AuthTokenCls = self.get_class_AuthToken()
        messages = ''
        for typeToken, tokenValue in token.items():
            if tokenValue is not None:
                try:
                    return AuthTokenCls[typeToken](tokenValue)
                except jwt_authentication.TokenError as e:
                    pass
        message = "Token is invalid or expired"
                    
        raise jwt_authentication.InvalidToken(
            {
                "detail": _("Given token not valid for any token type"),
                "messages": "Token is invalid or expired",
                "code": "token_not_valid",
            }
        )