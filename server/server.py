#!/usr/bin/env python3
import socket
import time
import random
import argparse
import threading
import os

def generate_random_data(size_bytes):
    """Génère des données aléatoires de la taille spécifiée"""
    return os.urandom(size_bytes)

def handle_client(client_socket, client_address, delay_min, delay_max, data_size):
    """Gère un client dans un thread séparé"""
    print(f"[SERVEUR] Nouveau client connecté: {client_address[0]}:{client_address[1]}")
    
    try:
        # Recevoir la requête du client
        data = client_socket.recv(1024)
        if not data:
            return
            
        message = data.decode('utf-8')
        print(f"[SERVEUR] [{client_address[0]}:{client_address[1]}] Message reçu: {message}")
        
        # Émulation de la lenteur
        delay = random.uniform(delay_min, delay_max)
        print(f"[SERVEUR] [{client_address[0]}:{client_address[1]}] Traitement pendant {delay:.2f} secondes...")
        time.sleep(delay)
        
        # Générer et envoyer les données (1 Mo par défaut)
        print(f"[SERVEUR] [{client_address[0]}:{client_address[1]}] Génération de {data_size} octets...")
        payload = generate_random_data(data_size)
        
        # Envoyer d'abord une confirmation avec la taille
        response_header = f"ACK: {message} | Size: {len(payload)} bytes\n".encode('utf-8')
        client_socket.send(response_header)
        
        # Envoyer les données par morceaux
        bytes_sent = 0
        chunk_size = 8192  # 8 KB par chunk
        while bytes_sent < len(payload):
            chunk = payload[bytes_sent:bytes_sent + chunk_size]
            client_socket.send(chunk)
            bytes_sent += len(chunk)
        
        print(f"[SERVEUR] [{client_address[0]}:{client_address[1]}] {bytes_sent} octets envoyés")
        
    except Exception as e:
        print(f"[SERVEUR] [{client_address[0]}:{client_address[1]}] Erreur: {e}")
    finally:
        client_socket.close()
        print(f"[SERVEUR] [{client_address[0]}:{client_address[1]}] Connexion fermée")

def server_program(host='0.0.0.0', port=8888, delay_min=5, delay_max=10, data_size=1048576):
    """
    Serveur TCP multi-clients qui répond avec un délai configurable
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((host, port))
        server_socket.listen(10)  # Queue de 10 connexions en attente
        print(f"[SERVEUR] Démarré sur {host}:{port}")
        print(f"[SERVEUR] Délai de réponse: {delay_min}-{delay_max} secondes")
        print(f"[SERVEUR] Taille des données: {data_size} octets ({data_size/1024/1024:.2f} Mo)")
        print(f"[SERVEUR] En attente de connexions...")
        
        while True:
            client_socket, client_address = server_socket.accept()
            
            # Créer un thread pour chaque client
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address, delay_min, delay_max, data_size),
                daemon=True
            )
            client_thread.start()
                
    except KeyboardInterrupt:
        print("\n[SERVEUR] Arrêt du serveur...")
    finally:
        server_socket.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Serveur TCP multi-clients avec délai configurable')
    parser.add_argument('--host', default='0.0.0.0', help='Adresse IP du serveur (défaut: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=8888, help='Port du serveur (défaut: 8888)')
    parser.add_argument('--delay-min', type=float, default=5.0, help='Délai minimum en secondes (défaut: 5)')
    parser.add_argument('--delay-max', type=float, default=10.0, help='Délai maximum en secondes (défaut: 10)')
    parser.add_argument('--data-size', type=int, default=1048576, help='Taille des données à envoyer en octets (défaut: 1048576 = 1 Mo)')
    
    args = parser.parse_args()
    server_program(args.host, args.port, args.delay_min, args.delay_max, args.data_size)


