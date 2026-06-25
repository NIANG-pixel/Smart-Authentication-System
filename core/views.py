from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import UserProfile
from .utils.qr_generator import generate_qr

# Imports de vos services découplés
from core.services.auth_service import AuthService
from core.services.access_service import AccessService


def login_view(request):
    """
    Gère la connexion de l'utilisateur avec le système de sécurité Django
    """
    error = None
    if request.method == "POST":
        u_name = request.POST.get("username")
        p_word = request.POST.get("password")
        user = authenticate(request, username=u_name, password=p_word)
        
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            error = "Identifiants invalides."
            
    return render(request, "core/login.html", {"error": error})


def logout_view(request):
    """
    Déconnexion de l'utilisateur
    """
    logout(request)
    return redirect("login")


@login_required
def home(request):
    """
    Dashboard principal : utilise le service pour lister tous les utilisateurs
    """
    users = AuthService.get_all_users()
    return render(request, "core/home.html", {"users": users})


@login_required
def generate_qr_view(request, user_id):
    """
    Génère un jeton sécurisé via AccessService et crée le fichier QR correspondant
    """
    user_prof = get_object_or_404(UserProfile, id=user_id)
    
    # 1. Utilisation du service pour générer le jeton unique (UUID)
    qr_access = AccessService.generate_user_qr(user_prof)
    
    # 2. Génération physique de l'image basée sur ce jeton UUID unique
    qr_path = generate_qr(qr_access.token)
    
    return render(request, "core/generate_qr.html", {
        "qr_path": qr_path,
        "user_prof": user_prof,
        "token": qr_access.token
    })


def verify_qr(request, token_uuid):
    """
    Endpoint API appelé par JavaScript (AJAX) en temps réel lors du scan
    """
    # Utilisation de la logique de validation centralisée de votre service
    user_prof, status = AccessService.validate_qr(token_uuid)
    
    if user_prof and status == "ALLOWED":
        AccessService.log_access(user_prof, "ALLOWED", "Passé avec succès par la borne de scan.")
        return JsonResponse({"status": "ALLOWED", "user": user_prof.user.username})
    else:
        username = user_prof.user.username if user_prof else "Inconnu"
        details = "Tentative de fraude ou retard." if status != "INVALID" else "Jeton inexistant."
        AccessService.log_access(user_prof, status, details)
        return JsonResponse({"status": status, "user": username})


def trigger_camera_view(request):
    """
    Affiche l'interface du scanner vidéo (géré côté navigateur en JS)
    """
    return render(request, "core/camera_active.html")


def access_page(request, user_id):
    """
    Page d'accès individuelle (historique)
    """
    user = AuthService.get_user_by_id(user_id)
    if user:
        AccessService.log_access(user, "QR ACCESSED", "Page d'accès consultée.")
        
    return render(request, "core/access.html", {
        "user": user
    })