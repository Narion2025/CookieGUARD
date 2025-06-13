# CookieGUARD

Eine Browser-Erweiterung, die automatisch Cookie-Banner erkennt und diese basierend auf einer datenschutzfreundlichen Risikobewertung verwaltet.

## Features

- Automatische Risikobewertung von Cookie-Bannern
- Intelligente Verwaltung von Cookie-Einstellungen
- Detaillierte Analyse von Cookie-Verwendung
- Rechtliche Compliance-Prüfung (GDPR, ePrivacy, TTDSG)
- Mehrsprachige Unterstützung (aktuell Deutsch)

## Installation

1. Repository klonen:
```bash
git clone https://github.com/yourusername/CookieGUARD.git
cd CookieGUARD
```

2. Erweiterung in Chrome laden:
- Öffne Chrome und gehe zu `chrome://extensions/`
- Aktiviere den "Entwicklermodus"
- Klicke auf "Entpackte Erweiterung laden"
- Wähle den `extension`-Ordner aus

## Crawler

Der CookieGUARD-Crawler analysiert Webseiten auf Cookie-Banner und deren Compliance mit Datenschutzrichtlinien.

### Installation des Crawlers

```bash
cd crawler
npm install
```

### Ausführung des Crawlers

1. URLs in `urls.txt` hinzufügen
2. Crawler starten:
```bash
./run.sh
```

### Crawler-Funktionen

- **Cookie-Banner-Analyse**
  - Erkennung von Banner-Selektoren
  - Analyse des Banner-Verhaltens
  - Identifikation von Interaktionsmöglichkeiten

- **Cookie-Analyse**
  - Kategorisierung von Cookies
  - Analyse von Cookie-Eigenschaften
  - Tracking von Cookie-Lebenszyklen

- **Rechtliche Compliance**
  - GDPR-Konformität
  - ePrivacy-Richtlinie
  - TTDSG-Anforderungen

- **Automatisierungsdaten**
  - Klick-Sequenzen
  - Timing-Informationen
  - Fehlerbehandlung

### Datenstruktur

Der Crawler speichert die Ergebnisse in `data/crawl-results.json`:

```json
{
  "domain.com": {
    "timestamp": "2024-03-21T12:00:00Z",
    "banner": {
      "selectors": {
        "container": ["#cookie-banner"],
        "accept": [".accept-button"],
        "reject": [".reject-button"],
        "settings": [".settings-button"]
      },
      "behavior": {
        "appearsOn": "load",
        "delay": 0,
        "reappears": false
      }
    },
    "cookies": {
      "essential": [...],
      "functional": [...],
      "analytics": [...],
      "marketing": [...]
    },
    "compliance": {
      "gdpr": {
        "required": true,
        "checks": {...},
        "violations": []
      },
      "eprivacy": {...},
      "ttdsg": {...}
    },
    "automation": {
      "sequences": {...},
      "timing": {...},
      "errorHandling": {...}
    }
  }
}
```

### Rechtliche Anforderungen

#### GDPR
- Einwilligung muss aktiv gegeben werden
- Ablehnung muss gleichwertig möglich sein
- Detaillierte Informationen über Cookie-Zweck
- Speicherdauer muss angegeben werden
- Drittanbieter müssen genannt werden
- Widerrufsmöglichkeit muss bestehen

#### ePrivacy
- Cookie-Informationen müssen bereitgestellt werden
- Tracking-Informationen müssen transparent sein
- Opt-Out-Möglichkeit muss vorhanden sein
- Speicherungsinformationen müssen bereitgestellt werden

#### TTDSG
- Deutsche Datenschutzinformationen
- Deutsche Einstellungsmöglichkeiten
- Deutsche Button-Beschriftungen
- Deutsche Datenschutzerklärung

## Projektstruktur

```
CookieGUARD/
├── extension/
│   ├── manifest.json
│   ├── content-script.js
│   ├── popup.js
│   └── styles/
├── crawler/
│   ├── crawler.js
│   ├── package.json
│   ├── urls.txt
│   └── data/
└── README.md
```

## Abhängigkeiten

- Chrome Extension API
- Puppeteer (Crawler)
- Node.js (Crawler)

## Mitwirken

1. Fork erstellen
2. Feature-Branch erstellen (`git checkout -b feature/AmazingFeature`)
3. Änderungen committen (`git commit -m 'Add some AmazingFeature'`)
4. Branch pushen (`git push origin feature/AmazingFeature`)
5. Pull Request erstellen

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe [LICENSE](LICENSE) für Details. 