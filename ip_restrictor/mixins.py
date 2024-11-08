from django.conf import settings
from django.http import HttpResponseForbidden

from ip_restrictor.utils import get_client_ip, ip_address_in_ip_range


class WhitelistIPMixin:
    """
    Mixin to restrict access CBV only to whitelisted IPs.
    """

    def dispatch(self, request, *args, **kwargs):

        ip_address = get_client_ip(request)
        allowed_ips = getattr(settings, "WHITELIST_IPS", [])

        if not ip_address_in_ip_range(ip_address, allowed_ips):
            return HttpResponseForbidden("Access denied: Your IP is not on allowed.")

        return super().dispatch(request, *args, **kwargs)


class BlackListIPMixin:
    """
    Mixin to restrict CBV access to all but blacklisted IPs.
    """

    def dispatch(self, request, *args, **kwargs):

        ip_address = get_client_ip(request)
        blocked_ips = getattr(settings, "WHITELIST_IPS", [])

        if ip_address_in_ip_range(ip_address, blocked_ips):
            return HttpResponseForbidden("Access denied: Your IP is not on allowed.")

        return super().dispatch(request, *args, **kwargs)
