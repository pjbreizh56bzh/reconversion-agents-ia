#!/bin/bash
# $1 = fichier .svg/.html source, $2 = png de sortie (2100x2970, sans bandeau du navigateur)
C=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
$C --headless --no-sandbox --hide-scrollbars --screenshot=/tmp/_full.png --window-size=2100,3200 file://$PWD/$1 >/dev/null 2>&1
python3 -c "from PIL import Image;Image.open('/tmp/_full.png').crop((0,0,2100,2970)).save('$2')"
