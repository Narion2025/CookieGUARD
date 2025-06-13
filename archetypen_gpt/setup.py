#!/usr/bin/env python3
"""
Setup-Script für Archetypen-GPT System
Automatisiert die Installation und Konfiguration
"""

import os
import sys
import subprocess
from pathlib import Path
import json

def print_banner():
    """Zeigt das Banner an"""
    print("""
🧬 ============================================= 🧬
    ARCHETYPEN-GPT SYSTEM SETUP
🧬 ============================================= 🧬
""")

def check_python_version():
    """Überprüft die Python-Version"""
    print("🐍 Überprüfe Python-Version...")
    
    if sys.version_info < (3, 10):
        print("❌ Python 3.10+ erforderlich!")
        print(f"   Aktuelle Version: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} erkannt")
    return True

def install_dependencies():
    """Installiert die erforderlichen Dependencies"""
    print("\n📦 Installiere Dependencies...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "--upgrade", "pip"
        ])
        
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        
        print("✅ Dependencies erfolgreich installiert!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Fehler bei Installation: {e}")
        return False

def setup_environment():
    """Erstellt .env Datei"""
    print("\n🔑 Konfiguriere Umgebungsvariablen...")
    
    env_path = Path(".env")
    template_path = Path(".env.template")
    
    if env_path.exists():
        print("⚠️ .env Datei existiert bereits")
        response = input("Überschreiben? (y/N): ").lower().strip()
        if response != 'y':
            print("✅ Bestehende .env Datei beibehalten")
            return True
    
    # Template kopieren falls vorhanden
    if template_path.exists():
        with open(template_path, 'r') as f:
            template_content = f.read()
        
        with open(env_path, 'w') as f:
            f.write(template_content)
        
        print("✅ .env Datei aus Template erstellt")
    else:
        # Standard .env erstellen
        env_content = """# OpenAI API Konfiguration
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_ORG_ID=org-your-organization-id

# System Konfiguration
DEBUG=False
LOG_LEVEL=INFO

# Archetypen-GPT Einstellungen
MAX_TOKENS=4000
TEMPERATURE=0.7
MODEL_NAME=gpt-4-turbo-preview
EMBEDDING_MODEL=text-embedding-3-small
"""
        
        with open(env_path, 'w') as f:
            f.write(env_content)
        
        print("✅ Standard .env Datei erstellt")
    
    print("\n🔧 Bitte OpenAI API-Key in .env Datei eintragen!")
    print("   1. Öffne .env Datei")
    print("   2. Ersetze 'sk-your-api-key-here' mit deinem echten API-Key")
    
    return True

def create_directories():
    """Erstellt notwendige Verzeichnisse"""
    print("\n📁 Erstelle Verzeichnisse...")
    
    directories = [
        "answers",
        "profiles", 
        "prompts",
        "config",
        "embeddings",
        "questions",
        "tools",
        "assistant_setup"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ {directory}/")
    
    return True

def create_config_files():
    """Erstellt Standard-Konfigurationsdateien"""
    print("\n⚙️ Erstelle Konfigurationsdateien...")
    
    config_dir = Path("config")
    config_dir.mkdir(exist_ok=True)
    
    # OpenAI-Konfiguration
    openai_config = {
        "model": "gpt-4-turbo-preview",
        "temperature": 0.7,
        "max_tokens": 4000,
        "assistant_name_prefix": "Archetypen-GPT",
        "assistant_description": "Personalisierter Archetypen-GPT basierend auf psychodynamischer Analyse",
        "embedding_model": "text-embedding-3-small"
    }
    
    config_file = config_dir / "openai_keys.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(openai_config, f, indent=2, ensure_ascii=False)
    
    print("✅ OpenAI-Konfiguration erstellt")
    
    # Assistenten-Datenbank initialisieren
    assistants_db = {"assistants": {}}
    assistants_file = config_dir / "assistants.json"
    
    if not assistants_file.exists():
        with open(assistants_file, 'w', encoding='utf-8') as f:
            json.dump(assistants_db, f, indent=2, ensure_ascii=False)
        print("✅ Assistenten-Datenbank initialisiert")
    
    return True

def verify_installation():
    """Überprüft die Installation"""
    print("\n🔍 Überprüfe Installation...")
    
    # Wichtige Dateien prüfen
    required_files = [
        "main.py",
        "requirements.txt",
        ".env",
        "tools/ask_questions.py",
        "tools/profile_builder.py",
        "tools/prompt_generator.py",
        "tools/visual_map.py",
        "assistant_setup/create_assistant.py",
        "questions/archetypen.md",
        "questions/schatten.md",
        "questions/spiral_dynamics.md"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Fehlende Dateien:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    # Import-Test
    try:
        import openai
        import yaml
        import numpy as np
        import plotly
        import faiss
        print("✅ Alle Dependencies verfügbar")
    except ImportError as e:
        print(f"❌ Import-Fehler: {e}")
        return False
    
    print("✅ Installation erfolgreich verifiziert!")
    return True

def show_next_steps():
    """Zeigt die nächsten Schritte an"""
    print("""
🎉 SETUP ABGESCHLOSSEN!

📋 NÄCHSTE SCHRITTE:

1. 🔑 OpenAI API-Key konfigurieren:
   → Öffne .env Datei
   → Ersetze 'sk-your-api-key-here' mit deinem API-Key
   → Speichere die Datei

2. 🚀 System starten:
   → python main.py

3. 📝 Erstes Profil erstellen:
   → Option 1 im Menü wählen
   → Fragen beantworten
   → Profil analysieren lassen

4. 🤖 GPT-Assistant erstellen:
   → Option 3: Prompt generieren
   → Option 4: Assistant konfigurieren

5. 📊 Visualisierung anschauen:
   → Option 6: Profil visualisieren
   → HTML-Datei im Browser öffnen

💡 TIPPS:
- Erste Nutzung: ~25 Fragen beantworten (5-10 Min)
- API-Kosten: ~$0.50-2.00 pro Profil
- Profile werden lokal gespeichert
- System läuft vollständig offline (außer OpenAI-Calls)

🆘 BEI PROBLEMEN:
- README.md für Details lesen
- .env Datei prüfen
- Python-Version 3.10+ sicherstellen
- Internet-Verbindung für OpenAI API

🧬 Viel Erfolg mit deinem Archetypen-GPT System!
""")

def main():
    """Hauptfunktion des Setup-Scripts"""
    print_banner()
    
    if not check_python_version():
        sys.exit(1)
    
    if not install_dependencies():
        print("\n❌ Setup fehlgeschlagen bei Dependencies!")
        sys.exit(1)
    
    if not setup_environment():
        print("\n❌ Setup fehlgeschlagen bei Umgebungsvariablen!")
        sys.exit(1)
    
    if not create_directories():
        print("\n❌ Setup fehlgeschlagen bei Verzeichnissen!")
        sys.exit(1)
    
    if not create_config_files():
        print("\n❌ Setup fehlgeschlagen bei Konfiguration!")
        sys.exit(1)
    
    if not verify_installation():
        print("\n❌ Installation konnte nicht verifiziert werden!")
        sys.exit(1)
    
    show_next_steps()

if __name__ == "__main__":
    main() 