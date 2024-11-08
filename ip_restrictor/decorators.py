from django.http import HttpResponseForbidden
from django.conf import settings

from ip_restrictor.utils import get_client_ip, ip_address_in_ip_range


def allow_whitelist(view_func):
    """
    Decorator to restrict access only to whitelisted IPs.
    """

    def _wrapped_view(request, *args, **kwargs):
        ip_address = get_client_ip(request)
        allowed_ips = getattr(settings, "WHITELIST_IPS", [])

        if not ip_address_in_ip_range(ip_address, allowed_ips):
            return HttpResponseForbidden("Access denied: Your IP is not on allowed.")

        return view_func(request, *args, **kwargs)

    return _wrapped_view


def deny_blacklist(view_func):
    """
    Decorator to restrict access to all but blacklisted IPs.
    """

    def _wrapped_view(request, *args, **kwargs):
        ip_address = get_client_ip(request)
        blocked_ips = getattr(settings, "BLACKLIST_IPS", [])

        if ip_address_in_ip_range(ip_address, blocked_ips):
            return HttpResponseForbidden("Access denied: Your IP is not on allowed.")

        return view_func(request, *args, **kwargs)

    return _wrapped_view
