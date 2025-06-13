# 🎭 Archetypen Voice Bot

Eine moderne Web-App für Jung'sche Archetypen-Analyse mit Sprachsteuerung und personalisierten GPT-Prompt-Generierung.

## ✨ Features

- **🎤 Sprachgesteuerte Analyse** - Beantworte Fragen per Sprache oder Text
- **🧠 44 psychologische Fragen** - Basierend auf Jung'schen Archetypen + Spiral Dynamics
- **🤖 ElevenLabs Voice Integration** - Natürliche deutsche Sprachausgabe
- **📊 Detaillierte Persönlichkeitsanalyse** - Top 3 Archetypen mit Scores
- **📝 Personalisierte GPT-Prompts** - Sofort einsatzbereit für ChatGPT
- **💾 Download-Funktionen** - Alle Ergebnisse als Dateien
- **📱 Responsive Design** - Funktioniert auf allen Geräten

## 🚀 Quick Start

### 1. Repository klonen
```bash
git clone <repository-url>
cd archetypen_voice_web
```

### 2. Dependencies installieren
```bash
npm install
```

### 3. Umgebungsvariablen konfigurieren
```bash
cp env.example .env
# Bearbeite .env mit deinen API-Keys
```

### 4. Server starten
```bash
npm start
# Oder für Development:
npm run dev
```

### 5. Browser öffnen
```
http://localhost:3000
```

## 🔧 Konfiguration

### API Keys benötigt:

#### OpenAI API Key
- Gehe zu: https://platform.openai.com/api-keys
- Erstelle einen neuen API Key
- Füge ihn in `.env` als `OPENAI_API_KEY` ein

#### ElevenLabs API Key
- Gehe zu: https://elevenlabs.io/
- Erstelle einen Account
- Gehe zu Profile → API Keys
- Füge den Key in `.env` als `ELEVENLABS_API_KEY` ein

#### ElevenLabs Voice ID
- Gehe zu: https://elevenlabs.io/voices
- Wähle eine deutsche Stimme (z.B. "Seraphina" oder "Freya")
- Kopiere die Voice ID
- Füge sie in `.env` als `ELEVENLABS_VOICE_ID` ein

## 🎯 Verwendung

### 1. **Willkommensbildschirm**
- Klicke "Analyse starten"

### 2. **Name eingeben**
- Sage oder tippe deinen Namen

### 3. **Fragebogen durchlaufen**
- 36 Jung'sche Archetypen-Fragen
- 8 Spiral Dynamics-Fragen
- Antworte mit 1-5 oder natürlicher Sprache

### 4. **Ergebnisse erhalten**
- Top 3 Archetypen mit Scores
- Spiral Dynamics Level
- Schattenmuster-Analyse
- Integrationsthema

### 5. **Dateien herunterladen**
- GPT System-Prompt
- Detaillierte Analyse
- DALL-E Bild-Prompt
- ChatGPT Konfiguration

## 📁 Projektstruktur

```
archetypen_voice_web/
├── index.html              # Haupt-HTML-Datei
├── styles.css              # CSS-Styling
├── script.js               # Frontend-JavaScript
├── backend/
│   └── server.js           # Express.js Server
├── package.json            # Node.js Dependencies
├── env.example             # Umgebungsvariablen-Vorlage
└── README.md              # Diese Datei
```

## 🔌 API Endpoints

### `GET /`
Hauptseite der Anwendung

### `POST /api/analyze`
Basis-Analyse der Antworten

### `POST /api/openai-analysis`
Erweiterte Analyse mit OpenAI GPT-4

### `POST /api/tts`
Text-to-Speech mit ElevenLabs

### `GET /api/health`
Server-Status prüfen

## 🎨 Anpassungen

### Neue Archetypen hinzufügen
1. Erweitere das `QUESTIONS` Array in `script.js`
2. Füge Beschreibungen in `getArchetypeDescription()` hinzu
3. Erweitere die Bild-Prompts in `generateImagePrompt()`

### Andere Sprachen
1. Ändere `lang` in der Speech Recognition
2. Übersetze die Fragen im `QUESTIONS` Array
3. Passe die ElevenLabs Voice ID an

### Styling anpassen
- Bearbeite `styles.css`
- Ändere Farben in den CSS-Variablen
- Passe Animationen an

## 🚀 Deployment

### Lokaler Server
```bash
npm start
```

### Heroku
```bash
# Heroku CLI installieren
heroku create archetypen-voice-bot
heroku config:set OPENAI_API_KEY=your-key
heroku config:set ELEVENLABS_API_KEY=your-key
heroku config:set ELEVENLABS_VOICE_ID=your-voice-id
git push heroku main
```

### Vercel
```bash
# Vercel CLI installieren
vercel
# Umgebungsvariablen in Vercel Dashboard konfigurieren
```

### Netlify
```bash
# Netlify CLI installieren
netlify deploy
# Umgebungsvariablen in Netlify Dashboard konfigurieren
```

## 🔒 Sicherheit

- API Keys niemals in den Code committen
- Verwende `.env` für sensible Daten
- Rate Limiting für API-Calls implementieren
- HTTPS in Produktion verwenden

## 🐛 Troubleshooting

### Spracherkennung funktioniert nicht
- Stelle sicher, dass HTTPS verwendet wird
- Erlaube Mikrofon-Zugriff im Browser
- Teste mit verschiedenen Browsern

### ElevenLabs API Fehler
- Prüfe API Key und Voice ID
- Stelle sicher, dass Credits verfügbar sind
- Teste mit dem Browser Speech Synthesis als Fallback

### OpenAI API Fehler
- Prüfe API Key
- Stelle sicher, dass Credits verfügbar sind
- Verwende die lokale Analyse als Fallback

## 📊 Psychologische Grundlagen

### Jung'sche Archetypen
- **12 Hauptarchetypen** nach C.G. Jung
- **Licht- und Schattenaspekte** jedes Archetyps
- **Persönlichkeitsentwicklung** durch Archetypen-Integration

### Spiral Dynamics
- **8 Bewusstseinsstufen** nach Clare Graves
- **Entwicklungspsychologie** und Werteebenen
- **Integration** verschiedener Entwicklungsstufen

## 🤝 Beitragen

1. Fork das Repository
2. Erstelle einen Feature Branch
3. Committe deine Änderungen
4. Push zum Branch
5. Erstelle einen Pull Request

## 📄 Lizenz

MIT License - siehe LICENSE Datei

## 👨‍💻 Autor

**Benjamin Poersch**
- GitHub: [@Narion2025](https://github.com/Narion2025)

## 🙏 Danksagungen

- C.G. Jung für die Archetypen-Theorie
- Clare Graves für Spiral Dynamics
- OpenAI für GPT-4 Integration
- ElevenLabs für Voice Synthesis

---

**Viel Spaß beim Entdecken deiner Archetypen! 🎭✨** 