from django.http import JsonResponse
from time import time
from collections import defaultdict

class RateLimitMiddleware:
    RATE_LIMIT = 50  # requests
    TIME_WINDOW = 10  # seconds
    REQUESTS_LOG = defaultdict(list)

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        client_ip = self.get_client_ip(request)
        current_time = time()

        # Clean up old requests
        self.REQUESTS_LOG[client_ip] = [
            timestamp for timestamp in self.REQUESTS_LOG[client_ip]
            if timestamp > current_time - self.TIME_WINDOW
        ]

        # Check rate limit
        if len(self.REQUESTS_LOG[client_ip]) >= self.RATE_LIMIT:
            return JsonResponse(
                {"error": "Too Many Requests"}, status=429
            )

        # Log current request
        self.REQUESTS_LOG[client_ip].append(current_time)

        return self.get_response(request)

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")
