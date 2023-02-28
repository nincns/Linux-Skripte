import os

# Load the text file
filename = input("Enter the name of the text file: ")
if not os.path.isfile(filename):
    print("The file does not exist.")
    exit()
with open(filename, "r") as file:
    text = file.read()

# Ask for motor speed
speed = float(input("Enter the motor speed: "))

# Font selection menu
font_choices = ["Arial", "Tahoma", "Helvetica", "Times New Roman"]
print("Available fonts:")
for i, font in enumerate(font_choices):
    print(f"{i+1}. {font}")
font_choice = int(input("Select a font: "))
if font_choice not in range(1, len(font_choices)+1):
    print("Invalid input.")
    exit()
font = font_choices[font_choice-1]

# Ask for font size
font_size = int(input("Enter the font size: "))

# Generate the G-code
lines = text.split("\n")
gcode = []
for line in lines:
    for word in line.split():
        gcode.append(f"G1 X{ord(word)} Y{ord(word)} Z1 F{speed}")
        gcode.append(f"G1 Z0")
gcode = "\n".join(gcode)

# Output the G-code
print("Generated G-code:")
print(f"Text: {text}")
print(f"Font: {font}")
print(f"Font size: {font_size}")
print(f"Speed: {speed}")
print("G-code:")
print(gcode)

# Save the G-code to a file
save_filename = input("Enter the name to save the G-code file: ")
with open(save_filename, "w") as file:
    file.write(gcode)
print(f"G-code saved to {save_filename}")
