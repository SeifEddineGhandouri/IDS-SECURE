from scapy.all import sniff, IP, TCP, UDP
import threading
import queue
from src.utils.config import NETWORK_INTERFACE
from src.utils.logger import logger

class PacketSniffer:
    def __init__(self, callback_function=None):
        """
        Args:
            callback_function: Fonction à appeler pour chaque paquet capturé (pour l'analyse)
        """
        self.interface = NETWORK_INTERFACE
        self.stop_sniffing = threading.Event()
        self.packet_queue = queue.Queue()
        self.callback = callback_function
        self.thread = None

    def _packet_handler(self, packet):
        """Callback interne de Scapy"""
        if self.callback:
            self.callback(packet)
            
    def start(self):
        """Lance la capture dans un thread séparé"""
        logger.info(f"Starting Packet Sniffer on interface: {self.interface or 'Default'}")
        self.thread = threading.Thread(target=self._sniff_loop, daemon=True)
        self.thread.start()

    def _sniff_loop(self):
        try:
            # prn est la fonction appelée pour chaque paquet
            # store=0 évite de garder les paquets en mémoire (fuite mémoire sinon)
            sniff(
                iface=self.interface,
                prn=self._packet_handler,
                store=0,
                stop_filter=lambda x: self.stop_sniffing.is_set()
            )
        except Exception as e:
            logger.critical(f"Sniffer failed: {e}")

    def stop(self):
        logger.info("Stopping Sniffer...")
        self.stop_sniffing.set()
        if self.thread:
            self.thread.join(timeout=2.0)
