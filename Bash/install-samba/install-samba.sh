#!/bin/bash

# Samba Server installieren
sudo apt-get update
sudo apt-get install samba -y

# Ordner erstellen
sudo mkdir /home/smb-share
sudo chmod 777 /home/smb-share

# Samba-Konfiguration bearbeiten
sudo bash -c 'cat << EOF >> /etc/samba/smb.conf
[Austausch]
    path = /home/smb-share
    writable = yes
    guest ok = yes
    read only = no
    create mask = 0666
    directory mask = 0777
EOF'

# Samba-Dienst neu starten
sudo systemctl restart smbd

echo "Samba-Server wurde installiert und der Ordner 'Austausch' wurde erstellt."
