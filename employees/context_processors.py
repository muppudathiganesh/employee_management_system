from django.contrib.auth.models import User

def admin_id_processor(request):
    try:
        admin_user = User.objects.filter(is_superuser=True).first()
        return {'admin_id': admin_user.id if admin_user else None}
    except:
        return {'admin_id': None}
    
from .models import Ticket

def unread_ticket_count(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return {"unread_count": Ticket.objects.filter(is_read=False).count()}
    return {"unread_count": 0}
