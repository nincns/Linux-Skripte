#!/usr/bin/env python3
import hashlib

text = input("Gib einen Text ein: ")
md5hash = hashlib.md5(text.encode()).hexdigest()

print("Der MD5-Hash des eingegebenen Texts lautet:", md5hash)
