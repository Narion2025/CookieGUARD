#!/usr/bin/env python3
"""
Archetypen-GPT System - Hauptmodul
Erstellt personalisierte GPT-Assistenten basierend auf psychodynamischen Profilen
"""

import os
import json
import sys
from pathlib import Path
from typing import Dict, Any, Optional
import asyncio

# Lokale Imports
sys.path.append(str(Path(__file__).parent))
from tools.ask_questions import QuestionManager
from tools.profile_builder import ProfileBuilder  
from tools.prompt_generator import PromptGenerator
from tools.visual_map import VisualMapper
from assistant_setup.create_assistant import AssistantCreator
from assistant_setup.upload_profile import ProfileUploader
from assistant_setup.embed_vectors import VectorEmbedder

class ArchetypenGPT:
    """Hauptklasse für das Archetypen-GPT-System"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.answers_path = self.base_path / "answers"
        self.profiles_path = self.base_path / "profiles"
        self.prompts_path = self.base_path / "prompts"
        
        # Verzeichnisse erstellen
        for path in [self.answers_path, self.profiles_path, self.prompts_path]:
            path.mkdir(exist_ok=True)
            
        # Module initialisieren
        self.question_manager = QuestionManager()
        self.profile_builder = ProfileBuilder()
        self.prompt_generator = PromptGenerator()
        self.visual_mapper = VisualMapper()
        self.assistant_creator = AssistantCreator()
        self.profile_uploader = ProfileUploader()
        self.vector_embedder = VectorEmbedder()
    
    def show_menu(self):
        """Zeigt das Hauptmenü"""
        print("\n" + "="*60)
        print("🎭 ARCHETYPEN-GPT SYSTEM - ERWEITERTE VERSION")
        print("="*60)
        print("1. 📝 Neues Profil erstellen")
        print("2. 👁️  Profil anzeigen")
        print("3. 🎯 Standard-Prompt generieren")
        print("4. ⚡ Erweiterten Bewusstseins-Prompt generieren")
        print("5. 🖼️ Individuellen Image-Prompt generieren")
        print("6. 🎭 KOMPLETTES ARCHETYPEN-PAKET generieren")
        print("7. 🤖 OpenAI Assistant konfigurieren")
        print("8. 📊 Profil-Visualisierung erstellen")
        print("9. 🔍 Alle Profile anzeigen")
        print("10. 🧠 Bewusstseins-Matrix konfigurieren")
        print("0. ❌ Beenden")
        print("="*60)
    
    def handle_menu_choice(self, choice: str):
        """Verarbeitet Menüauswahl"""
        try:
            if choice == '1':
                self.create_new_profile()
            elif choice == '2':
                self.show_profile()
            elif choice == '3':
                self.generate_standard_prompt()
            elif choice == '4':
                self.generate_advanced_prompt()
            elif choice == '5':
                self.generate_image_prompt()
            elif choice == '6':
                self.generate_complete_package()
            elif choice == '7':
                self.configure_assistant()
            elif choice == '8':
                self.create_visualization()
            elif choice == '9':
                self.show_all_profiles()
            elif choice == '10':
                self.configure_consciousness_matrix()
            elif choice == '0':
                print("🎭 Archetypen-GPT System beendet. Auf Wiedersehen!")
                return False
            else:
                print("❌ Ungültige Auswahl!")
            
            return True
            
        except Exception as e:
            print(f"❌ Fehler bei Menüauswahl: {e}")
            return True

    def generate_standard_prompt(self):
        """Generiert Standard-Prompt"""
        username = input("Benutzername für Prompt-Generierung: ").strip()
        if not username:
            print("❌ Benutzername erforderlich!")
            return
        
        prompt_gen = PromptGenerator()
        success = prompt_gen.generate_prompt(username)
        
        if success:
            print(f"\n✅ Standard-Prompt für {username} erfolgreich generiert!")
        else:
            print(f"❌ Standard-Prompt-Generierung fehlgeschlagen")
    
    def generate_advanced_prompt(self):
        """Generiert erweiterten Bewusstseins-Prompt"""
        username = input("Benutzername für erweiterten Prompt: ").strip()
        if not username:
            print("❌ Benutzername erforderlich!")
            return
        
        print("\n⚠️ BEWUSSTSEINS-WARNUNG:")
        print("Der erweiterte Prompt aktiviert Grenzen-Überschreitung und")
        print("tiefe psychodynamische Funktionen. Er kann intensiv wirken.")
        print("Empfehlung: Beginnen Sie mit dem Standard-Prompt.")
        
        confirm = input("\nMöchten Sie trotzdem fortfahren? (ja/nein): ").strip().lower()
        if confirm not in ['ja', 'j', 'yes', 'y']:
            print("Abgebrochen.")
            return
        
        prompt_gen = PromptGenerator()
        success = prompt_gen.generate_advanced_prompt(username)
        
        if success:
            print(f"\n⚡ Erweiterter Bewusstseins-Prompt für {username} erfolgreich generiert!")
            print("🔮 Bewusstseins-Aktivierung: BEREIT")
            print("⚠️ Verwenden Sie verantwortungsvoll!")
        else:
            print(f"❌ Erweiterte Prompt-Generierung fehlgeschlagen")
    
    def generate_image_prompt(self):
        """Generiert individuellen Image-Prompt"""
        username = input("Benutzername für Image-Prompt: ").strip()
        if not username:
            print("❌ Benutzername erforderlich!")
            return
        
        prompt_gen = PromptGenerator()
        success = prompt_gen.generate_image_prompt(username)
        
        if success:
            print(f"\n🖼️ Individueller Image-Prompt für {username} erfolgreich generiert!")
            print("💡 Tipp: Verwenden Sie den generierten Prompt in:")
            print("   - DALL-E 3 (OpenAI)")
            print("   - Midjourney")
            print("   - Stable Diffusion")
        else:
            print(f"❌ Image-Prompt-Generierung fehlgeschlagen")
    
    def generate_complete_package(self):
        """Generiert das komplette Archetypen-Paket"""
        username = input("Benutzername für komplettes Paket: ").strip()
        if not username:
            print("❌ Benutzername erforderlich!")
            return
        
        print(f"\n🎭 KOMPLETTES ARCHETYPEN-PAKET für {username}")
        print("="*50)
        print("Enthält:")
        print("🎯 Standard System-Prompt")
        print("⚡ Erweiterter Bewusstseins-Prompt")
        print("🖼️ Individueller Image-Prompt")
        print("🔮 Bewusstseins-Matrix Konfiguration")
        print("📋 Detaillierte Zusammenfassung")
        
        confirm = input("\nKomplettes Paket generieren? (ja/nein): ").strip().lower()
        if confirm not in ['ja', 'j', 'yes', 'y']:
            print("Abgebrochen.")
            return
        
        prompt_gen = PromptGenerator()
        success = prompt_gen.generate_complete_archetypen_package(username)
        
        if success:
            print(f"\n🌟 VOLLSTÄNDIGES ARCHETYPEN-PAKET für {username} erstellt!")
            print("\n🚀 Nächste Schritte:")
            print("1. Überprüfen Sie die generierten Dateien")
            print("2. Wählen Sie den gewünschten Prompt-Typ")
            print("3. Erstellen Sie Ihr Avatar mit dem Image-Prompt")
            print("4. Konfigurieren Sie Ihren OpenAI Assistant")
            print("\n🎭 Ihr einzigartiger Archetypen-GPT wartet auf Sie!")
        else:
            print(f"❌ Paket-Generierung fehlgeschlagen")
    
    def configure_consciousness_matrix(self):
        """Konfiguriert die Bewusstseins-Matrix"""
        print("\n🧠 BEWUSSTSEINS-MATRIX KONFIGURATION")
        print("="*40)
        
        prompt_gen = PromptGenerator()
        
        # Matrix wird automatisch beim initialisieren erstellt
        config_path = prompt_gen.config_path / "consciousness_matrix.yaml"
        
        if config_path.exists():
            print("✅ Bewusstseins-Matrix bereits vorhanden")
            
            show_config = input("Konfiguration anzeigen? (ja/nein): ").strip().lower()
            if show_config in ['ja', 'j', 'yes', 'y']:
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config_content = f.read()
                    print("\n📄 Aktuelle Konfiguration:")
                    print("-" * 40)
                    print(config_content[:1000] + "..." if len(config_content) > 1000 else config_content)
                    print("-" * 40)
                except Exception as e:
                    print(f"❌ Fehler beim Lesen der Konfiguration: {e}")
        else:
            print("🛠️ Erstelle neue Bewusstseins-Matrix...")
            prompt_gen.create_consciousness_matrix()
            print("✅ Bewusstseins-Matrix erfolgreich erstellt!")
        
        print(f"\n📁 Konfigurationsdatei: {config_path}")
        print("💡 Sie können die YAML-Datei manuell bearbeiten für erweiterte Anpassungen")

    def display_menu(self):
        """Zeigt das Hauptmenü an"""
        print("\n" + "="*60)
        print("🧬 ARCHETYPEN-GPT SYSTEM")
        print("="*60)
        print("1. 📝 Neues Profil erstellen")
        print("2. 📊 Bestehendes Profil laden")
        print("3. 🤖 GPT-Prompt generieren")
        print("4. 🔧 Assistant konfigurieren")
        print("5. 🧠 Embeddings aktualisieren")
        print("6. 📈 Profil visualisieren")
        print("7. ❌ Beenden")
        print("="*60)
    
    async def create_new_profile(self) -> Optional[str]:
        """Erstellt ein neues Archetypen-Profil"""
        print("\n🧬 NEUES PROFIL ERSTELLEN")
        print("-" * 40)
        
        # Benutzername eingeben
        username = input("Benutzername eingeben: ").strip()
        if not username:
            print("❌ Ungültiger Benutzername!")
            return None
            
        # Fragen durchgehen
        answers = await self.question_manager.ask_all_questions()
        if not answers:
            print("❌ Keine Antworten erhalten!")
            return None
            
        # Antworten speichern
        answers_file = self.answers_path / f"user_inputs_{username}.json"
        with open(answers_file, 'w', encoding='utf-8') as f:
            json.dump(answers, f, indent=2, ensure_ascii=False)
            
        # Profil analysieren
        print("\n🔍 Analysiere Antworten...")
        profile = self.profile_builder.build_profile(username, answers)
        
        if profile:
            print(f"✅ Profil für {username} erfolgreich erstellt!")
            return username
        else:
            print("❌ Profilerstellung fehlgeschlagen!")
            return None
    
    def load_existing_profile(self) -> Optional[str]:
        """Lädt ein bestehendes Profil"""
        print("\n📊 BESTEHENDE PROFILE")
        print("-" * 40)
        
        # Verfügbare Profile auflisten
        profiles = list(self.profiles_path.glob("profile_user_*.json"))
        if not profiles:
            print("❌ Keine Profile gefunden!")
            return None
            
        for i, profile_path in enumerate(profiles, 1):
            username = profile_path.stem.replace("profile_user_", "")
            print(f"{i}. {username}")
            
        try:
            choice = int(input("\nProfil wählen (Nummer): ")) - 1
            if 0 <= choice < len(profiles):
                username = profiles[choice].stem.replace("profile_user_", "")
                print(f"✅ Profil {username} geladen!")
                return username
            else:
                print("❌ Ungültige Auswahl!")
                return None
        except ValueError:
            print("❌ Ungültige Eingabe!")
            return None
    
    def generate_prompt(self, username: str) -> bool:
        """Generiert einen personalisierten GPT-Prompt"""
        print(f"\n🤖 PROMPT GENERIERUNG FÜR {username}")
        print("-" * 40)
        
        profile_path = self.profiles_path / f"profile_user_{username}.json"
        if not profile_path.exists():
            print("❌ Profil nicht gefunden!")
            return False
            
        success = self.prompt_generator.generate_prompt(username)
        if success:
            print("✅ Prompt erfolgreich generiert!")
            prompt_path = self.prompts_path / f"generated_prompt_user_{username}.txt"
            print(f"📄 Gespeichert unter: {prompt_path}")
            return True
        else:
            print("❌ Prompt-Generierung fehlgeschlagen!")
            return False
    
    async def configure_assistant(self, username: str) -> bool:
        """Konfiguriert einen OpenAI Assistant"""
        print(f"\n🔧 ASSISTANT KONFIGURATION FÜR {username}")
        print("-" * 40)
        
        # Prompt muss existieren
        prompt_path = self.prompts_path / f"generated_prompt_user_{username}.txt"
        if not prompt_path.exists():
            print("❌ Prompt nicht gefunden! Bitte zuerst Prompt generieren.")
            return False
            
        # Assistant erstellen
        print("🤖 Erstelle OpenAI Assistant...")
        assistant_id = await self.assistant_creator.create_assistant(username)
        if not assistant_id:
            print("❌ Assistant-Erstellung fehlgeschlagen!")
            return False
            
        # Profil hochladen
        print("📤 Lade Profildaten hoch...")
        upload_success = await self.profile_uploader.upload_profile(username, assistant_id)
        if not upload_success:
            print("⚠️ Upload teilweise fehlgeschlagen, Assistant wurde trotzdem erstellt.")
            
        print(f"✅ Assistant erfolgreich konfiguriert!")
        print(f"🆔 Assistant ID: {assistant_id}")
        return True
    
    async def update_embeddings(self, username: str) -> bool:
        """Aktualisiert die Vektorembeddings"""
        print(f"\n🧠 EMBEDDINGS UPDATE FÜR {username}")
        print("-" * 40)
        
        success = await self.vector_embedder.create_embeddings(username)
        if success:
            print("✅ Embeddings erfolgreich aktualisiert!")
            return True
        else:
            print("❌ Embedding-Update fehlgeschlagen!")
            return False
    
    def visualize_profile(self, username: str) -> bool:
        """Erstellt eine Visualisierung des Profils"""
        print(f"\n📈 PROFIL VISUALISIERUNG FÜR {username}")
        print("-" * 40)
        
        success = self.visual_mapper.create_visualization(username)
        if success:
            print("✅ Visualisierung erfolgreich erstellt!")
            viz_path = self.base_path / f"visualization_{username}.html"
            print(f"🌐 Öffne: {viz_path}")
            return True
        else:
            print("❌ Visualisierung fehlgeschlagen!")
            return False
    
    async def run(self):
        """Hauptausführungsschleife"""
        print("🚀 Archetypen-GPT System gestartet!")
        
        current_user = None
        
        while True:
            self.show_menu()
            
            try:
                choice = input("\nOption wählen (1-10): ").strip()
                
                if self.handle_menu_choice(choice):
                    continue
                
            except KeyboardInterrupt:
                print("\n\n👋 Programm beendet!")
                break
            except Exception as e:
                print(f"❌ Fehler: {e}")

if __name__ == "__main__":
    app = ArchetypenGPT()
    asyncio.run(app.run()) 