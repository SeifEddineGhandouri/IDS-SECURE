import numpy as np
from sklearn.ensemble import IsolationForest
from scapy.all import IP, TCP, UDP
from src.utils.logger import logger
from src.utils.config import ML_CONTAMINATION

class AnomalyDetector:
    def __init__(self, alert_manager):
        self.alert_manager = alert_manager
        self.model = IsolationForest(contamination=ML_CONTAMINATION, random_state=42)
        self.data_buffer = []
        self.buffer_size = 500  # Nombre de paquets pour entraîner le modèle
        self.is_trained = False
        
    def extract_features(self, packet):
        """Extrait les caractéristiques numériques d'un paquet pour le ML"""
        if not packet.haslayer(IP):
            return None
            
        features = [
            len(packet),           # Taille du paquet
            packet[IP].ttl,       # Time To Live
            int(packet[IP].proto) # Protocole (6 TCP, 17 UDP)
        ]
        
        if packet.haslayer(TCP):
             features.append(packet[TCP].sport)
             features.append(packet[TCP].dport)
        elif packet.haslayer(UDP):
             features.append(packet[UDP].sport)
             features.append(packet[UDP].dport)
        else:
             features.append(0)
             features.append(0)
             
        return features

    def process_packet(self, packet):
        features = self.extract_features(packet)
        if not features:
            return

        # Phase 1: Collecte de données pour l'apprentissage initial
        if not self.is_trained:
            self.data_buffer.append(features)
            if len(self.data_buffer) >= self.buffer_size:
                self.train_model()
            return

        # Phase 2: Prédiction en temps réel
        prediction = self.model.predict([features])
        
        # -1 signifie anomalie (outlier)
        if prediction[0] == -1:
            src = packet[IP].src if packet.haslayer(IP) else "Unknown"
            self.alert_manager.log_alert(
                "Traffic Anomaly",
                f"Sastistical anomaly detected (Size: {features[0]}, Protocol: {features[2]})",
                "medium",
                src,
                details={"features": str(features)}
            )
            
            # Ré-entraînement progressif (optionnel mais recommandé pour s'adapter)
            # Ici on ajoute simplement au buffer pour un futur ré-entrainement si besoin
            # Pour simplifier, on ne le fait pas ici pour éviter de bloquer le thread

    def train_model(self):
        logger.info(f"Training Anomaly Detection Model with {len(self.data_buffer)} packets...")
        try:
            X = np.array(self.data_buffer)
            self.model.fit(X)
            self.is_trained = True
            logger.info("Model trained successfully. Real-time detection ACTIVATE.")
        except Exception as e:
            logger.error(f"Error training model: {e}")
