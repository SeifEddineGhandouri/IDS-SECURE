# NetGuard-IDS

NetGuard-IDS est un système de détection d'intrusion réseau en Python. Il capture le trafic réseau, applique des règles de détection par signature et des modèles d'anomalie, puis alerte en temps réel via une interface web.

## Fonctionnalités

- Capture de paquets en temps réel avec Scapy
- Détection de signatures : `SYN Flood`, `NULL Scan`, `XMAS Scan`, `ICMP Flood`
- Détection d'anomalies avec Isolation Forest
- Dashboard Flask pour afficher les alertes en direct
- Page de connexion sécurisée avant accès au tableau de bord
- Script `kali_attack_menu.py` pour simuler des attaques depuis Kali Linux

## Installation

1. Cloner le dépôt
2. Créer un environnement virtuel Python

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # PowerShell sur Windows
pip install -r requirements.txt
```

## Exécution du IDS

Lancer le service principal :

```bash
python main.py
```

- Le serveur web Flask démarre sur `http://0.0.0.0:5000`
- Ouvrir `http://localhost:5000` ou `http://<IP_VM>:5000`
- Page de connexion disponible sur `/login`
- Identifiants par défaut : `admin` / `admin`

## Interface Web

- `GET /api/alerts` renvoie les alertes récentes au format JSON
- Le dashboard affiche les alertes et leur niveau de gravité
- Si l'utilisateur n'est pas connecté, il est redirigé vers la page de connexion avec un message :
  - `Veuillez vous connecter pour accéder à cette page`

## Script de simulation d'attaque (Kali Linux)

Utiliser le script `kali_attack_menu.py` pour lancer des attaques ciblant l'IDS :

```bash
python kali_attack_menu.py
```

Le menu propose des attaques interactives sur l'adresse `192.168.209.133`, et permet de valider la détection des paquets suspects par le moteur IDS.

- Menu interactif pour choisir le type d'attaque
- Attaques proposées : `SYN Flood`, `NULL Scan`, `ICMP Flood`, `XMAS Scan`
- Permet de vérifier la détection et la réactivité du moteur IDS

## Notes

- Sur VMware, assurez-vous que la VM Kali et la VM Windows sont sur le même réseau
- Vérifiez que l'IDS Windows est actif avant de lancer les attaques
- Contrôles réalisés : alertes en console, logs dans `logs/alerts.json`, requêtes web vers `/api/alerts`

## Contribution

Ce projet peut être poussé sur GitHub avec une explication claire des composants suivants :
- capture réseau
- détection par signature
- détection d'anomalie
- interface web sécurisée
- script de test d'attaque Kali

---

*Projet éducatif et fonctionnel de détection d'intrusion*.
