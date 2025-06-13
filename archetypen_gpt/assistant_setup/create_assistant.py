"""
OpenAI Assistant Creator für Archetypen-GPT System
Erstellt personalisierte GPT-Assistenten über die OpenAI API
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

class AssistantCreator:
    """Erstellt und verwaltet OpenAI Assistenten"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.prompts_path = self.base_path / "prompts"
        self.profiles_path = self.base_path / "profiles"
        self.config_path = self.base_path / "config"
        
        # OpenAI Client initialisieren
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY nicht in Umgebungsvariablen gefunden!")
        
        self.client = AsyncOpenAI(api_key=api_key)
        
        # Konfiguration laden
        self.config = self.load_config()
        
        # Assistenten-Datenbank
        self.assistants_db_path = self.config_path / "assistants.json"
        self.assistants_db = self.load_assistants_db()
    
    def load_config(self) -> Dict[str, Any]:
        """Lädt Konfiguration oder erstellt Standardkonfiguration"""
        config_file = self.config_path / "openai_keys.json"
        
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Standardkonfiguration erstellen
            default_config = {
                "model": "gpt-4-turbo-preview",
                "temperature": 0.7,
                "max_tokens": 4000,
                "assistant_name_prefix": "Archetypen-GPT",
                "assistant_description": "Personalisierter Archetypen-GPT basierend auf psychodynamischer Analyse"
            }
            
            # Verzeichnis und Datei erstellen
            self.config_path.mkdir(exist_ok=True)
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
            
            return default_config
    
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
    
    async def create_assistant(self, username: str) -> Optional[str]:
        """Erstellt einen neuen OpenAI Assistant für einen Benutzer"""
        try:
            # Prüfen ob Assistant bereits existiert
            if username in self.assistants_db["assistants"]:
                existing_id = self.assistants_db["assistants"][username]["assistant_id"]
                print(f"⚠️ Assistant für {username} existiert bereits: {existing_id}")
                
                # Prüfen ob Assistant noch aktiv ist
                if await self.validate_assistant(existing_id):
                    return existing_id
                else:
                    print("🔄 Alter Assistant nicht mehr verfügbar, erstelle neuen...")
            
            # Prompt laden
            prompt_path = self.prompts_path / f"generated_prompt_user_{username}.txt"
            if not prompt_path.exists():
                print(f"❌ Prompt für {username} nicht gefunden! Bitte zuerst Prompt generieren.")
                return None
            
            with open(prompt_path, 'r', encoding='utf-8') as f:
                system_prompt = f.read()
            
            # Profil-Daten für zusätzliche Informationen laden
            profile_data = self.load_profile_data(username)
            
            # Assistant erstellen
            assistant_name = f"{self.config['assistant_name_prefix']} - {username}"
            
            print(f"🤖 Erstelle Assistant '{assistant_name}'...")
            
            assistant = await self.client.beta.assistants.create(
                name=assistant_name,
                instructions=system_prompt,
                description=f"{self.config['assistant_description']} für {username}",
                model=self.config["model"],
                tools=[
                    {"type": "code_interpreter"},
                    {"type": "retrieval"}
                ],
                metadata={
                    "username": username,
                    "created_by": "archetypen_gpt_system",
                    "profile_version": "1.0"
                }
            )
            
            assistant_id = assistant.id
            
            # Assistant-Informationen speichern
            self.assistants_db["assistants"][username] = {
                "assistant_id": assistant_id,
                "assistant_name": assistant_name,
                "created_at": assistant.created_at,
                "model": assistant.model,
                "profile_data": profile_data
            }
            
            self.save_assistants_db()
            
            print(f"✅ Assistant erfolgreich erstellt!")
            print(f"🆔 Assistant ID: {assistant_id}")
            print(f"📝 Name: {assistant_name}")
            
            return assistant_id
            
        except Exception as e:
            print(f"❌ Fehler beim Assistant-Erstellen: {e}")
            return None
    
    async def validate_assistant(self, assistant_id: str) -> bool:
        """Validiert ob ein Assistant noch existiert und funktioniert"""
        try:
            assistant = await self.client.beta.assistants.retrieve(assistant_id)
            return assistant.id == assistant_id
        except:
            return False
    
    def load_profile_data(self, username: str) -> Dict[str, Any]:
        """Lädt Profil-Daten für zusätzliche Assistant-Informationen"""
        try:
            profile_path = self.profiles_path / f"profile_user_{username}.json"
            if profile_path.exists():
                with open(profile_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        return {}
    
    async def update_assistant(self, username: str) -> bool:
        """Aktualisiert einen bestehenden Assistant mit neuen Profil-Daten"""
        try:
            if username not in self.assistants_db["assistants"]:
                print(f"❌ Kein Assistant für {username} gefunden!")
                return False
            
            assistant_id = self.assistants_db["assistants"][username]["assistant_id"]
            
            # Neuen Prompt laden
            prompt_path = self.prompts_path / f"generated_prompt_user_{username}.txt"
            if not prompt_path.exists():
                print(f"❌ Prompt für {username} nicht gefunden!")
                return False
            
            with open(prompt_path, 'r', encoding='utf-8') as f:
                system_prompt = f.read()
            
            # Assistant aktualisieren
            await self.client.beta.assistants.update(
                assistant_id,
                instructions=system_prompt,
                metadata={
                    "username": username,
                    "updated_by": "archetypen_gpt_system",
                    "profile_version": "1.1"
                }
            )
            
            print(f"✅ Assistant für {username} aktualisiert!")
            return True
            
        except Exception as e:
            print(f"❌ Fehler beim Assistant-Update: {e}")
            return False
    
    async def delete_assistant(self, username: str) -> bool:
        """Löscht einen Assistant"""
        try:
            if username not in self.assistants_db["assistants"]:
                print(f"❌ Kein Assistant für {username} gefunden!")
                return False
            
            assistant_id = self.assistants_db["assistants"][username]["assistant_id"]
            
            # Assistant löschen
            await self.client.beta.assistants.delete(assistant_id)
            
            # Aus Datenbank entfernen
            del self.assistants_db["assistants"][username]
            self.save_assistants_db()
            
            print(f"✅ Assistant für {username} gelöscht!")
            return True
            
        except Exception as e:
            print(f"❌ Fehler beim Assistant-Löschen: {e}")
            return False
    
    async def create_thread_and_run(self, username: str, user_message: str) -> Optional[str]:
        """Erstellt einen Thread und führt eine Nachricht aus"""
        try:
            if username not in self.assistants_db["assistants"]:
                print(f"❌ Kein Assistant für {username} gefunden!")
                return None
            
            assistant_id = self.assistants_db["assistants"][username]["assistant_id"]
            
            # Thread erstellen
            thread = await self.client.beta.threads.create()
            
            # Nachricht hinzufügen
            await self.client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=user_message
            )
            
            # Run erstellen
            run = await self.client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=assistant_id
            )
            
            # Auf Fertigstellung warten
            while run.status in ["queued", "in_progress", "cancelling"]:
                await asyncio.sleep(1)
                run = await self.client.beta.threads.runs.retrieve(
                    thread_id=thread.id,
                    run_id=run.id
                )
            
            if run.status == "completed":
                # Antwort abrufen
                messages = await self.client.beta.threads.messages.list(
                    thread_id=thread.id
                )
                
                # Neueste Antwort finden
                for message in messages.data:
                    if message.role == "assistant":
                        return message.content[0].text.value
            
            return None
            
        except Exception as e:
            print(f"❌ Fehler beim Thread-Run: {e}")
            return None
    
    def list_assistants(self) -> List[Dict[str, Any]]:
        """Listet alle erstellten Assistenten auf"""
        assistants = []
        for username, data in self.assistants_db["assistants"].items():
            assistants.append({
                "username": username,
                "assistant_id": data["assistant_id"],
                "assistant_name": data["assistant_name"],
                "created_at": data["created_at"],
                "model": data["model"]
            })
        return assistants
    
    def get_assistant_info(self, username: str) -> Optional[Dict[str, Any]]:
        """Holt Informationen über einen Assistant"""
        if username in self.assistants_db["assistants"]:
            return self.assistants_db["assistants"][username]
        return None
    
    async def test_assistant(self, username: str) -> bool:
        """Testet einen Assistant mit einer einfachen Nachricht"""
        try:
            test_message = f"Hallo, ich bin {username}. Erkennst du mich?"
            response = await self.create_thread_and_run(username, test_message)
            
            if response:
                print(f"✅ Assistant-Test erfolgreich!")
                print(f"🤖 Antwort: {response[:200]}...")
                return True
            else:
                print(f"❌ Assistant-Test fehlgeschlagen!")
                return False
                
        except Exception as e:
            print(f"❌ Fehler beim Assistant-Test: {e}")
            return False
    
    async def batch_create_assistants(self, usernames: List[str]) -> Dict[str, str]:
        """Erstellt mehrere Assistenten gleichzeitig"""
        results = {}
        
        tasks = []
        for username in usernames:
            task = self.create_assistant(username)
            tasks.append(task)
        
        # Parallel ausführen
        assistant_ids = await asyncio.gather(*tasks, return_exceptions=True)
        
        for username, assistant_id in zip(usernames, assistant_ids):
            if isinstance(assistant_id, Exception):
                results[username] = f"Fehler: {assistant_id}"
            else:
                results[username] = assistant_id or "Fehler beim Erstellen"
        
        return results
    
    def export_assistant_config(self, username: str) -> Optional[Dict[str, Any]]:
        """Exportiert Assistant-Konfiguration für Backup"""
        if username not in self.assistants_db["assistants"]:
            return None
        
        assistant_data = self.assistants_db["assistants"][username]
        
        # Prompt laden
        prompt_path = self.prompts_path / f"generated_prompt_user_{username}.txt"
        prompt_content = ""
        if prompt_path.exists():
            with open(prompt_path, 'r', encoding='utf-8') as f:
                prompt_content = f.read()
        
        return {
            "username": username,
            "assistant_data": assistant_data,
            "system_prompt": prompt_content,
            "export_timestamp": assistant_data.get("created_at"),
            "config": self.config
        } 