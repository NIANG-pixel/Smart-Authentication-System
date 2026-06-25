import uuid
from datetime import timedelta
from django.utils import timezone
from core.models import AccessLog, QRAccess

class AccessService:

    @staticmethod
    def generate_user_qr(user_profile):
        """
        Génère un jeton d'accès unique sécurisé (UUID) pour un profil utilisateur
        """
        # Génération d'un UUID4 propre, impossible à deviner (ex: '4a2b3c4d-...')
        secure_token = str(uuid.uuid4())

        qr_access = QRAccess.objects.create(
            user=user_profile,
            token=secure_token,
            is_used=False
        )
        return qr_access

    @staticmethod
    def log_access(user_profile, status, details=""):
        """
        Enregistre une tentative d'accès (Historique)
        """
        return AccessLog.objects.create(
            user=user_profile,
            status=status,
            details=details
        )

    @staticmethod
    def validate_qr(token_str):
        """
        Vérifie la validité du jeton, gère les 5 minutes et l'usage unique
        """
        try:
            qr = QRAccess.objects.get(token=token_str)
            
            # Temps d'expiration : 5 minutes après création
            expiration_time = qr.created_at + timedelta(minutes=5)
            
            if timezone.now() < expiration_time and not qr.is_used:
                # Sécurité : On consomme immédiatement le ticket
                qr.is_used = True
                qr.save()
                return qr.user, "ALLOWED"
            elif qr.is_used:
                return qr.user, "ALREADY_USED"
            else:
                return qr.user, "EXPIRED"
                
        except QRAccess.DoesNotExist:
            return None, "INVALID"