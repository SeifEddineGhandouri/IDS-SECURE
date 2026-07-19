import json
import time
import os
from datetime import datetime
from src.utils.config import ALERTS_FILE
from src.utils.logger import logger

class AlertManager:
    def __init__(self, alerts_file=ALERTS_FILE):
        self.alerts_file = alerts_file
        # Créer le fichier s'il n'existe pas
        if not os.path.exists(self.alerts_file):
            with open(self.alerts_file, 'w') as f:
                json.dump([], f)

    def log_alert(self, alert_type, message, severity="medium", source_ip="N/A", details=None):
        """
        Enregistre une alerte dans le fichier JSON et l'affiche dans la console.
        
        Args:
            alert_type (str): Type d'attaque (ex: 'SYN Scan', 'Anomaly')
            message (str): Description humaine
            severity (str): low, medium, high, critical
            source_ip (str): IP source suspecte
            details (dict): Données techniques supplémentaires
        """
        alert = {
            "timestamp": datetime.now().isoformat(),
            "type": alert_type,
            "message": message,
            "severity": severity,
            "source_ip": source_ip,
            "details": details or {}
        }
        
        # Log console
        if severity == "critical":
            logger.critical(f"ALERT [{alert_type}] {message} FROM {source_ip}")
        elif severity == "high":
            logger.error(f"ALERT [{alert_type}] {message} FROM {source_ip}")
        else:
            logger.warning(f"ALERT [{alert_type}] {message} FROM {source_ip}")

        # Sauvegarde persistante
        self._save_to_file(alert)

    def _save_to_file(self, alert):
        try:
            # Lecture du fichier existant
            with open(self.alerts_file, 'r') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
            
            data.append(alert)
            
            # Écriture (On garde les 1000 dernières alertes pour éviter un fichier géant)
            if len(data) > 1000:
                data = data[-1000:]
                
            with open(self.alerts_file, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            logger.error(f"Failed to save alert: {e}")

    def get_latest_alerts(self, limit=10):
        try:
            with open(self.alerts_file, 'r') as f:
                data = json.load(f)
            return sorted(data, key=lambda x: x['timestamp'], reverse=True)[:limit]
        except Exception:
            return []
