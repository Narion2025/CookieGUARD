# Cookie Guardian - Installation und Setup

## 📁 Ordnerstruktur erstellen

1. Erstellen Sie einen neuen Ordner namens `cookie-guardian`
2. Laden Sie alle 7 Dateien herunter und speichern Sie sie in diesem Ordner:
   - `manifest.json`
   - `background.js`
   - `content-script.js`
   - `guardian-overlay.css`
   - `popup.html`
   - `popup.js`
   - `popup.css`

3. Erstellen Sie einen Unterordner `icons` im `cookie-guardian` Ordner

## 🎨 Icons erstellen (Optional)

Sie benötigen 4 Icon-Dateien in verschiedenen Größen:
- `icon-16.png` (16x16 Pixel)
- `icon-32.png` (32x32 Pixel)
- `icon-48.png` (48x48 Pixel)
- `icon-128.png` (128x128 Pixel)

**Einfacher Weg:** Verwenden Sie ein kostenloses Tool wie [Favicon.io](https://favicon.io/) oder erstellen Sie ein einfaches Shield-Icon (🛡️) in einem Bildbearbeitungsprogramm.

## 🚀 Chrome Extension installieren

1. **Chrome öffnen** und zu `chrome://extensions/` navigieren
2. **Entwicklermodus aktivieren** (Schalter oben rechts)
3. **"Entpackte Erweiterung laden"** klicken
4. **Ihren `cookie-guardian` Ordner auswählen**
5. Die Extension sollte nun installiert und aktiv sein!

## ✅ Funktionstest

1. **Website besuchen**: Gehen Sie zu einer deutschen Website mit Cookie-Banner (z.B. spiegel.de)
2. **Guardian Popup**: Sollte über dem Cookie-Banner erscheinen
3. **Auswahl treffen**: Wählen Sie eine der drei Optionen
4. **Wiederholter Besuch**: Bei erneutem Besuch sollte kein Popup mehr erscheinen

## 🔧 Troubleshooting

**Extension funktioniert nicht:**
- Prüfen Sie, ob alle 7 Dateien im richtigen Ordner sind
- Schauen Sie in die Chrome Entwicklerkonsole (F12) nach Fehlermeldungen
- Vergewissern Sie sich, dass der Entwicklermodus aktiviert ist

**Icons fehlen:**
- Extension funktioniert auch ohne Icons
- Sie können temporär beliebige kleine PNG-Dateien verwenden

**Cookie-Banner wird nicht erkannt:**
- Öffnen Sie die Entwicklerkonsole (F12)
- Schauen Sie nach "Cookie Guardian" Meldungen
- Manche Websites verwenden noch unbekannte Banner-Systeme

## 📱 Ampel-System verstehen

**🔴 Rot (Hohes Risiko):**
- Marketing-Cookies und Tracking für Werbung
- Datenverkauf an Drittanbieter
- Personalisierung und Profiling

**🟡 Gelb (Mittleres Risiko):**
- Analyse und Statistik-Cookies
- Performance-Tracking
- Allgemeine Datensammlung

**🟢 Grün (Geringes Risiko):**
- Nur funktionale Cookies
- Technisch notwendige Cookies
- Transparente Datenverwendung

## 🎯 Nächste Schritte

1. **Testen** Sie die Extension auf verschiedenen deutschen Websites
2. **Sammeln** Sie Erfahrungen mit dem Ampel-System
3. **Erweitern** Sie bei Bedarf die Banner-Erkennung
4. **Feedback** sammeln von anderen Nutzern

Die Extension ist nun bereit für den Einsatz! Sie wird automatisch Cookie-Banner erkennen und Ihre Einstellungen dauerhaft speichern.