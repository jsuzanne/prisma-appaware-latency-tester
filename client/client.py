#!/usr/bin/env python3
import socket
import time
import argparse
from datetime import datetime
import random

def is_business_hours():
    """
    Vérifie si nous sommes pendant les heures de travail
    Lundi-Vendredi: 8h-18h
    """
    now = datetime.now()
    
    # Vérifier si c'est le weekend (samedi=5, dimanche=6)
    if now.weekday() >= 5:
        return False
    
    # Vérifier les heures (8h-18h)
    if now.hour < 8 or now.hour >= 18:
        return False
    
    return True

def get_dynamic_interval(base_interval):
    """
    Retourne un intervalle adapté selon l'heure
    - Heures de travail: intervalle normal avec variation
    - Hors heures de travail: intervalle très long
    - Weekend: intervalle très long
    """
    now = datetime.now()
    is_weekend = now.weekday() >= 5
    
    if is_business_hours():
        # Heures de travail: activité normale avec variation aléatoire
        # Simule des pics d'activité (ex: plus actif à 10h, 14h, 16h)
        if now.hour in [10, 14, 16]:
            # Heures de pointe: plus rapide
            return base_interval * random.uniform(0.5, 1.0)
        elif now.hour in [8, 12, 17]:
            # Début/pause déjeuner/fin: plus lent
            return base_interval * random.uniform(1.5, 2.5)
        else:
            # Normal
            return base_interval * random.uniform(0.8, 1.5)
    
    elif is_weekend:
        # Weekend: très peu d'activité (1 requête toutes les 30-60 min)
        return random.uniform(1800, 3600)
    
    else:
        # Nuit (18h-8h): activité minimale (1 requête toutes les 10-30 min)
        return random.uniform(600, 1800)

def client_program(host='127.0.0.1', port=8888, interval=2, max_iterations=None):
    """
    Client TCP qui émule du trafic réaliste d'utilisateurs
    """
    iteration = 0
    
    print(f"[CLIENT] Configuration: {host}:{port}, intervalle de base: {interval}s")
    print(f"[CLIENT] Mode émulation horaires de travail activé")
    
    try:
        while True:
            if max_iterations and iteration >= max_iterations:
                print(f"[CLIENT] Nombre maximum d'itérations atteint ({max_iterations})")
                break
            
            # Vérifier si nous sommes en heures de travail
            now = datetime.now()
            in_business_hours = is_business_hours()
            
            # Afficher le statut
            day_type = "Weekend" if now.weekday() >= 5 else "Semaine"
            hour_type = "Heures de travail" if in_business_hours else "Hors heures"
            
            iteration += 1
            
            # Nouvelle connexion pour chaque transaction
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(60)
            
            try:
                print(f"\n[CLIENT] Transaction #{iteration} - {day_type} - {hour_type}")
                print(f"[CLIENT] {now.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"[CLIENT] Connexion à {host}:{port}...")
                
                start_time = time.time()
                client_socket.connect((host, port))
                connect_time = time.time() - start_time
                print(f"[CLIENT] Connecté en {connect_time:.3f} secondes")
                
                # Envoyer le message
                message = f"Request #{iteration} - {now.strftime('%Y-%m-%d %H:%M:%S')}"
                print(f"[CLIENT] Envoi: {message}")
                send_time = time.time()
                client_socket.send(message.encode('utf-8'))
                
                # Recevoir la réponse (header uniquement jusqu'au \n)
                header_data = b''
                while b'\n' not in header_data:
                    chunk = client_socket.recv(1)
                    if not chunk:
                        raise Exception("Connexion fermée avant de recevoir le header complet")
                    header_data += chunk
                
                header = header_data.decode('utf-8').strip()
                print(f"[CLIENT] Header reçu: {header}")
                
                # Recevoir les données binaires
                bytes_received = 0
                data_chunks = []
                
                while True:
                    chunk = client_socket.recv(8192)
                    if not chunk:
                        break
                    data_chunks.append(chunk)
                    bytes_received += len(chunk)
                
                total_time = time.time() - send_time
                
                print(f"[CLIENT] Données reçues: {bytes_received} octets ({bytes_received/1024/1024:.2f} Mo)")
                print(f"[CLIENT] Temps de transaction: {total_time:.2f} secondes")
                if total_time > 0:
                    print(f"[CLIENT] Débit: {(bytes_received/1024/1024)/total_time:.2f} Mo/s")
                
            except socket.timeout:
                print(f"[CLIENT] Timeout lors de la transaction #{iteration}")
            except ConnectionRefusedError:
                print(f"[CLIENT] Connexion refusée par le serveur")
            except Exception as e:
                print(f"[CLIENT] Erreur lors de la transaction #{iteration}: {e}")
            finally:
                client_socket.close()
                print(f"[CLIENT] Connexion fermée")
            
            # Calculer l'intervalle dynamique
            if max_iterations is None or iteration < max_iterations:
                dynamic_interval = get_dynamic_interval(interval)
                next_time = datetime.fromtimestamp(time.time() + dynamic_interval)
                
                print(f"[CLIENT] Attente de {dynamic_interval:.0f} secondes ({dynamic_interval/60:.1f} min)")
                print(f"[CLIENT] Prochaine connexion prévue: {next_time.strftime('%Y-%m-%d %H:%M:%S')}")
                
                time.sleep(dynamic_interval)
            
    except KeyboardInterrupt:
        print("\n[CLIENT] Arrêt du client...")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Client TCP avec émulation horaires de travail')
    parser.add_argument('--host', default='127.0.0.1', help='Adresse IP du serveur (défaut: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=8888, help='Port du serveur (défaut: 8888)')
    parser.add_argument('--interval', type=float, default=180.0, help='Intervalle de base en secondes (défaut: 180 = 3 min)')
    parser.add_argument('--max-iterations', type=int, default=None, help='Nombre maximum de transactions (défaut: infini)')
    
    args = parser.parse_args()
    client_program(args.host, args.port, args.interval, args.max_iterations)

