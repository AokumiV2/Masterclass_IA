# 🎮 Tetris - Python Edition

Ce projet est une implémentation complète du célèbre jeu vidéo **Tetris**, développé en Python en utilisant la bibliothèque **Pygame**. Le jeu propose une expérience visuelle agréable, des animations fluides, ainsi qu'une gestion avancée des collisions et des rotations des pièces.

## 🚀 Fonctionnalités

- **Interface graphique dynamique** utilisant Pygame.
- **Rotation avancée des pièces** avec gestion précise des "Wall Kicks" (ajustement des rotations proches des murs).
- **Prévisualisation de la pièce suivante**.
- **Animations visuelles** pour l'apparition des pièces et la disparition des lignes.
- **Gestion complète du score** avec sauvegarde des meilleurs scores.
- **Mode Zen** (optionnel).
- **Contrôle via clavier** intuitif et réactif.

## 🛠️ Installation

### 1. Prérequis

- Python 3.x
- Bibliothèque Pygame

Installe Pygame via pip :

```bash
pip install pygame
```

### 2. Récupération du projet

Clone le repository :

```bash
git clone https://github.com/AokumiV2/Tetris.git
cd Tetris
```

## 🎯 Lancer le jeu

Exécute simplement la commande suivante dans le dossier du projet :

```bash
python main.py
```

## 🎮 Contrôles

| Touche           | Action            |
|------------------|-------------------|
| `←` et `→`       | Déplacer la pièce |
| `↑`              | Rotation horaire  |
| `Z`              | Rotation antihoraire|
| `↓`              | Descente rapide   |
| `Espace`         | Descente instantanée|
| `P`              | Pause / Reprise   |
| `Entrée`         | Démarrer / Rejouer|
| `Échap`          | Retour au menu    |

## 📁 Structure du projet

```bash
Tetris/
├── constants.py
├── game.py
├── main.py
├── menu.py
├── tetrimino.py
├── high_score.txt
└── README.md
```

## 📌 Dépendances

- **Pygame** : gestion de l'affichage et des entrées utilisateur.

## 📝 Contribuer

Les contributions sont bienvenues ! N'hésite pas à soumettre une pull request pour améliorer le jeu ou corriger des bugs éventuels.

## 🎓 Auteur

Développé avec ❤️ par [AokumiV2](https://github.com/AokumiV2).

## 🧾 Licence

Ce projet est sous licence MIT. Consulte le fichier [LICENSE](LICENSE) pour plus de détails.

