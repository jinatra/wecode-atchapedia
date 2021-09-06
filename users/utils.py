import jwt

from django.http import JsonResponse

from .models     import User
from my_settings import SECRET_KEY, ALGORITHM


def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get("Authorization", None)
            user = jwt.decode(access_token, SECRET_KEY, algorithms=ALGORITHM)
            request.user = User.objects.get(id = user['id'])

        except jwt.exceptions.DecodeError:                                   
            return JsonResponse({'message' : '일치하지 않는 토큰입니다.' }, status=400)

        except User.DoesNotExist:       
            return JsonResponse({'message' : '존재하지 않는 사용자입니다.'}, status=400)

        return func(self, request, *args, **kwargs)

    return wrapper
        
