from django.urls import path
from . import views

urlpatterns = [
    # Authentification sécurisée Django
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard principal
    path('', views.home, name='home'),
    
    # Gestion des QR Codes et accès
    path('generate-qr/<int:user_id>/', views.generate_qr_view, name='generate_qr_view'),
    path('access/<int:user_id>/', views.access_page, name='access_page'),
    
    # Scanner et API temps réel (Appelée par le JavaScript)
    path('start-scanner/', views.trigger_camera_view, name='start_scanner'),
    path('verify-qr/<str:token_uuid>/', views.verify_qr, name='verify_qr'),
]