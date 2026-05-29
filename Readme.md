# Platformer Multijoueur - Jeu Réseau Local

Un jeu platformer 2D multijoueur en Python avec Pygame, supportant l'architecture client-serveur en réseau local.

## Fonctionnalités

✨ **Multijoueur Réseau Local**
- Architecture client-serveur TCP
- Jusqu'à 4 joueurs simultanés
- Synchronisation en temps réel

🎮 **Gameplay**
- Platformer 2D avec physique réaliste
- Système de tir avec visée à la souris
- Système de santé avec zones de dégât différentiées:
  - **Corps**: 4 tirs pour éliminer un joueur
  - **Tête**: 1 tir (zone délimitée supérieure)
- Cooldown de tir pour équilibrer le jeu
- Plateformes interactives

👥 **Système de Lobby**
- Chaque joueur choisit un pseudo unique
- 6 couleurs disponibles (pas de doublons)
- Interface de sélection facile

## Installation

### Prérequis
- Python 3.8+
- Pygame 2.0+

### Installation des dépendances
```bash
pip install -r requirements.txt
```

## Démarrage du Jeu

```bash
python main.py
```

### Menu Principal
1. **Créer un serveur (HOST)**: Lancez le jeu en mode serveur et attendez que les clients se connectent
2. **Rejoindre un serveur (CLIENT)**: Connectez-vous à un serveur existant

## Contrôles de Jeu

### Mouvement
- **A / Flèche Gauche**: Se déplacer à gauche
- **D / Flèche Droite**: Se déplacer à droite
- **ESPACE / Flèche Haut / W**: Sauter

### Combat
- **Souris**: Viser
- **Clic Gauche**: Tirer (cooldown entre les tirs)

### Menu
- **ENTRÉE**: Confirmer
- **ESC**: Retours au menu
- **← / →**: Sélectionner une couleur

## Architecture Réseau

### Architecture Client-Serveur
- **Serveur**: Gère l'état du jeu, la physique, les collisions, les tirs
- **Clients**: Envoient les inputs (mouvements, tirs) et reçoivent l'état du jeu
- **Port par défaut**: 5000
- **Protocole**: TCP avec messages JSON

### Messages Réseau
- `join`: Rejoindre le jeu (pseudo + couleur)
- `input`: Envoyer les mouvements du joueur
- `shoot`: Envoyer un tir
- `state_update`: Mise à jour de l'état du jeu
- `game_started`: Le jeu a commencé
- `join_success`/`join_failed`: Confirmation de connexion

## Système de Santé

Chaque joueur possède 4 points de vie (HP).

### Dégâts des Tirs
- **Corps**: 1 dégât par tir
- **Tête** (zone supérieure): 4 dégâts par tir = élimination instantanée

### Invincibilité
Après avoir été touché, un joueur est invincible pendant 60 frames (env. 1 seconde à 60 FPS).

## Système de Plateformes

Le jeu inclut plusieurs plateformes dont:
- Le sol (plateforme inférieure)
- Plateformes flottantes de différentes hauteurs
- Limites de la map

## Configuration

Les paramètres peuvent être modifiés dans `constants.py`:
- `WIDTH`, `HEIGHT`: Dimensions de la fenêtre
- `FPS`: Images par seconde
- `GRAVITY`: Force de gravité
- `PLAYER_SPEED`: Vitesse de déplacement
- `JUMP_STRENGTH`: Force du saut
- `BULLET_SPEED`: Vitesse des projectiles
- `SHOOT_COOLDOWN`: Refroidissement entre les tirs (ms)
- `MAX_HP`: Points de vie maximum
- `DEFAULT_PORT`: Port réseau par défaut

## Structure des Fichiers

```
plateformer/
├── main.py          # Point d'entrée, menu principal
├── constants.py     # Configuration et constantes du jeu
├── shared.py        # Classes partagées (Player, Bullet, GameState)
├── server.py        # Logique du serveur
├── client.py        # Logique du client et rendu
├── requirements.txt # Dépendances Python
└── Readme.md       # Ce fichier
```

## Exemple d'Utilisation

**Terminal 1 - Créer un serveur:**
```bash
python main.py
# Menu -> 1. Créer un serveur
# Choisir pseudo et couleur
```

**Terminal 2/3/4 - Se connecter au serveur (sur la même machine ou réseau):**
```bash
python main.py
# Menu -> 2. Rejoindre un serveur
# Entrer l'IP du serveur (ou "localhost" pour la machine locale)
# Choisir pseudo et couleur différente
```

Une fois tous les joueurs connectés, le HOST peut appuyer sur ESPACE pour démarrer le jeu.

## Troubleshooting

### "Échec jointure: Color taken"
La couleur que vous avez choisie est déjà utilisée. Sélectionnez une autre couleur.

### "Serveur plein!"
Le serveur a atteint le nombre maximum de joueurs (4). Attendez qu'un joueur se déconnecte.

### Impossible de se connecter
- Vérifiez que vous utilisez la bonne adresse IP du serveur
- Vérifiez le port par défaut (5000)
- S'il y a un pare-feu, autorisez le port 5000

## À Faire (Améliorations Futures)

- [ ] Système de respawn
- [ ] Armes spéciales
- [ ] Power-ups
- [ ] Effets visuels et son
- [ ] Système de points/classement
- [ ] Chat in-game
- [ ] Support de plus de 4 joueurs
- [ ] Mode de jeu personnalisé

## Auteur
Moi et pas toi
Jeu développé avec Python et Pygame.

## Licence

Libre d'utilisation et de modification.
