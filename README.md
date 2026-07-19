# 🛡️ IDS Project – Intrusion Detection System en Python

## 📌 Description
Ce projet implémente un **IDS (Intrusion Detection System)** modulaire en Python. Il combine une détection **par signatures** et **par anomalies** pour identifier en temps réel les menaces réseau. Le projet est conçu pour un usage académique et professionnel, avec une architecture claire et extensible.

---

## 🏗️ Architecture

Le projet est organisé en modules indépendants :

```text
NetGuard-IDS/
├── main.py              # Script principal IDS (détection en temps réel)
├── kali_attack_menu.py  # Menu d'attaque Kali Linux
├── requirements.txt     # Dépendances Python
├── src/
│   ├── alerting/        # Gestion des alertes et journalisation
│   ├── analysis/        # Détection par signatures et détection d'anomalies
│   ├── capture/         # Capture des paquets réseau avec Scapy
│   ├── utils/           # Configuration, logger et utilitaires
│   └── web/             # Dashboard Flask + templates
├── logs/                # Stockage des alertes et captures
└── tests/               # Scripts de test / simulation
```

### 🔄 Flux de fonctionnement
1. **Capture réseau (`src/capture/`)** → collecte des paquets via Scapy.
2. **Analyse & détection (`src/analysis/`)** → règles signatures + modèles ML.
3. **Alerting (`src/alerting/`)** → génération de logs, alertes et stockage.
4. **Dashboard (`src/web/`)** → interface Flask pour visualiser les résultats.

---

## 🚀 Installation

1. Cloner le repo :

```bash
git clone https://github.com/SeifEddineGhandouri/IDS-SECURE.git
cd IDS-SECURE
```

2. Créer un environnement virtuel :

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # Windows
# source .venv/bin/activate      # Linux/Mac
```

3. Installer les dépendances :

```bash
pip install -r requirements.txt
```

---

## ▶️ Utilisation

### 9.3 Détection d'intrusions en temps réel
Lancer le moteur IDS :

```bash
python main.py
```

Ce lancement :
- initialise le sniffer réseau,
- démarre la détection par signatures et par anomalies,
- affiche les alertes en temps réel dans la console.

Exemples d’alertes détectées :
- `PoD Attack Detected`
- `Buffer Overflow`
- `SYN Flood`
- `NULL Scan`
- `XMAS Scan`

### 9.4 Lancement du serveur Flask
Le serveur web démarre automatiquement depuis `main.py`, mais peut aussi être lancé séparément :

```bash
python src/web/app.py
```

Accéder au dashboard :

```text
http://127.0.0.1:5000
```

En environnement VMware, l’interface peut être accessible sur :

```text
http://192.168.209.133:5000
```

Points importants :
- les requêtes entrantes `GET /api/alerts` montrent la communication frontend/backend,
- le dashboard récupère les alertes JSON en temps réel.

### 9.5 Interface de connexion IDS Secure
La page de connexion est disponible sur `/login`.

- champs : `Utilisateur` et `Mot de passe`
- identifiant par défaut : `admin`
- message en rouge : `Veuillez vous connecter pour accéder à cette page`
- interface sombre avec icône bouclier
- bouton `Se Connecter`

### 9.6 Interface de connexion – thème néon
L’interface propose un style sombre et moderne :

- bordures lumineuses autour des champs,
- mot de passe masqué,
- message d’erreur rouge lors d’une tentative sans authentification,
- bouton violet `Se Connecter`.

### 9.7 Menu d'attaque dans Kali Linux
Lancer le script d’attaque :

```bash
python kali_attack_menu.py
```

- cible : `192.168.209.133`
- attaques proposées : `SYN Flood`, `NULL Scan`, `XMAS Scan`, `ICMP Flood`
- note : vérifier que l’IDS Windows est actif avant le test

### 9.8 Tableau de bord IDS en temps réel
Le dashboard affiche :

- les alertes détectées en direct,
- la sévérité de chaque événement,
- l’adresse IP source,
- l’heure de l’alerte.

Dans une démonstration typique :
- Kali Linux lance un scan de port,
- l’IDS détecte l’attaque en temps réel,
- le tableau de bord affiche les alertes critiques et moyennes.

### 9.9 Visualisation des menaces
Le dashboard est conçu pour présenter clairement les menaces :

- répartition des niveaux de gravité,
- histogramme des IP les plus agressives,
- tendances du trafic et des alertes.

### 9.10 Analyse graphique – IDS SECURE
Ce type de monitor peut inclure :

- graphiques en secteurs pour la répartition des gravités,
- histogrammes des IP les plus actives,
- liste des événements avec filtres par sévérité.

Exemple :
- `CRITICAL : 1.87 %`
- `MEDIUM : 95.3 %`
- alertes `Suspiciously Large Packet (PoD/Buffer Overflow)`.

### 9.11 Liste des alertes IDS
Le tableau de bord peut montrer des alertes telles que :

- scans de ports (sévérité haute),
- attaques `SYN Flood` (sévérité critique),
- horodatage précis de chaque événement.

### 9.12 Génération de rapports PDF
Un script de génération de rapport PDF peut être ajouté dans `src/alerting/` comme `report_gen.py` pour produire un fichier `IDS_Report.pdf` récapitulant les alertes.

### 9.13 IDS CORE DASHBOARD
Le dashboard principal peut afficher :

- `TOTAL TRAFFIC ANALYSÉ`,
- `ALERTES SÉCURITÉ`,
- un bouton `Générer Rapport PDF`,
- un bouton `Déconnexion`.

### 9.14 Rapport IDS PDF
Le rapport PDF peut résumer :

- 1000 alertes détectées,
- 14 alertes critiques,
- 8 alertes de haute sévérité,
- table des 50 dernières alertes.

---

## 🔍 Fonctionnalités

- Détection en temps réel : port scans, SYN Flood, ICMP Flood, XMAS/NULL scans
- Dashboard Flask interactif
- Authentification basique à la connexion
- Architecture modulaire et extensible

## 👨‍💻 Auteur
Projet réalisé par **Seif Eddine Ghandouri**
Université Tek-UP – Année universitaire 2025-2026

---

👉 Ce README est prêt pour GitHub : il explique **l’architecture**, **les modules**, et **les modes de lancement** (IDS, Flask, PDF).