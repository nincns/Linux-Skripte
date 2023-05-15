#!/bin/bash

# Nach Variablen fragen
read -p "Geben Sie den Benutzernamen ein: " BENUTZERNAME
read -s -p "Geben Sie das Passwort ein: " PASSWORT
read -p "Geben Sie den SSH-Schlüssel ein: " SSH_KEY

# Benutzeraccount erstellen
useradd -m "$BENUTZERNAME"

# Passwort setzen
echo "$BENUTZERNAME:$PASSWORT" | chpasswd

# Benutzer der sudo-Gruppe hinzufügen
usermod -aG sudo "$BENUTZERNAME"

# SSH-Verzeichnis erstellen und Berechtigungen setzen
mkdir -p /home/"$BENUTZERNAME"/.ssh
chmod 700 /home/"$BENUTZERNAME"/.ssh

# Public Key ins SSH-Verzeichnis schreiben
echo "$SSH_KEY" > /home/"$BENUTZERNAME"/.ssh/authorized_keys
chmod 600 /home/"$BENUTZERNAME"/.ssh/authorized_keys

# Besitzer des SSH-Verzeichnisses ändern
chown -R "$BENUTZERNAME":"$BENUTZERNAME" /home/"$BENUTZERNAME"/.ssh
