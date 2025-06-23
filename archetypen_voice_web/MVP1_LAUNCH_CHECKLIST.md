# 🚀 Archetypen-Schmied MVP1 - Launch Checklist

## 📋 Pre-Launch Checklist

### ✅ Code & Assets
- [ ] `index_mvp1_enhanced.html` - Hauptdatei vorhanden
- [ ] `index_mvp1.html` - Simple Version als Fallback
- [ ] `SChmiedAmFeuer.mp4` - Feuer-Video vorhanden
- [ ] `package_mvp1.json` → `package.json` umbenennen
- [ ] `server_mvp1.js` - Server-Datei bereit
- [ ] `.env` Datei erstellt (basierend auf `.env.example`)

### ✅ ElevenLabs Integration
- [ ] Agent ID verifiziert: `agent_01jxn7kxjpfvt87rphxdnq1ddj`
- [ ] Widget in verschiedenen Browsern getestet
- [ ] Fallback-Link funktioniert
- [ ] Voice-Bot antwortet auf Deutsch

### ✅ Design & UX
- [ ] Feuer-Video lädt und looped korrekt
- [ ] Interaktive Maus-Effekte funktionieren
- [ ] Mobile Responsive getestet (iOS & Android)
- [ ] Ladezeiten < 3 Sekunden
- [ ] Alle Animationen flüssig

### ✅ Browser Testing
- [ ] Chrome/Edge - Vollständig getestet
- [ ] Firefox - Vollständig getestet
- [ ] Safari - Vollständig getestet
- [ ] Mobile Chrome - Getestet
- [ ] Mobile Safari - Getestet

## 🌐 Deployment Options

### Option 1: Vercel (Empfohlen für MVP)
```bash
# 1. Vercel CLI installieren
npm i -g vercel

# 2. Im Projektordner
cd archetypen_voice_web

# 3. Deploy
vercel

# 4. Folge den Prompts:
# - Setup and deploy? Y
# - Which scope? (Wähle deinen Account)
# - Link to existing project? N
# - Project name? archetypen-schmied-mvp1
# - Directory? ./
# - Override settings? N

# 5. Production Deploy
vercel --prod
```

### Option 2: Netlify
```bash
# 1. Build Command: (leer lassen - static site)
# 2. Publish Directory: .
# 3. Environment Variables: Keine benötigt für MVP1
```

### Option 3: GitHub Pages
```bash
# 1. Erstelle gh-pages Branch
git checkout -b gh-pages

# 2. Rename index_mvp1_enhanced.html zu index.html
mv index_mvp1_enhanced.html index.html

# 3. Push
git add .
git commit -m "MVP1 for GitHub Pages"
git push origin gh-pages

# 4. Aktiviere GitHub Pages in Settings
```

## 📊 Launch Day Tasks

### Vor dem Launch (T-1 Tag)
- [ ] Finale Tests in allen Browsern
- [ ] Performance-Check (Lighthouse)
- [ ] SSL-Zertifikat verifiziert
- [ ] Analytics-Code eingebaut (optional)
- [ ] Backup aller Dateien erstellt

### Launch Day (T-0)
1. **09:00** - Deployment auf Production
2. **09:30** - Smoke Tests durchführen
3. **10:00** - DNS propagation prüfen
4. **10:30** - Erste User-Tests mit Team
5. **11:00** - Social Media Ankündigung vorbereiten
6. **12:00** - **🚀 SOFT LAUNCH**

### Post-Launch (T+1)
- [ ] Analytics prüfen
- [ ] Error-Logs checken
- [ ] User-Feedback sammeln
- [ ] Performance monitoren
- [ ] Erste Iterationen planen

## 🎯 Success Criteria

### Technical KPIs
- **Uptime**: > 99.9%
- **Page Load**: < 3s (Desktop), < 5s (Mobile)
- **Widget Load**: < 5s
- **Error Rate**: < 0.1%

### User KPIs
- **Bounce Rate**: < 40%
- **Widget Interaction**: > 60%
- **Avg. Session**: > 3 Minuten
- **44 Fragen Completion**: > 30%

## 🔥 Quick Fixes

### Problem: ElevenLabs Widget lädt nicht
```javascript
// In index_mvp1_enhanced.html hinzufügen:
window.addEventListener('error', (e) => {
    if (e.target.tagName === 'ELEVENLABS-CONVAI') {
        console.warn('Widget failed, showing fallback');
        // Show fallback button
    }
});
```

### Problem: Video lädt nicht
```html
<!-- Fallback Image hinzufügen -->
<video class="fire-video" autoplay muted loop playsinline 
       poster="fire-fallback.jpg">
    <source src="SChmiedAmFeuer.mp4" type="video/mp4">
</video>
```

### Problem: Langsame Performance
```javascript
// Partikel reduzieren
setInterval(createParticle, 500); // statt 200
```

## 📞 Support Kontakte

### Hosting Support
- **Vercel**: status.vercel.com
- **Netlify**: status.netlify.com
- **Render**: status.render.com

### API Support
- **ElevenLabs**: support@elevenlabs.io

## ✨ Launch-Mantra

> "Mit diesem MVP überschreiten wir die Schwelle vom Konzept zur Realität. Der Archetypen-Schmied erwacht zum Leben, bereit, die ersten Seelen zu transformieren."

---

**Bereit für den Launch? Die Schmiede wartet auf ihre ersten Besucher! 🔥**

*Letzte Aktualisierung: [Datum einfügen]*
