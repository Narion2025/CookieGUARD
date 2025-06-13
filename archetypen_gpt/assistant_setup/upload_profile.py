"""
Profil-Upload-Modul für Archetypen-GPT System
Lädt Profildaten und Dokumente zu OpenAI Assistenten hoch
"""

import os
import json
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional, List
from openai import AsyncOpenAI
from dotenv import load_dotenv

# Umgebungsvariablen laden
load_dotenv()

class ProfileUploader:
    """Verwaltet Upload von Profildaten zu OpenAI Assistenten"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.profiles_path = self.base_path / "profiles"
        self.config_path = self.base_path / "config"
        
        # OpenAI Client initialisieren
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY nicht in Umgebungsvariablen gefunden!")
        
        self.client = AsyncOpenAI(api_key=api_key)
        
        # Assistenten-Datenbank laden
        self.assistants_db_path = self.config_path / "assistants.json"
        self.assistants_db = self.load_assistants_db()
    
    def load_assistants_db(self) -> Dict[str, Any]:
        """Lädt die Assistenten-Datenbank"""
        if self.assistants_db_path.exists():
            with open(self.assistants_db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {"assistants": {}}
    
    def save_assistants_db(self):
        """Speichert die Assistenten-Datenbank"""
        self.config_path.mkdir(exist_ok=True)
        with open(self.assistants_db_path, 'w', encoding='utf-8') as f:
            json.dump(self.assistants_db, f, indent=2, ensure_ascii=False)
    
    async def upload_profile(self, username: str, assistant_id: str) -> bool:
        """Lädt alle Profildaten für einen Benutzer hoch"""
        try:
            print(f"📤 Lade Profildaten für {username} hoch...")
            
            # Profil-Dateien sammeln
            profile_files = self.get_profile_files(username)
            if not profile_files:
                print(f"❌ Keine Profil-Dateien für {username} gefunden!")
                return False
            
            uploaded_files = []
            
            # Jede Datei hochladen
            for file_path in profile_files:
                file_id = await self.upload_file(file_path)
                if file_id:
                    uploaded_files.append({
                        'file_id': file_id,
                        'filename': file_path.name,
                        'path': str(file_path)
                    })
                    print(f"✅ {file_path.name} hochgeladen")
                else:
                    print(f"❌ Fehler beim Upload von {file_path.name}")
            
            # File-IDs zum Assistant hinzufügen
            if uploaded_files:
                success = await self.attach_files_to_assistant(assistant_id, uploaded_files)
                if success:
                    # Upload-Info in Datenbank speichern
                    self.update_assistant_files(username, uploaded_files)
                    print(f"✅ {len(uploaded_files)} Dateien erfolgreich hochgeladen!")
                    return True
                else:
                    print("❌ Fehler beim Anhängen der Dateien an Assistant")
                    return False
            else:
                print("❌ Keine Dateien konnten hochgeladen werden")
                return False
                
        except Exception as e:
            print(f"❌ Fehler beim Profil-Upload: {e}")
            return False
    
    def get_profile_files(self, username: str) -> List[Path]:
        """Sammelt alle relevanten Profil-Dateien"""
        files = []
        
        # JSON Profil
        json_file = self.profiles_path / f"profile_user_{username}.json"
        if json_file.exists():
            files.append(json_file)
        
        # Markdown Report
        md_file = self.profiles_path / f"profile_user_{username}.md"
        if md_file.exists():
            files.append(md_file)
        
        # YAML Profil
        yaml_file = self.profiles_path / f"profile_user_{username}.yaml"
        if yaml_file.exists():
            files.append(yaml_file)
        
        return files
    
    async def upload_file(self, file_path: Path) -> Optional[str]:
        """Lädt eine einzelne Datei hoch"""
        try:
            with open(file_path, 'rb') as f:
                file_response = await self.client.files.create(
                    file=f,
                    purpose='assistants'
                )
            return file_response.id
        except Exception as e:
            print(f"❌ Fehler beim Upload von {file_path}: {e}")
            return None
    
    async def attach_files_to_assistant(self, assistant_id: str, uploaded_files: List[Dict]) -> bool:
        """Hängt hochgeladene Dateien an einen Assistant an"""
        try:
            file_ids = [file_info['file_id'] for file_info in uploaded_files]
            
            # Assistant mit neuen Dateien aktualisieren
            await self.client.beta.assistants.update(
                assistant_id,
                file_ids=file_ids
            )
            
            return True
            
        except Exception as e:
            print(f"❌ Fehler beim Anhängen der Dateien: {e}")
            return False
    
    def update_assistant_files(self, username: str, uploaded_files: List[Dict]):
        """Aktualisiert die Assistenten-Datenbank mit Upload-Informationen"""
        if username in self.assistants_db["assistants"]:
            self.assistants_db["assistants"][username]["uploaded_files"] = uploaded_files
            self.assistants_db["assistants"][username]["last_upload"] = uploaded_files[0].get('upload_time') if uploaded_files else None
            self.save_assistants_db()
    
    async def upload_additional_context(self, username: str, context_text: str, filename: str = "context.txt") -> bool:
        """Lädt zusätzlichen Kontext-Text hoch"""
        try:
            if username not in self.assistants_db["assistants"]:
                print(f"❌ Kein Assistant für {username} gefunden!")
                return False
            
            assistant_id = self.assistants_db["assistants"][username]["assistant_id"]
            
            # Temporäre Datei erstellen
            temp_file = self.profiles_path / f"temp_{username}_{filename}"
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(context_text)
            
            try:
                # Datei hochladen
                file_id = await self.upload_file(temp_file)
                if file_id:
                    # An Assistant anhängen
                    success = await self.attach_files_to_assistant(assistant_id, [{'file_id': file_id, 'filename': filename}])
                    if success:
                        print(f"✅ Zusätzlicher Kontext '{filename}' hochgeladen")
                        return True
                    else:
                        return False
                else:
                    return False
            finally:
                # Temporäre Datei löschen
                if temp_file.exists():
                    temp_file.unlink()
            
        except Exception as e:
            print(f"❌ Fehler beim Upload des zusätzlichen Kontexts: {e}")
            return False
    
    async def list_assistant_files(self, username: str) -> List[Dict[str, Any]]:
        """Listet alle Dateien eines Assistanten auf"""
        try:
            if username not in self.assistants_db["assistants"]:
                return []
            
            assistant_id = self.assistants_db["assistants"][username]["assistant_id"]
            assistant = await self.client.beta.assistants.retrieve(assistant_id)
            
            files_info = []
            for file_id in assistant.file_ids:
                try:
                    file_info = await self.client.files.retrieve(file_id)
                    files_info.append({
                        'file_id': file_id,
                        'filename': file_info.filename,
                        'created_at': file_info.created_at,
                        'bytes': file_info.bytes
                    })
                except:
                    # Datei möglicherweise gelöscht
                    files_info.append({
                        'file_id': file_id,
                        'filename': 'Unbekannt (möglicherweise gelöscht)',
                        'created_at': None,
                        'bytes': 0
                    })
            
            return files_info
            
        except Exception as e:
            print(f"❌ Fehler beim Auflisten der Dateien: {e}")
            return []
    
    async def delete_assistant_file(self, username: str, file_id: str) -> bool:
        """Löscht eine Datei vom Assistant"""
        try:
            if username not in self.assistants_db["assistants"]:
                print(f"❌ Kein Assistant für {username} gefunden!")
                return False
            
            assistant_id = self.assistants_db["assistants"][username]["assistant_id"]
            
            # Datei aus OpenAI löschen
            await self.client.files.delete(file_id)
            
            # Assistant-File-IDs aktualisieren
            assistant = await self.client.beta.assistants.retrieve(assistant_id)
            current_file_ids = assistant.file_ids
            updated_file_ids = [fid for fid in current_file_ids if fid != file_id]
            
            await self.client.beta.assistants.update(
                assistant_id,
                file_ids=updated_file_ids
            )
            
            print(f"✅ Datei {file_id} gelöscht")
            return True
            
        except Exception as e:
            print(f"❌ Fehler beim Löschen der Datei: {e}")
            return False
    
    async def update_all_profiles(self) -> Dict[str, bool]:
        """Aktualisiert Profile für alle Assistenten"""
        results = {}
        
        for username in self.assistants_db["assistants"].keys():
            assistant_id = self.assistants_db["assistants"][username]["assistant_id"]
            success = await self.upload_profile(username, assistant_id)
            results[username] = success
        
        return results
    
    def create_profile_summary(self, username: str) -> str:
        """Erstellt eine Zusammenfassung des Profils als Text"""
        try:
            profile_path = self.profiles_path / f"profile_user_{username}.json"
            if not profile_path.exists():
                return ""
            
            with open(profile_path, 'r', encoding='utf-8') as f:
                profile_data = json.load(f)
            
            # Zusammenfassung erstellen
            summary = f"""ARCHETYPEN-PROFIL ZUSAMMENFASSUNG: {username}

🎭 HAUPTARCHETYPEN:
"""
            
            archetypes = profile_data.get('archetypes', [])[:3]
            for i, arch in enumerate(archetypes, 1):
                summary += f"{i}. {arch['name']} (Score: {arch['score']})\n"
                summary += f"   Licht: {arch['light']}\n"
                summary += f"   Schatten: {arch['shadow']}\n\n"
            
            spiral = profile_data.get('spiral_dynamics', {})
            summary += f"""🌈 SPIRAL DYNAMICS:
- Primärebene: {spiral.get('primary', 'Orange')}
- Entwicklungsrichtung: {spiral.get('integration', 'Grün')}
- Widerstand: {spiral.get('resistance', 'Blau')}

"""
            
            shadow = profile_data.get('shadow', {})
            summary += f"""🌑 SCHATTEN-PROFIL:
- Hauptmuster: {shadow.get('pattern', 'Vermeidung')}
- Trigger: {', '.join(shadow.get('triggers', []))}
- Integrationspotential: {shadow.get('integration', 'Mittel')}

"""
            
            summary += f"""🎯 DOMINANTE MARKER:
{', '.join(profile_data.get('markers', []))}

🔮 INTEGRATIONSTHEMA:
{profile_data.get('integration_theme', 'Ganzheit entwickeln')}

---
Diese Zusammenfassung dient als Referenz für personalisierte Gespräche und tieferes Verstehen der psychodynamischen Struktur.
"""
            
            return summary
            
        except Exception as e:
            print(f"❌ Fehler beim Erstellen der Profil-Zusammenfassung: {e}")
            return ""
    
    async def upload_profile_summary(self, username: str) -> bool:
        """Lädt eine Profil-Zusammenfassung als zusätzlichen Kontext hoch"""
        summary = self.create_profile_summary(username)
        if summary:
            return await self.upload_additional_context(username, summary, "profile_summary.txt")
        return False 