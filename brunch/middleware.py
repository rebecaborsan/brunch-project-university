class IPClientMiddleware:
    """Salveaza IP-ul in cerere, ca sa il putem folosi in views.py."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Citim IP-ul din datele cererii primite de server.
        request.ip_client = request.META.get("REMOTE_ADDR", "")
        return self.get_response(request)
