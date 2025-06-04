# Cookie Guardian - Terminal Setup (OPTIONAL)

# ======================
# OPTION 1: DIREKT VERWENDEN (EMPFOHLEN)
# ======================
# Keine Terminal-Befehle nötig!
# Einfach die 7 Dateien in einen Ordner kopieren und als Extension laden

# ======================
# OPTION 2: PROFESSIONAL DEVELOPMENT SETUP
# ======================

# 1. Projekt-Ordner erstellen
mkdir cookie-guardian
cd cookie-guardian

# 2. Node.js Projekt initialisieren (für Linting/Testing)
npm init -y

# 3. Development Dependencies installieren
npm install --save-dev \
  eslint \
  eslint-config-standard \
  eslint-plugin-import \
  eslint-plugin-node \
  eslint-plugin-promise \
  prettier \
  web-ext \
  chrome-types

# 4. ESLint Konfiguration erstellen
echo '{
  "extends": ["standard"],
  "env": {
    "browser": true,
    "webextensions": true
  },
  "globals": {
    "chrome": "readonly"
  }
}' > .eslintrc.json

# 5. Prettier Konfiguration
echo '{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5"
}' > .prettierrc

# 6. Package.json Scripts hinzufügen
npm pkg set scripts.lint="eslint *.js"
npm pkg set scripts.format="prettier --write *.js *.css *.html"
npm pkg set scripts.build="web-ext build"
npm pkg set scripts.start="web-ext run --target=chromium"

# ======================
# OPTION 3: ICON GENERIERUNG
# ======================

# ImageMagick installieren (für Icon-Generierung)
# Ubuntu/Debian:
sudo apt-get install imagemagick

# macOS (mit Homebrew):
brew install imagemagick

# Icons aus einem SVG generieren (falls Sie eine SVG-Datei haben)
# convert shield.svg -resize 16x16 icons/icon-16.png
# convert shield.svg -resize 32x32 icons/icon-32.png
# convert shield.svg -resize 48x48 icons/icon-48.png
# convert shield.svg -resize 128x128 icons/icon-128.png

# ======================
# OPTION 4: GIT REPOSITORY
# ======================

# Git Repository initialisieren
git init

# .gitignore erstellen
echo 'node_modules/
*.log
.DS_Store
web-ext-artifacts/
.vscode/
*.zip' > .gitignore

# Erste Commits
git add .
git commit -m "Initial Cookie Guardian Extension"

# ======================
# OPTION 5: SCHNELL-SETUP (Copy-Paste alle Befehle)
# ======================

# Alles in einem Befehl (für Ubuntu/Debian):
mkdir cookie-guardian && cd cookie-guardian && \
npm init -y && \
npm install --save-dev eslint prettier web-ext chrome-types && \
mkdir icons && \
echo "Chrome Extension bereit! Kopieren Sie jetzt die 7 Dateien hierhin."

# ======================
# VERWENDUNG DER DEVELOPMENT TOOLS
# ======================

# Code prüfen:
# npm run lint

# Code formatieren:
# npm run format

# Extension testen:
# npm run start

# Extension packen:
# npm run build