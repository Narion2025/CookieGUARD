# Multi-AI Desktop

Eine lokale Desktop-Anwendung für die gleichzeitige Nutzung mehrerer KI-Agenten (GPT, Claude, Gemini, etc.) in einem gemeinsamen Chat-Interface.

## 🚀 Features

- **Multi-Agent-Chat**: Mehrere KI-Modelle können gleichzeitig auf deine Fragen antworten
- **Lokale Desktop-App**: Läuft komplett offline auf deinem Computer
- **Projekt-Management**: Organisiere deine Chats in Projekten
- **Agent-Verwaltung**: Einfaches Hinzufügen und Konfigurieren von KI-Agenten
- **Export-Funktionen**: Exportiere Konversationen als Markdown oder JSON
- **Dark/Light Theme**: Anpassbare Benutzeroberfläche
- **Cursor Cloud Integration**: Nutze bestehende Cursor-Sessions

## 📋 Voraussetzungen

- Node.js 18+ 
- npm oder yarn
- API-Schlüssel für die gewünschten KI-Dienste:
  - OpenAI API Key (für GPT-Modelle)
  - Anthropic API Key (für Claude)
  - Google AI API Key (für Gemini)
  - Cursor Session Token (optional)

## 🛠️ Installation

1. Repository klonen:
```bash
git clone https://github.com/yourusername/multi-ai-desktop.git
cd multi-ai-desktop
```

2. Abhängigkeiten installieren:
```bash
npm install
```

3. App starten:
```bash
npm start
```

## 🔧 Konfiguration

### Agenten hinzufügen

1. Klicke auf "Agenten verwalten" in der Sidebar
2. Wähle den Agent-Typ (OpenAI, Anthropic, Google, Cursor)
3. Gib deinen API-Schlüssel ein
4. Wähle das gewünschte Modell
5. Optional: Füge einen System-Prompt hinzu

### Projekte erstellen

- Klicke auf "Neues Projekt" oder nutze `Cmd/Ctrl + N`
- Projekte werden automatisch alle 5 Minuten gespeichert
- Manuelle Speicherung mit `Cmd/Ctrl + S`

## 🎮 Verwendung

1. **Agent auswählen**: Wähle die Agenten aus, die auf deine Frage antworten sollen
2. **Frage stellen**: Tippe deine Frage ein und drücke Enter
3. **Antworten vergleichen**: Alle ausgewählten Agenten antworten nacheinander
4. **Exportieren**: Exportiere interessante Konversationen als Markdown

## ⌨️ Tastenkürzel

- `Cmd/Ctrl + N`: Neues Projekt
- `Cmd/Ctrl + S`: Projekt speichern
- `Cmd/Ctrl + Shift + A`: Agent hinzufügen
- `Cmd/Ctrl + ,`: Einstellungen öffnen
- `Enter`: Nachricht senden
- `Shift + Enter`: Neue Zeile in Nachricht

## 🏗️ Architektur

```
multi-ai-desktop/
├── src/
│   ├── main/           # Electron Main Process
│   │   ├── main.js     # Hauptprozess
│   │   └── preload.js  # Preload Script
│   ├── renderer/       # Frontend
│   │   ├── index.html  # Haupt-HTML
│   │   ├── styles/     # CSS-Dateien
│   │   ├── components/ # UI-Komponenten
│   │   └── utils/      # Hilfsfunktionen
│   ├── services/       # Business Logic
│   │   ├── agentRegistry.js
│   │   └── chatOrchestrator.js
│   └── adapters/       # KI-Service-Adapter
│       ├── openaiAdapter.js
│       ├── anthropicAdapter.js
│       ├── googleAdapter.js
│       └── cursorAdapter.js
```

## 🔐 Sicherheit

- API-Schlüssel werden lokal verschlüsselt gespeichert
- Keine Daten werden an externe Server gesendet (außer an die KI-APIs)
- Alle Chats und Projekte bleiben auf deinem Computer

## 🐛 Bekannte Probleme

- Cursor Cloud Integration ist noch experimentell
- Streaming-Antworten noch nicht implementiert
- Regenerierung von Antworten in Entwicklung

## 🤝 Beitragen

Pull Requests sind willkommen! Für größere Änderungen bitte erst ein Issue erstellen.

## 📄 Lizenz

MIT License - siehe [LICENSE](LICENSE) Datei

## 🚧 Roadmap

### Version 0.2.0
- [ ] Streaming-Antworten
- [ ] Workflow-Engine für Agent-Ketten
- [ ] Bessere Fehlerbehandlung
- [ ] Toast-Benachrichtigungen

### Version 0.3.0
- [ ] Plugin-System für neue Agenten
- [ ] Vektor-Datenbank für Konversations-Memory
- [ ] Meta-Agent für automatische Optimierung
- [ ] Cloud-Sync (optional)

## 💡 Tipps

- Nutze verschiedene Modelle für unterschiedliche Aufgaben
- Claude ist gut für kreative Aufgaben
- GPT-4 für komplexe Reasoning-Aufgaben
- Gemini für multimodale Aufgaben (wenn implementiert)
- Kombiniere mehrere Agenten für beste Ergebnisse

---

Built with ❤️ using Electron, Node.js, and multiple AI APIs
