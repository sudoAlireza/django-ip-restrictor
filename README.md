# django-ip-restrictor

A simple Django package to restrict access to views based on IP addresses.

## Installation

```bash
pip install django-ip-restrictor
```

## Configuration

1. Add `ip_restrictor.middleware.IPRestrictMiddleware` to your `MIDDLEWARE` setting in `settings.py`:

```python
MIDDLEWARE = [
    # ... other middleware ...
    'ip_restrictor.middleware.IPRestrictMiddleware',
    # ... other middleware ...
]
```

2. Configure allowed and blocked IP addresses in your `settings.py`:

```python
WHITELIST_IPS = ["127.0.0.1", "192.168.1.0/24"]  # Allow localhost and the 192.168.1.0/24 subnet
BLACKLIST_IPS = ["10.0.0.5", "10.0.0.6"]  # Block these specific IPs
```

3.  Set the default restriction mode (optional):

```python
DEFAULT_IP_RESTRICTION_MODE = "WHITELIST"  # or "BLACKLIST" or False (default)
```

- `"WHITELIST"`: Only allows access from IPs in `WHITELIST_IPS`.
- `"BLACKLIST"`: Blocks access from IPs in `BLACKLIST_IPS`.
- `False`: No default restriction; use decorators or mixins for specific views.

## Usage

### 1. Decorators:

Use the `@allow_whitelist` and `@deny_blacklist` decorators to restrict access to function-based views:

```python
from ip_restrictor.decorators import allow_whitelist, deny_blacklist

@allow_whitelist
def my_protected_view(request):
    # ... your view logic ...
    return HttpResponse("This view is only accessible from whitelisted IPs.")


@deny_blacklist
def another_protected_view(request):
    # ... your view logic ...
    return HttpResponse("This view blocks blacklisted IPs.")
```

### 2. Mixins:

Use the `WhitelistIPMixin` and `BlackListIPMixin` for class-based views:


```python
from ip_restrictor.mixins import WhitelistIPMixin, BlackListIPMixin
from django.views.generic import TemplateView

class ProtectedCBV(WhitelistIPMixin, TemplateView):
    template_name = "my_template.html"


class AnotherProtectedCBV(BlackListIPMixin, TemplateView):
    template_name = "another_template.html"

```

### 3. Middleware (Global Restriction):

The middleware applies the restrictions based on `DEFAULT_IP_RESTRICTION_MODE`.  If the mode is set to "WHITELIST", only whitelisted IPs will be allowed access to any view.  If set to "BLACKLIST", blacklisted IPs will be denied access.


## Handling X-Forwarded-For

The middleware and decorators handle the `X-Forwarded-For` header, so it should work correctly with reverse proxies.


## Error Handling

If an IP address is not allowed, the middleware or decorator will return an `HttpResponseForbidden` (403). You can customize this behavior by implementing custom error handling middleware or overriding the decorator/mixin functionality.


## Example settings.py

```python
MIDDLEWARE = [
    # ... other middleware ...
    'ip_restrictor.middleware.IPRestrictMiddleware',
]

WHITELIST_IPS = ["127.0.0.1", "192.168.0.0/16"]
BLACKLIST_IPS = ["10.0.0.0/8"]
DEFAULT_IP_RESTRICTION_MODE = "WHITELIST" # Or "BLACKLIST" or False
```
