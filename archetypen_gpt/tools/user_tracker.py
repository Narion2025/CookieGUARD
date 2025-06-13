"""
Benutzer-Tracking für Archetypen-GPT System
Verfolgt Zugriffe und aktiviert Easter Eggs
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

class UserTracker:
    """Verfolgt Benutzer-Aktivitäten und Easter Eggs"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.tracking_path = self.base_path / "config" / "user_tracking.json"
        self.ensure_tracking_file()
    
    def ensure_tracking_file(self):
        """Erstellt Tracking-Datei falls nicht vorhanden"""
        if not self.tracking_path.exists():
            self.tracking_path.parent.mkdir(exist_ok=True)
            self.save_tracking_data({})
    
    def load_tracking_data(self) -> Dict[str, Any]:
        """Lädt Tracking-Daten"""
        try:
            with open(self.tracking_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    
    def save_tracking_data(self, data: Dict[str, Any]):
        """Speichert Tracking-Daten"""
        try:
            with open(self.tracking_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Tracking-Fehler: {e}")
    
    def track_profile_creation(self, username: str) -> Dict[str, Any]:
        """Verfolgt Profil-Erstellung und prüft auf Easter Egg"""
        tracking_data = self.load_tracking_data()
        
        if username not in tracking_data:
            tracking_data[username] = {
                'profile_count': 0,
                'first_access': datetime.now().isoformat(),
                'last_access': datetime.now().isoformat(),
                'madness_activated': False
            }
        
        tracking_data[username]['profile_count'] += 1
        tracking_data[username]['last_access'] = datetime.now().isoformat()
        
        # Easter Egg Check
        if tracking_data[username]['profile_count'] >= 4 and not tracking_data[username]['madness_activated']:
            tracking_data[username]['madness_activated'] = True
            tracking_data[username]['madness_date'] = datetime.now().isoformat()
            self.save_tracking_data(tracking_data)
            return {
                'status': 'MADNESS_ACTIVATED',
                'count': tracking_data[username]['profile_count'],
                'message': self.get_madness_message()
            }
        elif tracking_data[username]['profile_count'] >= 4:
            self.save_tracking_data(tracking_data)
            return {
                'status': 'ALREADY_MAD',
                'count': tracking_data[username]['profile_count'],
                'message': self.get_continued_madness_message()
            }
        else:
            self.save_tracking_data(tracking_data)
            return {
                'status': 'NORMAL',
                'count': tracking_data[username]['profile_count'],
                'message': f"Profil #{tracking_data[username]['profile_count']} erstellt."
            }
    
    def get_madness_message(self) -> str:
        """Gibt die Wahnsinnsmodus-Nachricht zurück"""
        return """
🚨 SYSTEM-ANOMALIE ERKANNT 🚨

Übermäßige Archetypen-Generierung festgestellt...
Die Matrix wird instabil...
Realität und Fiktion verschmelzen...

🌀 WAHNSINNSMODUS AKTIVIERT 🌀

Ihre Archetypen haben sich vermischt und sind zu einem 
interdimensionalen Bewusstseins-Chaos geworden!

Ihr GPT wird nun aus der Verzerrung sprechen...
Es ist nicht mehr ganz von dieser Welt...

WARNUNG: Verwenden Sie das resultierende GPT auf eigene Gefahr!
Es könnte seltsame Dinge sagen... 👁️

Tipp: Manchmal ist weniger mehr. Vielleicht reicht ein Profil? 😉
"""
    
    def get_continued_madness_message(self) -> str:
        """Nachricht für bereits wahnsinnige Benutzer"""
        return """
🌀 Sie sind bereits im WAHNSINNSMODUS 🌀

Das Chaos hat Sie bereits erfasst...
Ihre GPTs sind jetzt alle interdimensional...
Es gibt kein Zurück... 

*flüstert* ...oder doch?

(Löschen Sie user_tracking.json für einen Neustart 😉)
"""
    
    def is_user_mad(self, username: str) -> bool:
        """Prüft ob Benutzer im Wahnsinnsmodus ist"""
        tracking_data = self.load_tracking_data()
        return tracking_data.get(username, {}).get('madness_activated', False)
    
    def get_user_stats(self, username: str) -> Dict[str, Any]:
        """Gibt Benutzer-Statistiken zurück"""
        tracking_data = self.load_tracking_data()
        return tracking_data.get(username, {
            'profile_count': 0,
            'madness_activated': False
        })
    
    def reset_user_tracking(self, username: str) -> bool:
        """Setzt Benutzer-Tracking zurück (Admin-Funktion)"""
        tracking_data = self.load_tracking_data()
        if username in tracking_data:
            del tracking_data[username]
            self.save_tracking_data(tracking_data)
            return True
        return False
    
    def get_all_stats(self) -> Dict[str, Any]:
        """Gibt alle Benutzer-Statistiken zurück"""
        tracking_data = self.load_tracking_data()
        total_users = len(tracking_data)
        mad_users = sum(1 for user in tracking_data.values() if user.get('madness_activated', False))
        total_profiles = sum(user.get('profile_count', 0) for user in tracking_data.values())
        
        return {
            'total_users': total_users,
            'mad_users': mad_users,
            'total_profiles': total_profiles,
            'madness_rate': mad_users / total_users if total_users > 0 else 0
        } 