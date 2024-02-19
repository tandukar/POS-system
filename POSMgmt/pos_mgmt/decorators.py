from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from functools import wraps
from rest_framework.response import Response


def user_login_required(view_func):
    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            return Response(
                {"message": "Access token not found"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        try:
            decoded_token = AccessToken(access_token)
            user_id = decoded_token.payload.get('user_id')
            if user_id is None:
                raise ValueError("User ID not found in token")
            return view_func(self, request, user_id, *args, **kwargs)
        except Exception as e:
            return Response({"message": e}, status=status.HTTP_401_UNAUTHORIZED)
        
    return wrapper
