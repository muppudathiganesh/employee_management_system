from django.contrib.auth.models import User

def admin_id_processor(request):
    try:
        admin_user = User.objects.filter(is_superuser=True).first()
        return {'admin_id': admin_user.id if admin_user else None}
    except:
        return {'admin_id': None}
