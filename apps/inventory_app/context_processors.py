# your_app/context_processors.py
from .models import Alert

def unseen_alerts_count(request):
    if request.user.is_authenticated and request.user.is_staff:
        unseen_alerts = Alert.objects.filter(is_seen=False)
        return {'unseen_alerts_count': unseen_alerts.count()}
    return {'unseen_alerts_count': 0}
