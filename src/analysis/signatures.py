from scapy.all import IP, TCP, ICMP
from collections import defaultdict
import time
from src.utils.logger import logger
from src.utils.config import SYN_FLOOD_THRESHOLD, TIME_WINDOW

class SignatureDetector:
    def __init__(self, alert_manager):
        self.alert_manager = alert_manager
        # Stockage pour le tracking de flow (IP Source -> Count)
        self.syn_counter = defaultdict(list)
        self.icmp_counter = defaultdict(list)

    def process_packet(self, packet):
        """Point d'entrée pour l'analyse par signature"""
        if not packet.haslayer(IP):
            return

        src_ip = packet[IP].src
        
        # 1. Détection SYN Flood (TCP)
        if packet.haslayer(TCP):
            flags = packet[TCP].flags
            # 'S' = SYN (0x02)
            if flags == 0x02:
                self._check_syn_flood(src_ip)
            
            # 2. Détection SCAN NULL (Aucun flag)
            # 0x00 = Aucun flag
            if flags == 0x00:
                self.alert_manager.log_alert(
                    "NULL Scan", 
                    f"Possible NULL Scan detected per TCP flags detection", 
                    "high", 
                    src_ip
                )
                
            # 3. Détection SCAN XMAS (FIN, URG, PUSH)
            # 0x29 = F, P, U set
            if flags == 0x29:
                self.alert_manager.log_alert(
                    "XMAS Scan", 
                    f"Possible XMAS Scan detected (FIN+URG+PUSH)", 
                    "high", 
                    src_ip
                )

        # 4. ICMP Flood
        if packet.haslayer(ICMP):
            if packet[ICMP].type == 8: # Echo Request
                self._check_icmp_flood(src_ip)

    def _check_syn_flood(self, src_ip):
        now = time.time()
        # Ajouter le timestamp actuel
        self.syn_counter[src_ip].append(now)
        
        # Nettoyer les timestamps vieux de > TIME_WINDOW secondes
        self.syn_counter[src_ip] = [t for t in self.syn_counter[src_ip] if now - t < TIME_WINDOW]
        
        count = len(self.syn_counter[src_ip])
        if count > SYN_FLOOD_THRESHOLD:
            # Pour éviter de spammer les logs, on check si c'est un multiple du seuil ou la première fois
            if count == SYN_FLOOD_THRESHOLD + 1:
                self.alert_manager.log_alert(
                    "SYN Flood", 
                    f"High rate of SYN packets detected ({count} packets/{TIME_WINDOW}s)", 
                    "critical", 
                    src_ip,
                    details={"rate": count, "window": TIME_WINDOW}
                )

    def _check_icmp_flood(self, src_ip):
        now = time.time()
        self.icmp_counter[src_ip].append(now)
        self.icmp_counter[src_ip] = [t for t in self.icmp_counter[src_ip] if now - t < TIME_WINDOW]
        
        count = len(self.icmp_counter[src_ip])
        # Seuil fixé arbitrairement un peu plus haut pour le Ping
        threshold = SYN_FLOOD_THRESHOLD * 2 
        
        if count > threshold:
             if count == threshold + 1:
                self.alert_manager.log_alert(
                    "ICMP Flood", 
                    f"Ping Flood detected ({count} packets/{TIME_WINDOW}s)", 
                    "medium", 
                    src_ip
                )
