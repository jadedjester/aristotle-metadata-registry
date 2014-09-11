
# This allows us to pass the Aristotle settigns through to the final rendered page
def settings(request):
    from django.conf import settings
    return {"config": getattr(settings, 'ARISTOTLE_SETTINGS', {})}
