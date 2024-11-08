from django.conf import settings
from django.http import HttpResponseForbidden

from ip_restrictor.utils import get_client_ip, ip_address_in_ip_range


class IPRestrictMiddleware:
    """
    Middleware to apply global IP restrictions based on DEFAULT_IP_RESTRICTION_MODE in settings file.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.default_mode = getattr(settings, "DEFAULT_IP_RESTRICTION_MODE", False)

    def __call__(self, request):
        allowed_ips = getattr(settings, "WHITELIST_IPS", [])
        blocked_ips = getattr(settings, "BLACKLIST_IPS", [])

        ip_address = get_client_ip(request)

        if self.default_mode == "WHITELIST" and not ip_address_in_ip_range(
            ip_address, allowed_ips
        ):
            return HttpResponseForbidden("Access denied: Your IP is not on allowed.")

        if self.default_mode == "BLACKLIST" and ip_address_in_ip_range(
            ip_address, blocked_ips
        ):
            return HttpResponseForbidden("Access denied: Your IP is not on allowed.")

        return self.get_response(request)
