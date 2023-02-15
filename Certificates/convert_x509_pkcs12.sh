#!/bin/bash

# Prompt for user input
read -p "Enter the filename of the certificate file in PEM format: " CERT_FILE
read -p "Enter the filename of the private key file in PEM format: " KEY_FILE

# Define variables for PKCS12 conversion
PKCS12_FILE="${CERT_FILE%.*}.p12"
read -s -p "Enter the password for the PKCS12 file: " PKCS12_PASSWORD
echo ""

# Define variables for x509 conversion
X509_FILE="${CERT_FILE%.*}_converted.crt"

# Create a menu to select the conversion
PS3="Select an option: "
options=("Convert x509 to PKCS12" "Convert PKCS12 to x509" "Exit")
select opt in "${options[@]}"
do
    case $opt in
        "Convert x509 to PKCS12")
            # Convert the certificate to PKCS12
            openssl pkcs12 -export -in "$CERT_FILE" -inkey "$KEY_FILE" -out "$PKCS12_FILE" -passout pass:"$PKCS12_PASSWORD"
            echo "Certificate has been saved in PKCS12 format as $PKCS12_FILE."
            break
            ;;
        "Convert PKCS12 to x509")
            # Convert the certificate to x509
            openssl pkcs12 -in "$CERT_FILE" -nodes -out "$X509_FILE"
            echo "Certificate has been saved in x509 format as $X509_FILE."
            break
            ;;
        "Exit")
            break
            ;;
        *) echo "Invalid option $REPLY";;
    esac
done
