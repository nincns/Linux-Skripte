#!/bin/bash

echo "Bitte wählen Sie den zu verwendenden USB-Stick aus: "
lsblk #zeigt alle angeschlossenen Speichermedien

read selected_disk #bittet den Benutzer, eine Auswahl zu treffen

echo "Das ausgewählte Laufwerk ist: $selected_disk"

echo "Kopiere relevanten Inhalt von SD Karte zum USB-Stick ..."

sudo dd bs=4M if=/dev/mmcblk0p1 of=/dev/$selected_disk conv=fsync #kopiert die Bootpartition auf den USB-Stick
sudo dd bs=4M if=/dev/mmcblk0p2 of=/dev/$selected_disk2 conv=fsync #kopiert die Root-Partition auf den USB-Stick

echo "Ändere Boot-Parameter, um von USB-Stick zu booten ..."

sudo sed -i 's/root=\/dev\/mmcblk0p2/root=\/dev\/sda2/' /boot/cmdline.txt #ändert den Pfad zur Root-Partition auf dem USB-Stick

echo "Fertig! Bitte starten Sie das System neu, um vom USB-Stick zu booten."
