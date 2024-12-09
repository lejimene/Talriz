from django.http import JsonResponse
from time import time
from collections import defaultdict

class RateLimitMiddleware:
    RATE_LIMIT = 50  # Max requests allowed
    TIME_WINDOW = 10  # Time window in seconds
    BLOCK_DURATION = 30  # Block duration in seconds
    REQUEST_LOG = defaultdict(list)  # Store timestamps for each IP
    BLOCKED_IPS = {}  # Store blocked IPs with unblock timestamps

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        client_ip = self.get_client_ip(request)
        current_time = time()

        # Check if the IP is blocked
        if client_ip in self.BLOCKED_IPS:
            unblock_time = self.BLOCKED_IPS[client_ip]
            if current_time < unblock_time:
                # Still blocked, return 429 response
                return JsonResponse(
                    {
                        "error": "Too Many Requests",
                        "message": "Your IP is temporarily blocked due to excessive requests. Please try again later.",
                    },
                    status=429,
                )
            else:
                # Unblock the IP
                del self.BLOCKED_IPS[client_ip]

        # Clean up old requests
        self.REQUEST_LOG[client_ip] = [
            timestamp for timestamp in self.REQUEST_LOG[client_ip]
            if timestamp > current_time - self.TIME_WINDOW
        ]

        # Check if the rate limit is exceeded
        if len(self.REQUEST_LOG[client_ip]) >= self.RATE_LIMIT:
            # Block the IP
            self.BLOCKED_IPS[client_ip] = current_time + self.BLOCK_DURATION
            return JsonResponse(
                {
                    "error": "Too Many Requests",
                    "message": "Your IP has been blocked due to excessive requests. Please wait 30 seconds before trying again.",
                },
                status=429,
            )

        # Log the current request
        self.REQUEST_LOG[client_ip].append(current_time)

        # Proceed with the request
        return self.get_response(request)

    @staticmethod
    def get_client_ip(request):
        """Retrieve the client IP address."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")

