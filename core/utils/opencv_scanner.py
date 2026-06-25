import cv2
import requests
import time

def start_camera():
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()
    
    last_scanned_token = None
    last_scanned_time = 0

    print("Scanner activé... Appuyez sur 'q' pour quitter.")

    while True:
        _, frame = cap.get_backend_data() if hasattr(cap, 'get_backend_data') else cap.read()
        if frame is None:
            break

        # Détection du QR Code
        data, bbox, _ = detector.detectAndDecode(frame)
        
        if data:
            current_time = time.time()
            # Anti-rebond : évite de scanner le même QR code en boucle (attendre 3 secondes)
            if data != last_scanned_token or (current_time - last_scanned_time > 3):
                last_scanned_token = data
                last_scanned_time = current_time
                
                print(f"QR Détecté : {data}")
                try:
                    # Envoi de la requête de validation à Django
                    response = requests.get(data, timeout=3)
                    result = response.json()
                    status = result.get('status', 'INVALID')
                    user = result.get('user', 'Inconnu')
                    print(f"Résultat serveur : {status} pour {user}")
                except Exception as e:
                    print(f"Erreur de connexion serveur : {e}")

        # Affichage du flux vidéo à l'écran
        cv2.imshow("Scanner de Securite - Smart Authentication", frame)

        # Quitter avec la touche 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()