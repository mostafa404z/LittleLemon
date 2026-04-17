from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # القائمة البيضاء: الصفحات التي لا تحتاج تسجيل دخول
        exempt_urls = [reverse('login'), reverse('register')] 

        if not request.user.is_authenticated and request.path not in exempt_urls:
            return redirect('login')

        response = self.get_response(request)
        return response