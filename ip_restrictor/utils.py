from ipaddress import ip_network, ip_address


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def ip_address_in_ip_range(client_ip, ip_ranges) -> bool:

    return any(
        ip_address(client_ip) in ip_network(ip_range, strict=False) for ip_range in ip_ranges
    )
