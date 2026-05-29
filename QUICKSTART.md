# Guide de Démarrage Rapide - Platformer Multijoueur

## Première Utilisation

### Étape 1: Installation
```bash
cd "chemin/vers/le/dossier/platformer"
pip install -r requirements.txt
```

### Étape 2: Lancer le Jeu
```bash
python main.py
```

### Étape 3: Créer une Partie (HOST)
1. Appuyez sur **1** pour créer un serveur
2. Appuyez sur **ENTRÉE** pour continuer
3. Entrez votre pseudo
4. Appuyez sur **ENTRÉE** pour confirmer
5. Sélectionnez votre couleur avec **← / →**
6. Appuyez encore sur **ENTRÉE** pour lancer le jeu

### Étape 4: Rejoindre une Partie (CLIENTS)
1. Appuyez sur **2** pour rejoindre un serveur
2. Entrez l'adresse IP du serveur:
   - Juste l'IP: `192.168.1.5` (utilise le port 5000 par défaut)
   - Avec port: `192.168.1.5:5000` (pour un port personnalisé)
   - Pour la machine locale: `localhost` ou `127.0.0.1`
3. Appuyez sur **ENTRÉE**
4. Entrez votre pseudo (différent du host si possible)
5. Sélectionnez votre couleur (UNE COULEUR DIFFÉRENTE du host)
6. Appuyez sur **ENTRÉE**

### Étape 5: Démarrer le Jeu
- Le HOST verra l'écran "En attente des joueurs..."
- Une fois tous les joueurs connectés, le HOST appuie sur **ESPACE** pour démarrer

## Pendant le Jeu

### Contrôles
- **A/D** ou **Flèches**: Se déplacer
- **W/ESPACE/Flèche Haut**: Sauter
- **Souris**: Viser
- **Clic Gauche**: Tirer

### Objectif
- Tirer sur les autres joueurs
- Éviter les tirs des autres
- Chaque joueur a 4 HP
- 1 tir au corps = 1 dégât
- 1 tir à la tête = instant KO!

## Test sur une Seule Machine

Pour tester sur votre machine LOCAL avec plusieurs instances:

**Terminal 1 (Host):**
```bash
python main.py
# Choisir "1. Créer un serveur"
# Pseudo: "Alice", Couleur: "Red"
```

**Terminal 2 (Client):**
```bash
python main.py
# Choisir "2. Rejoindre un serveur"
# IP: localhost (ou laisser vide et appuyer ENTRÉE)
# Pseudo: "Bob", Couleur: "Blue"
```

**Terminal 3 (Client 2):**
```bash
python main.py
# Choisir "2. Rejoindre un serveur"
# IP: localhost
# Pseudo: "Charlie", Couleur: "Green"
```

Une fois tous connectés, le HOST (Alice) appuie sur ESPACE pour démarrer.

## Test en Réseau Local

1. **Host** obtient son adresse IP (Windows: `ipconfig`, Linux: `hostname -I`)
2. Les **Clients** utilisent cette IP au lieu de "localhost"

## Dépannage

| Problème | Solution |
|----------|----------|
| "Enchec jointure: Color taken" | Choisir une autre couleur |
| "Serveur plein!" | Attendre qu'un joueur se déconnecte |
| Impossible de se connecter | Vérifier l'IP, le port 5000 |
| Jeu ne démarre pas | Vérifier que tous les joueurs sont connectés |
| Première fenêtre ne répond pas | Cliquer dans la fenêtre pour la réactiver |

## Architecture du Jeu

```
main.py (Menu)
    ↓
client.py (Interface + Input)
    ↔ Socket TCP
server.py (Logique + Physics)
```

- **Port**: 5000 (configurable dans constants.py)
- **Protocole**: JSON sur TCP
- **Max joueurs**: 4
- **FPS**: 60
- **Tailles**: 1000x700 pixels

## Fichiers Importants
- `constants.py` - Configurations (gravity, vitesse, HP, etc.)
- `server.py` - Logique serveur
- `client.py` - Logique client
- `shared.py` - Classes partagées
- `requirements.txt` - Dépendances

Amusez-vous! 🎮
