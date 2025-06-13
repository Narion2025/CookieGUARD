# 🔥 Bilder-Integration für den Archetypen-Schmied

## 📁 Bilder-Setup

### 1. Bilder-Ordner erstellen
```bash
mkdir archetypen_voice_web/images
```

### 2. Bilder hinzufügen
Kopiere die drei Bilder in den `images/` Ordner:
- `schmied-bei-arbeit.jpg` - Hauptbild für Hero-Section
- `feuer-flammen.jpg` - Hintergrund und Übergänge  
- `drei-gesichter.jpg` - Ergebnisseite

## 🎨 CSS-Integration (bereits implementiert)

### Hintergrund-Effekte:
- **Body**: Feuer-Flammen als Basis-Hintergrund
- **Welcome-Card**: Schmied-bei-Arbeit als Hero-Bild
- **Results-Container**: Drei-Gesichter für Archetypen-Darstellung

### Mystische Animationen:
- **fireGlow**: Pulsierender Feuer-Effekt für Avatar
- **firePulse**: Leuchtende Ringe um Elemente
- **fireTransition**: Sanfte Übergänge mit Feuer-Overlay
- **archetypeReveal**: 3D-Rotation für Ergebnisse
- **schmiedGlow**: Intensiver Glüh-Effekt

## 🔧 JavaScript-Effekte (bereits implementiert)

### Automatische Animationen:
```javascript
// Bei Ergebnisanzeige:
resultsContainer.classList.add('archetypen-reveal');    // Sofort
resultsContainer.classList.add('fire-transition');      // Nach 1s
resultsContainer.classList.add('schmied-glow');         // Nach 2.5s
```

## 🌟 Visuelle Atmosphäre

### Farbschema:
- **Primär**: `#ff8c00` (Orange/Gold)
- **Sekundär**: `#ff4500` (Feuer-Rot)
- **Akzent**: `#8b4513` (Braun/Erde)
- **Schatten**: `rgba(0,0,0,0.8)` (Tiefes Schwarz)

### Effekte:
- **Glühen**: Warme Orange-Töne
- **Schatten**: Dramatische Kontraste
- **Übergänge**: Sanfte Feuer-Animationen
- **Text**: Leuchtende Schrift mit Schatten

## 🚀 Deployment

### Vercel-Upload:
1. Bilder in `images/` Ordner kopieren
2. CSS und JS sind bereits angepasst
3. `vercel --prod` ausführen

### Lokaler Test:
```bash
cd archetypen_voice_web
python -m http.server 8000
# Öffne: http://localhost:8000
```

## 🎭 Mystische Elemente

### Schmied-Metaphorik:
- Feuer als Transformationskraft
- Hammer-Symbol (⚒️) in Navigation
- Glühende Metall-Effekte
- Funken-Animationen

### Archetypen-Symbolik:
- Drei Gesichter = Bewusstsein/Unbewusstes/Integration
- Goldener Riss = Erwachen/Erkenntnis
- Feuer = Transformation/Läuterung
- Schatten = Tiefe/Mysterium

Die Bilder verstärken die mystische Atmosphäre des Archetypen-Schmieds und schaffen eine immersive Erfahrung für die Nutzer! 🔥⚒️✨ 