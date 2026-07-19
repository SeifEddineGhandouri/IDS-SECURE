import signal
import sys
import time
import threading
from src.utils.logger import logger
from src.utils.config import NETWORK_INTERFACE
from src.capture.sniffer import PacketSniffer
from src.alerting.alert_manager import AlertManager
from src.analysis.signatures import SignatureDetector
from src.analysis.anomaly import AnomalyDetector
from src.web.app import run_web_server

def main():
    logger.info("Initializing NetGuard-IDS...")

    # 1. Alerting System
    alert_manager = AlertManager()

    # 2. Analysis Engines
    sig_detector = SignatureDetector(alert_manager)
    anomaly_detector = AnomalyDetector(alert_manager)

    # Fonction de callback appelée pour chaque paquet
    def packet_callback(packet):
        try:
            # Dispatch vers les moteurs d'analyse
            sig_detector.process_packet(packet)
            anomaly_detector.process_packet(packet)
        except Exception as e:
            logger.error(f"Error processing packet: {e}")

    # 3. Capture Module
    sniffer = PacketSniffer(callback_function=packet_callback)

    # Gestion de l'arrêt propre (CTRL+C)
    def signal_handler(sig, frame):
        logger.info("\nShutting down NetGuard-IDS...")
        sniffer.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    # 4. Démarrage des modules
    try:
        # Start Web Interface
        logger.info("Starting Web Dashboard...")
        web_thread = threading.Thread(target=run_web_server, daemon=True)
        web_thread.start()
        logger.info(f"Dashboard available at http://localhost:5000")

        # Start Sniffer
        sniffer.start()

        # Boucle principale pour maintenir le programme en vie
        while True:
            time.sleep(1)
            
    except Exception as e:
        logger.critical(f"Fatal error: {e}")
        sniffer.stop()

if __name__ == "__main__":
    main()
