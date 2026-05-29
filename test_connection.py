#!/usr/bin/env python
"""Test de connexion client-serveur"""
import threading
import time
from server import GameServer
from client import GameClient
from constants import DEFAULT_PORT

def test_connection():
    print("=" * 60)
    print("TEST DE CONNEXION CLIENT-SERVEUR")
    print("=" * 60)
    
    # Démarrer le serveur dans un thread
    server = GameServer(DEFAULT_PORT)
    server_thread = threading.Thread(target=server.start, daemon=True)
    server_thread.start()
    
    time.sleep(1)  # Attendre que le serveur démarre
    
    print("\n[TEST] Création dun client...")
    client = GameClient("localhost", DEFAULT_PORT, "TestPlayer", "Red")
    
    print("[TEST] Tentative de connexion...")
    if not client.connect():
        print("[ERREUR] Impossible de se connecter")
        return False
    
    print("[TEST] Attente de la confirmation de jointure...")
    timeout = time.time() + 5
    player_id_received = None
    
    while time.time() < timeout:
        with client.lock:
            if client.player_id is not None:
                player_id_received = client.player_id
                break
        time.sleep(0.1)
    
    if player_id_received is not None:
        print(f"[SUCCESS] Joueur reçu! ID: {player_id_received}")
        print(f"[SUCCESS] Pseudo: {client.player_name}")
        print(f"[SUCCESS] Couleur: {client.player_color}")
        print(f"[SUCCESS] Plateformes chargées: {len(client.platforms)}")
        print(f"\n[OK] La connexion fonctionne correctement!")
        return True
    else:
        print("[ERREUR] Timeout - Pas de player_id reçu")
        return False

if __name__ == "__main__":
    success = test_connection()
    exit(0 if success else 1)
