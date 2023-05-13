#!/usr/bin/env python3
import subprocess
import datetime

def scan_ip(ip, scan_type):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if scan_type == 1:
        command = f"nmap {ip}"
    elif scan_type == 2:
        command = f"nmap -p- {ip}"
    else:
        print("Ungültige Option!")
        return

    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    filename = f"scan_results_{ip.replace('/', '-')}.txt"
    with open(filename, "a") as file:
        file.write(f"Scan-Ergebnisse für {ip} am {timestamp}:\n")
        file.write(result.stdout)
        file.write("\n")

def parse_ip_range(ip_range):
    if '-' not in ip_range:
        return [ip_range]
    ip_start, ip_end = ip_range.split('-')
    ip_parts_start = ip_start.split('.')
    ip_parts_end = ip_end.split('.')
    if len(ip_parts_start) != 4 or len(ip_parts_end) != 4:
        print('Ungültige IP-Bereichsformat.')
        return []
    start = int(ip_parts_start[-1])
    end = int(ip_parts_end[-1])
    ips = []
    for i in range(start, end + 1):
        ip_parts_start[-1] = str(i)
        ips.append('.'.join(ip_parts_start))
    return ips

ip_range = input("Bitte gib den IP-Bereich ein (im Format IP-Start-IP-Ende): ")

ips = parse_ip_range(ip_range)

if not ips:
    exit()

scan_type = int(input("Bitte wähle den Scan-Typ:\n1. Standard\n2. Erweitert\n"))

for ip in ips:
    scan_ip(ip, scan_type)
