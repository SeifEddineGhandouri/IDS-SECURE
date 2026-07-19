from scapy.all import IP, TCP, ICMP, send
import time
import random

target_ip = "192.168.1.16" # IP détectée dans les logs 

def simulate_syn_flood():
    print(f"[*] Simulating SYN Flood on {target_ip}...")
    for _ in range(150): # > 100 threshold
        # Port aléatoire pour simuler de multiples connexions
        pkt = IP(dst=target_ip)/TCP(dport=80, flags="S", sport=random.randint(1024, 65535))
        send(pkt, verbose=0)
        time.sleep(0.01)
    print("[+] SYN Flood sent.")

def simulate_null_scan():
    print(f"[*] Simulating NULL Scan on {target_ip}...")
    pkt = IP(dst=target_ip)/TCP(dport=80, flags="")
    send(pkt, verbose=0)
    print("[+] NULL Scan sent.")

def simulate_icmp_flood():
    print(f"[*] Simulating ICMP (Ping) Flood on {target_ip}...")
    for _ in range(250):
        pkt = IP(dst=target_ip)/ICMP()
        send(pkt, verbose=0)
        time.sleep(0.005)
    print("[+] ICMP Flood sent.")

if __name__ == "__main__":
    time.sleep(2) # Attendre que l'IDS soit prêt si lancé en même temps
    simulate_null_scan()
    time.sleep(1)
    simulate_syn_flood()
    time.sleep(1)
    simulate_icmp_flood()
