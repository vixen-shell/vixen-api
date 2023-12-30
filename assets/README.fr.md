# ![vixen logo](/assets/vixen_logo_md.png) Projet Vixen Shell

## Environnement de bureau Linux

Le projet [Vixen Shell](https://github.com/vixen-shell) représente une initiative visant à créer un environnement de bureau convivial pour les utilisateurs de Linux, centré sur le développement. Fondé sur le gestionnaire de fenêtre [Hyprland](https://github.com/hyprwm/Hyprland), ce projet se distingue par son utilisation de Python pour le back-end et de technologies web telles que JavaScript, HTML et CSS pour l'interface utilisateur (front-end).

# ![vixen logo](/assets/vixen_logo_md.png) Vixen API

## API pour la communication entre interfaces et système

Ce projet est une composante essentiel du back-end de [Vixen Shell](https://github.com/vixen-shell), il implémente une API développée en python avec la librairie fastAPI permettant aux front-end de [Vixen Shell](https://github.com/vixen-shell) de communiquer avec [Hyprland](https://github.com/hyprwm/Hyprland) (window manager) ainsi qu'avec linux. Nous avons notamment la possibilité grâce à cette API de récupérer le flux d'évènements provenant du socket UNIX d'[Hyprland](https://github.com/hyprwm/Hyprland) via un WebSocket.

> **Note :** C'est un projet de développement qui vient tout juste de franchir sa phase proof of concept et se trouve encore en version alpha.