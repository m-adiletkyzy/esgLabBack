from django.http import JsonResponse

ALLOWED_ORIGINS = ['http://localhost', 'http://127.0.0.1', 'http://esg.kbtu.kz', 'https://esg.kbtu.kz']

class RestrictedAPIMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/esgadminpanel"):
            return self.get_response(request)
        
        origin = request.headers.get("Origin")
        referer = request.headers.get("Referer")

        if not origin and not referer:
            return JsonResponse({"error: Forbidden"}, status=403)
        
        if(origin not in ALLOWED_ORIGINS
            and not(referer and any(referer.startswith(o) for o in ALLOWED_ORIGINS))):
            return JsonResponse({"error: Forbidden"}, status=403)
        
        return self.get_response(request)
