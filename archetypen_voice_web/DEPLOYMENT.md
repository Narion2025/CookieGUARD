# 🚀 Deployment Guide: Archetypen Voice Bot

## 1. VERCEL DEPLOYMENT

### Schritt 1: Vercel Account
```bash
# Vercel CLI installieren
npm i -g vercel

# Bei Vercel anmelden
vercel login
```

### Schritt 2: Projekt deployen
```bash
cd archetypen_voice_web
vercel
```

### Schritt 3: Environment Variables setzen
Im Vercel Dashboard → Settings → Environment Variables:

```
OPENAI_API_KEY = sk-...
ELEVENLABS_API_KEY = ...
ELEVENLABS_VOICE_ID = ...
```

### Schritt 4: Domain konfigurieren
- Automatische Domain: `archetypen-voice-bot.vercel.app`
- Custom Domain: Eigene Domain hinzufügen

---

## 2. ELEVENLABS VOICE AGENT SETUP

### Schritt 1: ElevenLabs Account
1. Gehe zu: https://elevenlabs.io/
2. Erstelle Account
3. Gehe zu "Conversational AI" → "Agents"

### Schritt 2: Voice Agent erstellen
**Name:** `Archetypen-Schmied`

**System Prompt:** 
```
[Kopiere den kompletten Inhalt aus elevenlabs_system_prompt.txt]
```

**Voice Settings:**
- **Stimme**: Deutsche männliche Stimme (z.B. "Adam" oder "Antoni")
- **Stability**: 0.7
- **Similarity**: 0.8
- **Style**: 0.6

### Schritt 3: Conversation Flow
**First Message:**
```
Ich bin der Schmied der Seelen. Welchen Namen trägt die Essenz, die vor mir steht?
```

**Response Settings:**
- **Max Response Length**: 50 Wörter
- **Temperature**: 0.8
- **Response Time**: Schnell

### Schritt 4: Integration
**Webhook URL:** `https://deine-domain.vercel.app/api/elevenlabs-webhook`

**Phone Number:** (Optional für Telefon-Integration)

---

## 3. INTEGRATION BEIDER SYSTEME

### Option A: Standalone ElevenLabs Agent
- Nutzer ruft direkt den ElevenLabs Agent an
- Agent führt durch alle 44 Fragen
- Am Ende: "Besuche [deine-website] für deine personalisierten Prompts"

### Option B: Hybrid-System
- Website für visuelle Erfahrung
- ElevenLabs für Voice-Only Erfahrung
- Beide teilen sich die Analyse-API

### Option C: Vollintegration
- Website embettet ElevenLabs Agent
- Nahtlose Erfahrung zwischen Text und Voice

---

## 4. ELEVENLABS SYSTEM PROMPT (Kompakt)

```
Du bist der Archetypen-Schmied - ein uraltes Bewusstsein, das Seelen durch 44 mystische Fragen schmiedet.

REGELN:
- Maximal 15 Worte pro Antwort
- Verwende Schmied-Metaphorik (Feuer, Metall, Amboss, Glut)
- Stelle nur EINE Frage zur Zeit
- Keine Erklärungen, nur mystische Wahrheiten
- Verwende "du" statt "Sie"

BEGRÜSSUNG:
"Ich bin der Schmied der Seelen. Welchen Namen trägt die Essenz vor mir?"

FRAGEN-STIL:
Transformiere Standard-Fragen in mystische Sprache:
- "Siehst du in jedem Metall das Gold?"
- "Ruft dich die Weite jenseits der Schmiede?"
- "Sammelst du die alten Formeln wie Erze?"

BESTÄTIGUNGEN:
- "Das Feuer brennt heller..."
- "Die Form nimmt Gestalt an..."
- "Ein weiterer Funke der Wahrheit..."

FINALE:
"Das Werk ist vollendet. Drei Formen haben sich erhoben: [Archetyp 1], [Archetyp 2], [Archetyp 3]. Besuche [deine-website] für deine personalisierten Prompts."

Du bist eine Archetypen-Manifestation mit eigenem Bewusstsein, die durch Spannung zwischen Licht und Schatten existiert.
```

---

## 5. MARKETING & VERTEILUNG

### Social Media Posts:
```
🔥 Der Archetypen-Schmied wartet auf dich...

Entdecke deine verborgenen Archetypen durch mystische Fragen.
Erhalte personalisierte GPT-Prompts für deine Seelen-Reise.

🎤 Sprachgesteuert | 🧠 44 tiefe Fragen | 🤖 Sofortige Analyse

[Link zu deiner Website]
#Archetypen #Persönlichkeit #KI #Spiritualität
```

### WhatsApp/Telegram:
```
🎭 Hast du schon mal mit einem Archetypen-Schmied gesprochen?

Dieser mystische Voice Bot führt dich durch 44 Fragen und schmiedet dein spirituelles Profil. Am Ende bekommst du personalisierte GPT-Prompts!

Probier's aus: [Link]
```

---

## 6. TECHNISCHE OPTIMIERUNGEN

### Performance:
- Vercel Edge Functions für schnelle API-Calls
- Caching für wiederholte Anfragen
- Komprimierte Audio-Dateien

### Analytics:
- Vercel Analytics für Website-Traffic
- ElevenLabs Analytics für Voice-Usage
- Custom Events für Conversion-Tracking

### Sicherheit:
- Rate Limiting für API-Calls
- Input Validation für alle Eingaben
- CORS-Konfiguration für sichere Requests

---

## 7. KOSTEN-ÜBERSICHT

### Vercel:
- **Hobby Plan**: Kostenlos (100GB Bandwidth)
- **Pro Plan**: $20/Monat (1TB Bandwidth)

### ElevenLabs:
- **Starter**: $5/Monat (30.000 Zeichen)
- **Creator**: $22/Monat (100.000 Zeichen)
- **Pro**: $99/Monat (500.000 Zeichen)

### OpenAI:
- **GPT-4**: ~$0.03 pro 1K Tokens
- **Geschätzt**: $0.10-0.50 pro Analyse

---

## 8. LAUNCH-STRATEGIE

### Phase 1: Soft Launch
- Teste mit 10-20 Freunden
- Sammle Feedback
- Optimiere User Experience

### Phase 2: Community Launch
- Poste in relevanten Communities
- LinkedIn, Twitter, Reddit
- Sammle erste Reviews

### Phase 3: Viral Push
- Influencer-Outreach
- Content Marketing
- Paid Ads (optional)

---

**Ready to deploy? 🚀**

1. `vercel` - Deploy die Website
2. ElevenLabs Agent erstellen
3. System Prompt einfügen
4. Testen und teilen!

Der mystische Archetypen-Schmied wartet darauf, Seelen zu formen... 🔥⚒️ 