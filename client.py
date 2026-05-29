import pygame
import socket
import threading
import json
import math
from constants import *
from shared import Player, Bullet, GameState, NetworkMessage

class GameClient:
    def __init__(self, server_host, server_port, player_name, player_color):
        self.server_host = server_host
        self.server_port = server_port
        self.player_name = player_name
        self.player_color = player_color
        
        self.socket = None
        self.player_id = None
        self.my_player = None
        self.players = {}
        self.bullets = {}
        self.platforms = []
        self.game_running = False
        self.connected = False
        
        self.lock = threading.Lock()
        
        # Input client
        self.keys_pressed = {}
        self.mouse_pos = (0, 0)
        self.last_shoot_time = 0
        
    def connect(self):
        """Se connecte au serveur"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.server_host, self.server_port))
            self.connected = True
            print(f"[CLIENT] Connecté à {self.server_host}:{self.server_port}")
            
            # Envoyer les infos de jointure
            msg = NetworkMessage("join", {
                'name': self.player_name,
                'color': self.player_color
            })
            self.socket.send((msg.to_json() + "\n").encode())
            
            # Thread de réception
            threading.Thread(target=self._receive_messages, daemon=True).start()
            
            return True
        except Exception as e:
            print(f"[CLIENT] Erreur de connexion: {e}")
            self.connected = False
            return False
    
    def _receive_messages(self):
        """Reçoit les messages du serveur"""
        buffer = ""
        try:
            while self.connected:
                data = self.socket.recv(4096).decode()
                if not data:
                    break
                
                buffer += data
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    if line.strip():
                        self._process_server_message(line)
        except Exception as e:
            print(f"[CLIENT] Erreur réception: {e}")
        finally:
            self.connected = False
    
    def _process_server_message(self, message_str):
        """Traite un message du serveur"""
        try:
            msg = NetworkMessage.from_json(message_str)
            
            if msg.msg_type == "join_success":
                self._handle_join_success(msg.data)
            elif msg.msg_type == "join_failed":
                print(f"[CLIENT] Échec jointure: {msg.data.get('reason')}")
                self.connected = False
            elif msg.msg_type == "game_started":
                with self.lock:
                    self.game_running = True
            elif msg.msg_type == "state_update":
                self._handle_state_update(msg.data)
            elif msg.msg_type == "server_full":
                print("[CLIENT] Serveur plein!")
                self.connected = False
        except Exception as e:
            print(f"[CLIENT] Erreur traitement message: {e}")
    
    def _handle_join_success(self, data):
        """Traite la confirmation de jointure"""
        with self.lock:
            self.player_id = data['player_id']
            player_dict = data['player']
            self.my_player = Player(**player_dict)
            self.players[self.player_id] = player_dict
            
            # Recréer les rects des plateformes
            for plat_data in data.get('platforms', []):
                self.platforms.append(pygame.Rect(plat_data[0], plat_data[1], plat_data[2], plat_data[3]))
        
        print(f"[CLIENT] Jointure réussie! ID: {self.player_id}")
    
    def _handle_state_update(self, data):
        """Met à jour l'état du jeu"""
        state = data.get('state', {})
        with self.lock:
            self.players = state.get('players', {})
            self.bullets = state.get('bullets', {})
    
    def send_input(self, vel_x, jump):
        """Envoie les inputs du joueur"""
        if not self.connected:
            return
        
        msg = NetworkMessage("input", {
            'vel_x': vel_x,
            'jump': jump
        })
        try:
            self.socket.send((msg.to_json() + "\n").encode())
        except:
            pass
    
    def send_shoot(self):
        """Envoie un tir"""
        if not self.connected:
            return
        
        msg = NetworkMessage("shoot", {
            'mouse_x': self.mouse_pos[0],
            'mouse_y': self.mouse_pos[1]
        })
        try:
            self.socket.send((msg.to_json() + "\n").encode())
        except:
            pass
    
    def start_game(self):
        """Demande le démarrage du jeu"""
        if not self.connected:
            return
        
        msg = NetworkMessage("start_game", {})
        try:
            self.socket.send((msg.to_json() + "\n").encode())
        except:
            pass

class GameRenderer:
    def __init__(self, client):
        self.client = client
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Platformer Multijoueur")
        self.font_small = pygame.font.Font(None, 24)
        self.font_large = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()
        self.lobby_screen = True
        
    def run(self):
        """Boucle de rendu"""
        running = True
        
        while running and self.client.connected:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.lobby_screen:
                    # Démarrer le jeu
                    self.client.start_game()
                    self.lobby_screen = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.client.send_shoot()
            
            if self.lobby_screen and self.client.game_running:
                self.lobby_screen = False
            
            if self.lobby_screen:
                self._render_lobby()
            else:
                self._render_game()
            
            self.clock.tick(FPS)
        
        pygame.quit()
    
    def _render_lobby(self):
        """Affiche le lobby"""
        self.screen.fill(UI_BG_COLOR)
        
        # Titre
        title = self.font_large.render("En attente des joueurs...", True, TEXT_COLOR)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
        
        # Afficher les joueurs connectés
        y = 150
        with self.client.lock:
            for pid, player_dict in self.client.players.items():
                player_name = player_dict['name']
                player_color_str = player_dict['color']
                color_tuple = PLAYER_COLORS.get(player_color_str, (128, 128, 128))
                
                # Carré de couleur
                pygame.draw.rect(self.screen, color_tuple, (100, y, 30, 30))
                
                # Nom du joueur
                text = self.font_small.render(f"{player_name} ({player_color_str})", True, TEXT_COLOR)
                self.screen.blit(text, (150, y + 5))
                
                y += 50
        
        # Instructions
        with self.client.lock:
            is_host = self.client.player_id == 0
        if is_host:  # Premier joeur (host)
            instr = self.font_small.render("ESPACE pour démarrer le jeu", True, (0, 100, 0))
        else:
            instr = self.font_small.render("En attente du host...", True, TEXT_COLOR)
        self.screen.blit(instr, (WIDTH // 2 - instr.get_width() // 2, HEIGHT - 100))
        
        pygame.display.flip()
    
    def _render_game(self):
        """Affiche le jeu"""
        # Gestion des inputs
        keys = pygame.key.get_pressed()
        vel_x = 0
        jump = False
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            vel_x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            vel_x = PLAYER_SPEED
        if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]:
            jump = True
        
        self.client.mouse_pos = pygame.mouse.get_pos()
        
        # Envoyer les inputs
        self.client.send_input(vel_x, jump)
        
        # Rendu
        self.screen.fill(BG_COLOR)
        
        # Plateformes
        for plat in self.client.platforms:
            pygame.draw.rect(self.screen, PLATFORM_COLOR, plat)
        
        # Balles
        with self.client.lock:
            for bullet_dict in self.client.bullets.values():
                bullet = Bullet(**bullet_dict)
                pygame.draw.circle(self.screen, (0, 0, 0), (int(bullet.x), int(bullet.y)), BULLET_SIZE)
            
            # Joueurs
            for pid, player_dict in self.client.players.items():
                player = Player(**player_dict)
                if not player.alive:
                    continue
                
                color_tuple = PLAYER_COLORS.get(player.color, (128, 128, 128))
                
                # Tête
                head_rect = player.get_head_rect()
                pygame.draw.rect(self.screen, color_tuple, (player.x, player.y, PLAYER_WIDTH, HEAD_HEIGHT))
                
                # Corps
                body_rect = player.get_rect()
                pygame.draw.rect(self.screen, color_tuple, body_rect)
                
                # Contour si c'est notre joueur
                with self.client.lock:
                    is_my_player = (pid == self.client.player_id)
                if is_my_player:
                    pygame.draw.rect(self.screen, (255, 255, 255), (int(player.x), int(player.y), PLAYER_WIDTH, PLAYER_HEIGHT), 2)
                
                # Afficher les infos du joueur
                hp_text = self.font_small.render(f"{player.name} ({player.hp}HP)", True, TEXT_COLOR)
                self.screen.blit(hp_text, (player.x, player.y - 30))
        
        # Viseur à la souris
        mx, my = pygame.mouse.get_pos()
        pygame.draw.circle(self.screen, (255, 0, 0), (mx, my), 5, 1)
        
        # Afficher le cooldown de tir
        if self.client.my_player:
            cooldown_text = self.font_small.render(f"Tir: {'Prêt' if self.client.my_player.shoot_cooldown <= 0 else chr(int(self.client.my_player.shoot_cooldown))}",
                                                    True, TEXT_COLOR)
            self.screen.blit(cooldown_text, (10, 10))
        
        pygame.display.flip()

def run_game(server_host, server_port, player_name, player_color):
    """Fonction utilitaire pour lancer le jeu client"""
    pygame.init()
    
    client = GameClient(server_host, server_port, player_name, player_color)
    
    if not client.connect():
        print("Impossible de se connecter au serveur")
        return
    
    # Attendre la confirmation de jointure (avec lock pour éviter race condition)
    import time
    timeout = time.time() + 10
    while time.time() < timeout:
        with client.lock:
            if client.player_id is not None:
                break
        time.sleep(0.05)
    
    with client.lock:
        if client.player_id is None:
            print("[ERREUR] Timeout de connexion au serveur")
            return
    
    renderer = GameRenderer(client)
    renderer.run()
