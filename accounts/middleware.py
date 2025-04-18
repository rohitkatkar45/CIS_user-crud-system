from django.http import JsonResponse
from django.contrib.auth import logout

class DeactivatedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated and getattr(user, 'is_deactivated', False):
            logout(request)
            return JsonResponse({'detail': 'Your account has been deactivated.'}, status=403)

        response = self.get_response(request)
        return response
