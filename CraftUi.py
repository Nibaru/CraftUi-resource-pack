import json
import yaml
import shutil
import os

global currentChar

startChar = 0xE001
currentChar = 0

count = 0;

id = 'craftui'

character = {
    "file": "",
    "chars": [],
    "height": 0,
    "ascent": 0,
    "type": "bitmap"
}


default = {
    "providers": [

    ]
}

item_font = {
    "providers": [

    ]
}

legend = {}





alpha = {
    "ascent": 0,
    "type": "bitmap",
    "file": "minecraft:font/ascii.png",
    "chars": [
    ]
}





def getCurrentChar():
    global currentChar
    return chr(startChar + currentChar)

def nextChar():
    global currentChar
    currentChar = currentChar + 1

def setChar(ch):
    global currentChar
    currentChar = ord(ch)
    
def getLastChar():
    global currentChar
    return chr(currentChar - 1)

def appendCharacter(name, height, ascent, file, font=default):
    ch = getCurrentChar()

    if name in legend:
        legendData = legend[name]
    else:
        legendData = {"chars": []}

    data = character.copy()
    data["chars"] = [ch]
    data["height"] = height
    data["ascent"] = ascent
    data["file"] = file
    font["providers"].append(data)

    legendData["chars"].append(ch)
    legend[name] = legendData

    nextChar()


def appendCharacterAscentPixelRange(name, height, ascentStart, total, file):
    for i in range(0, total):
        appendCharacter(name, height, -abs(ascentStart + i), file)

def appendCharacterAscentImgRange(name, height, ascentStart, total, file):
    for i in range(1, total+1):
        appendCharacter(name, height, -abs(ascentStart + (i * height)), file)

def appendCharacterHeightRange(name, height, ascent, total, file):
    for i in range(0, abs(total)):
        newHeight = height + i if total > 0 else height - i
        appendCharacter(name, newHeight, ascent, file)


aplhaCharMap = [
    "                ",
    "                ",
    " !\"#$%&'()*+,-./",
    "0123456789:;<=>?",
    "@ABCDEFGHIJKLMNO",
    "PQRSTUVWXYZ[\]^_",
    "`abcdefghijklmno",
    "pqrstuvwxyz{|}~ ",
    "                ",
    "£ƒ              ",
    "ªº¬«»           ",
    "░▒▓│┤╡╢╖╕╣║╗╝╜╛┐",
    "└┴┬├─┼╞╟╚╔╩╦╠═╬╧",
    "╨╤╥╙╘╒╓╫╪┘┌█▄▌▐▀",
    "∅∈              ",
    "≡±≥≤⌠⌡÷≈°∙√ⁿ²■  "
]


def getCharList():
    chars = []
    legendData = {}
    for line in aplhaCharMap:
        row = ""
        for c in line:
            if c == " ":
                row = row + "\u0000" 
                nextChar()
            else:
                row = row + chr(ord(getCurrentChar()) + 3)
                legendData[c] = chr(ord(getCurrentChar()) + 3)
                nextChar()
        chars.append(row)
    return chars, legendData

def appendAplha(name, ascent):

    alphaCopy = alpha.copy()
    alphaCopy["ascent"] = ascent


    alphaCopy["chars"], legendData = getCharList()

    default["providers"].append(alphaCopy)
    legend[name] = legendData


#Loop Though All Minecraft image textures and add them to the atlas
def appendMinecraftTextures(folder_path):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    
    for filename in os.listdir(folder_path):
        if os.path.splitext(filename)[1].lower() in image_extensions:
            appendCharacter(filename, 16, 13, f"minecraft:item/{filename}", font=item_font)

appendCharacterAscentImgRange("slot/blank", 18, -14, 6, f"{id}:gui/slot/blank.png")
appendCharacterAscentImgRange("slot/grid", 18, -14, 6, f"{id}:gui/slot/grid.png")

#TODO ADD THESE
#appendCharacterAscentImgRange("slot/grid_inventory", 18, -14, 3, f"{id}:gui/slot/grid.png")
#appendCharacterAscentPixelRange("scroller/vertical", 15, 5, 92, "minecraft:gui/sprites/container/creative_inventory/scroller.png")


appendCharacterHeightRange("space/negative", 1, -32768, -200, f"{id}:font/space_split.png")
appendCharacterHeightRange("space/positive", 1, -32768, 200, f"{id}:font/space_split.png")

appendCharacter("gui/blank", 222, 13, f"{id}:gui/background/blank.png")
appendCharacter("gui/blank_inventory", 222, 13, f"{id}:gui/background/blank_inventory.png")

appendMinecraftTextures("C:/Users/nicks/Documents/Minecraft-projects/Minecraft Resources/1.20.4/assets/minecraft/textures/item")

for i in range(0, 6):
    appendAplha(f"slot/{i}", -14 -(18 * i))
    appendAplha(f"shadow/{i}", -15 -(18 * i))

with open("pack/assets/craftui/font/items.json", "w") as file:
    json.dump(item_font, file, skipkeys=True, indent=4)

with open("pack/assets/minecraft/font/default.json", "w") as file:
    json.dump(default, file, skipkeys=True, indent=4)

shutil.make_archive("C:/Users/nicks/AppData/Roaming/com.modrinth.theseus/profiles/Plugin Testing/resourcepacks/CraftUi", 'zip', "pack")

with open("default.json", "w") as file:
    json.dump(default, file, indent=4)

with open("atlas.yml", "w") as file:
    yaml.dump(legend, file, default_flow_style=False)
    
with open("C:/Users/nicks/Documents/Minecraft-projects/CraftUI/CraftUi/src/main/resources/assets/atlas.yml", "w") as file:
    yaml.dump(legend, file, default_flow_style=True)


print(f"Done: {currentChar} characters")