import os

# Get a list of available text files
path = "."
text_files = [file for file in os.listdir(path) if file.endswith(".txt")]
if not text_files:
    print("There are no text files in the current directory.")
    exit()

# Display a menu of available text files
print("Available text files:")
for i, file in enumerate(text_files):
    print(f"{i+1}. {file}")
file_choice = int(input("Select a file: "))
if file_choice not in range(1, len(text_files)+1):
    print("Invalid input.")
    exit()
filename = text_files[file_choice-1]

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

# Load the selected text file
with open(filename, "r") as file:
    text = file.read()

# Generate the G-code
lines = text.split("\n")
gcode = []
for line in lines:
    for word in line.split():
        for letter in word:
            gcode.append(f"G1 X{ord(letter)} Y{ord(letter)} Z1 F{speed}")
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
