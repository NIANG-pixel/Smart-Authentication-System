from core.models import UserProfile

class AuthService:

    @staticmethod
    def create_user(user_auth_instance, phone=""):
        """
        Lie un utilisateur natif Django à un UserProfile de notre application
        """
        return UserProfile.objects.create(
            user=user_auth_instance,
            phone=phone
        )

    @staticmethod
    def get_user_by_id(user_id):
        """
        Récupère un profil utilisateur par son ID de profil
        """
        try:
            return UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return None

    @staticmethod
    def get_all_users():
        """
        Retourne tous les profils utilisateurs pour le Dashboard
        """
        return UserProfile.objects.all()

    @staticmethod
    def delete_user(user_id):
        """
        Supprime un profil utilisateur
        """
        user_prof = AuthService.get_user_by_id(user_id)
        if user_prof:
            user_prof.delete()
            return True
        return False