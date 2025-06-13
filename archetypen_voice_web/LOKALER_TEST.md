# 🔥 Lokaler Test - Archetypen-Schmied

## 🎯 **WARUM HÖRST DU NICHTS?**

Das **ElevenLabs Widget** braucht **HTTPS** für Mikrofon-Zugriff!

---

## 🚀 **LÖSUNG 1: HTTPS Lokal (EMPFOHLEN)**

### **Mit Python HTTPS Server:**
```bash
cd archetypen_voice_web

# Erstelle SSL Zertifikat (einmalig)
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# Starte HTTPS Server
python3 -c "
import http.server, ssl, socketserver
httpd = socketserver.TCPServer(('localhost', 8443), http.server.SimpleHTTPRequestHandler)
httpd.socket = ssl.wrap_socket(httpd.socket, certfile='cert.pem', keyfile='key.pem', server_side=True)
print('HTTPS Server läuft auf: https://localhost:8443')
httpd.serve_forever()
"
```

### **Dann öffne:**
```
https://localhost:8443
```

---

## 🚀 **LÖSUNG 2: Netlify Deploy (EINFACHER)**

```bash
cd archetypen_voice_web
npx netlify deploy --prod --dir .
```

---

## 🚀 **LÖSUNG 3: Direkt ElevenLabs**

Falls das Widget nicht lädt, nutze den **direkten Link**:
```
https://elevenlabs.io/convai/agent_01jxn7kxjpfvt87rphxdnq1ddj
```

---

## 🔧 **TROUBLESHOOTING CHECKLIST:**

### **Browser-Einstellungen:**
- ✅ **Mikrofon-Berechtigung** erteilt?
- ✅ **Lautsprecher** nicht stumm?
- ✅ **HTTPS** verwendet (nicht HTTP)?
- ✅ **JavaScript** aktiviert?

### **ElevenLabs Widget:**
- ✅ **Agent-ID** korrekt: `agent_01jxn7kxjpfvt87rphxdnq1ddj`
- ✅ **Script** geladen: `@elevenlabs/convai-widget-embed`
- ✅ **Internet-Verbindung** stabil?

### **Audio-Test:**
1. **Klicke** auf das ElevenLabs Widget
2. **Erlaube** Mikrofon-Zugriff
3. **Sage** "Hallo" 
4. **Warte** auf Antwort vom Schmied

---

## 🎭 **ERWARTETES VERHALTEN:**

### **Erfolgreicher Dialog:**
```
Du: "Hallo"
Schmied: "Ich bin der Schmied der Seelen. Dein Name?"
Du: "Benjamin"
Schmied: "Benjamin... das Feuer kennt dich. Siehst du Gold in jedem Metall?"
```

### **Schmied-Charakteristika:**
- ✅ **Maximal 12 Worte** pro Antwort
- ✅ **Mystische Sprache** (Feuer, Metall, Glut)
- ✅ **44 transformierte Fragen**
- ✅ **Deutsche Stimme**

---

## 🔥 **QUICK FIX:**

**Falls gar nichts funktioniert:**
1. Öffne: https://elevenlabs.io/convai/agent_01jxn7kxjpfvt87rphxdnq1ddj
2. Teste den Agent direkt auf ElevenLabs
3. Nutze die schriftliche Analyse auf der Website

**Der Archetypen-Schmied wartet auf dich!** 🔥⚒️✨ 