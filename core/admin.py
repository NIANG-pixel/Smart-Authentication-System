from django.contrib import admin
from .models import UserProfile, QRAccess, AccessLog

# Enregistrez vos modèles pour l'interface d'administration
admin.site.register(UserProfile)
admin.site.register(QRAccess)
admin.site.register(AccessLog)