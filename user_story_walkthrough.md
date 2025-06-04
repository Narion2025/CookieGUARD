# User Story Walkthrough - Cookie Guardian

## 🎬 Szenario: Erster Besuch auf einer neuen Website

### Schritt 1: User öffnet Website
**User-Aktion:** 
- User navigiert zu `https://spiegel.de` zum ersten Mal

**System-Reaktion:**
- `content-script.js` wird automatisch geladen
- Extension prüft in der lokalen Speicherung: Gibt es bereits Einstellungen für `spiegel.de`?
- **Ergebnis:** Keine Einstellungen gefunden → Erste-Besuch-Modus

**User-Erfahrung:**
- User sieht normale Website-Ladevorgang
- Noch kein Cookie Guardian Interface sichtbar

---

### Schritt 2: Cookie-Banner wird erkannt
**System-Reaktion:**
```javascript
// Banner-Erkennung läuft automatisch
detectBanners() {
  // Sucht nach OneTrust, Cookiebot, etc.
  const banner = document.querySelector('#onetrust-consent-sdk');
  if (banner && isVisible(banner)) {
    handleBannerDetected(banner);
  }
}
```

**Was passiert:**
- Extension scannt nach bekannten Cookie-Banner Selektoren
- Banner von Spiegel.de wird gefunden (z.B. OneTrust-System)
- Risiko-Analyse startet automatisch basierend auf Banner-Inhalt

**User-Erfahrung:**
- User sieht den ursprünglichen Cookie-Banner kurz aufblitzen
- Noch keine Interaktion erforderlich

---

### Schritt 3: Ampel-System analysiert Risiko
**System-Reaktion:**
```javascript
assessRiskLevel(banner) {
  const text = banner.textContent.toLowerCase();
  // "marketing", "werbung", "personalisierung" gefunden
  riskScore += 3; 
  // Ergebnis: Risiko-Level "red"
  return 'red';
}
```

**Analyse-Ergebnis für Spiegel.de:**
- **Gefunden:** "Marketing-Cookies", "Werbepartner", "Personalisierung"
- **Bewertung:** 🔴 ROT (Hohes Datenschutz-Risiko)
- **Grund:** Datenverkauf an Drittanbieter für Werbezwecke

**User-Erfahrung:**
- Immer noch kein visuelles Feedback
- Analyse läuft in <100ms ab

---

### Schritt 4: Cookie Guardian Popup erscheint
**System-Reaktion:**
- Original Cookie-Banner wird überlagert (nicht entfernt)
- Cookie Guardian Popup erscheint mit höchstem z-index
- Popup zeigt rote Ampel und Risiko-Erklärung

**User-Erfahrung:**
```
┌─────────────────────────────────┐
│  🛡️ Cookie Guardian             │
│                                 │
│  🔴 Hohes Datenschutz-Risiko    │
│                                 │
│  Cookie-Banner erkannt auf      │
│  spiegel.de                     │
│                                 │
│  Diese Website verwendet        │
│  wahrscheinlich Marketing-      │
│  Cookies und Tracking-          │
│  Technologien für Werbezwecke.  │
│                                 │
│  🔴 Dauerhaft blockieren        │
│  🟡 Nur notwendige Cookies      │
│  🟢 Alle akzeptieren            │
│                                 │
│  Diese Einstellung wird für     │
│  spiegel.de gespeichert         │
└─────────────────────────────────┘
```

---

### Schritt 5: User trifft Entscheidung
**User-Aktion:** 
- User klickt auf "🔴 Dauerhaft blockieren"

**System-Reaktion:**
```javascript
handleUserChoice('block') {
  // 1. Speichere Einstellung lokal
  await saveDomainSetting('block');
  
  // 2. Wende Einstellung sofort an
  applyBannerAction('block');
  
  // 3. Aktualisiere Badge
  updateBadge('block');
}
```

**Was passiert:**
1. **Lokale Speicherung:** `{domain: 'spiegel.de', action: 'block', timestamp: Date.now()}`
2. **Banner-Manipulation:** System sucht "Alle ablehnen" Button und klickt ihn
3. **Badge-Update:** Extension-Icon zeigt 🛡️ Symbol
4. **Popup-Entfernung:** Cookie Guardian Popup verschwindet

**User-Erfahrung:**
- Popup verschwindet sofort
- Original Cookie-Banner verschwindet ebenfalls
- Extension-Icon zeigt roten Schutz-Status
- Website ist normal nutzbar

---

### Schritt 6: Bestätigung und Statistik-Update
**System-Reaktion:**
```javascript
updateStats('block') {
  stats.blocked++;
  stats.lastUpdated = Date.now();
  // Speichere in Chrome Storage
}
```

**User-Erfahrung:**
- Kurze Erfolgsmeldung (optional)
- Website funktioniert normal ohne Cookie-Belästigung
- Statistik im Extension-Popup wird aktualisiert

---

## 🔄 Szenario: Zweiter Besuch (Silent Mode)

### Schritt 1: User kehrt zurück
**User-Aktion:** 
- User besucht `https://spiegel.de` zwei Tage später

**System-Reaktion:**
```javascript
async init() {
  this.domainSetting = await getDomainSetting();
  // Gefunden: {action: 'block', timestamp: ...}
  
  if (this.domainSetting) {
    this.applySilentMode(); // KEIN Popup!
  }
}
```

**User-Erfahrung:**
- Website lädt normal
- **KEIN Cookie Guardian Popup**
- **KEIN Cookie-Banner** der Website
- Sofortiger Zugang zu Inhalten

---

### Schritt 2: Automatische Banner-Bearbeitung
**System-Reaktion:**
```javascript
applySilentMode() {
  setTimeout(() => {
    this.detectBanners();
    if (this.currentBanner) {
      this.applyBannerAction('block'); // Automatisch ablehnen
    }
  }, 1000);
}
```

**Was passiert:**
- System wartet auf Cookie-Banner Erscheinen
- Sobald Banner da ist: Automatisches Klicken auf "Alle ablehnen"
- Banner verschwindet ohne User-Interaktion

**User-Erfahrung:**
- Möglicherweise kurzes Aufblitzen des Cookie-Banners
- Automatisches Verschwinden ohne User-Aktion
- Normale Website-Nutzung ohne Unterbrechung

---

### Schritt 3: Status-Anzeige
**System-Reaktion:**
- Extension-Badge zeigt weiterhin 🛡️ Symbol
- Bei Klick auf Extension: Popup zeigt "Cookies werden blockiert seit [Datum]"

**User-Erfahrung:**
- User kann Status jederzeit einsehen
- Einstellungen bei Bedarf ändern
- Vollständige Transparenz über Automatisierung

---

## 🔧 Edge Cases und Fehlerbehandlung

### Banner nicht erkannt
**Problem:** Neue, unbekannte Cookie-Banner
**System-Reaktion:** Timeout nach 15 Sekunden → Default-Aktion "block"
**User-Erfahrung:** Popup erscheint mit Hinweis, dass Banner möglicherweise nicht vollständig automatisiert werden konnte

### Button nicht gefunden
**Problem:** "Alle ablehnen" Button hat unbekannten Text
**System-Reaktion:** Fallback auf "Einstellungen" → Fallback auf "Akzeptieren"
**User-Erfahrung:** Funktionalität bleibt erhalten, eventuell suboptimale Cookie-Einstellung

### Extension-Konflikt
**Problem:** Andere Cookie-Extension aktiv
**System-Reaktion:** Cookie Guardian hat höchste z-index Priorität
**User-Erfahrung:** Cookie Guardian "gewinnt" und funktioniert normal

---

## 📊 User Value Proposition

**Nach der ersten Woche:**
- ✅ 50+ Websites automatisch konfiguriert
- ✅ Null Cookie-Banner Unterbrechungen bei bekannten Sites
- ✅ Statistik zeigt gesparte Zeit und blockierte Tracker
- ✅ Stress-freies Browsen ohne Cookie-Popups

**Long-term Benefits:**
- 🎯 Personalisierte Datenschutz-Einstellungen pro Website
- 📈 Wachsende Kompatibilität durch Community-Updates  
- 🛡️ Transparente Kontrolle über Online-Privatsphäre
- ⚡ Schnelleres Web-Browsing ohne Popup-Unterbrechungen