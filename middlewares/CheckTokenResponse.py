from pprint import pprint
from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework.request import Request
from rest_framework.response import Response

from core.customToken import CustomRefreshToken
from core.settings import SIMPLE_JWT as JWT_SETTINGS
from utils.encrypt import decrypt


def getTokenCls(request: Request) -> CustomRefreshToken:
    if not hasattr(request,'auth') or request.auth is None:
        return None
    # print("Request.auth: ", request.auth)
    # print("check boolena",not hasattr(request,'auth') and request.auth is None)
    if request.auth.token_type == 'access':
        return None
    
    refresh_token = request.COOKIES.get(JWT_SETTINGS['AUTH_COOKIE_REFRESH']) or None
    if refresh_token is None:
        return None
    
    refresh_token = decrypt(refresh_token.encode()).decode()
    return CustomRefreshToken(refresh_token)
    
class CheckTokenResponse(MiddlewareMixin):
    
    def process_response(self, request: HttpRequest, response: HttpResponse):
        # pprint(vars(request))
        refreshTokenCls = getTokenCls(request)
        if refreshTokenCls is not None and 'logout' not in request.path:
            if isinstance(response, Response):
                data = response.data
                if type(data) != dict:
                    response.data = {'message': data}
                response.data['access_token'] = str(refreshTokenCls.access_token)
                response._is_rendered = False
                response.render()
            # response.content = data
        return response