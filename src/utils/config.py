import os

# --- Configuration Réseau ---
# Interface à écouter. Sur Windows, cela peut être complexe à identifier.
# 'None' laisse Scapy choisir l'interface par défaut.
NETWORK_INTERFACE = None 

# --- Configuration Détection ---
# Seuil de paquets pour considérer un flood (ex: Syn Flood)
SYN_FLOOD_THRESHOLD = 100
# Fenêtre de temps pour l'analyse en secondes
TIME_WINDOW = 10

# --- Configuration ML ---
# Contamination estimée pour Isolation Forest (pourcentage d'anomalies attendues)
ML_CONTAMINATION = 0.01

# --- Configuration Logging/Alerting ---
LOG_DIR = os.path.join(os.getcwd(), 'logs')
ALERTS_FILE = os.path.join(LOG_DIR, 'alerts.json')
PACKET_DUMP_FILE = os.path.join(LOG_DIR, 'captured_packets.pcap')

# --- Configuration Web ---
WEB_HOST = '0.0.0.0'
WEB_PORT = 5000
DEBUG_MODE = True

# Assurer que le dossier de logs existe
os.makedirs(LOG_DIR, exist_ok=True)
