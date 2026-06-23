# myapp/middleware.py
from threading import local

_user = local()

class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Store the current user in thread-local storage
        _user.value = request.user
        response = self.get_response(request)
        return response

    @staticmethod
    def get_current_user():
        # Retrieve the current user from thread-local storage
        return getattr(_user, 'value', None)
