import qrcode
import os
from django.conf import settings

def generate_qr(token_uuid):
    folder = os.path.join(settings.BASE_DIR, "core", "static", "qr_codes")
    os.makedirs(folder, exist_ok=True)

    filename = f"qr_{token_uuid}.png"
    path = os.path.join(folder, filename)

    # L'URL que le scanner va décoder (il scanne et valide directement via une API/Vue)
    # En production, remplacez par votre vrai domaine
    qr_data = f"http://127.0.0.1:8000/verify-qr/{token_uuid}/"

    img = qrcode.make(qr_data)
    img.save(path)

    return f"qr_codes/{filename}"