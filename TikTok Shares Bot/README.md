# Gravity Staircase Animation

Ce dépôt contient une petite animation interactive écrite avec [pygame](https://www.pygame.org/)
qui simule la chute d'une balle sur un escalier infini qui descend progressivement.

## Prérequis

- Python 3.10 ou version ultérieure
- Pygame

Installez la dépendance principale avec pip :

```bash
pip install pygame
```

## Lancer l'animation

Exécutez simplement le script suivant :

```bash
python gravity_animation.py
```

Une fenêtre s'ouvre et affiche :

- Une série de marches générées à l'infini vers le bas
- Une balle qui avance horizontalement, subit la gravité et rebondit légèrement
- Un léger suivi de caméra qui permet d'observer la descente sans fin

Fermez la fenêtre (ou appuyez sur la croix) pour quitter l'animation.

## Structure du projet

- `gravity_animation.py` : script principal de l'animation
- `main.py` : code legacy du projet original (ancien bot TikTok)
- `setup.py` : métadonnées d'installation héritées

## License

Le code source est distribué sans garantie. Utilisez-le, modifiez-le et partagez-le librement.
