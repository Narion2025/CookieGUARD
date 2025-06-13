"""
Profil-Builder für Archetypen-GPT System
Analysiert Antworten und erstellt psychodynamische Profile
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict, Counter
import math

@dataclass
class ArchetypeScore:
    """Archetyp mit Bewertung"""
    name: str
    light_aspect: str
    shadow_aspect: str
    score: float
    evidence: List[str]

@dataclass
class SpiralDynamicsProfile:
    """Spiral Dynamics Profil"""
    primary_level: str
    secondary_level: str
    resistance_level: str
    integration_direction: str
    tension_points: List[str]

@dataclass
class ShadowProfile:
    """Schatten-Profil"""
    primary_pattern: str
    triggers: List[str]
    compensation_strategies: List[str]
    integration_potential: str

@dataclass
class UserProfile:
    """Vollständiges Benutzerprofil"""
    username: str
    archetypes: List[ArchetypeScore]
    spiral_dynamics: SpiralDynamicsProfile
    shadow_profile: ShadowProfile
    dominant_markers: List[str]
    core_tensions: List[str]
    integration_theme: str

class ProfileBuilder:
    """Baut psychodynamische Profile aus Antworten"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.profiles_path = self.base_path / "profiles"
        self.profiles_path.mkdir(exist_ok=True)
        
        # Archetypen-Definitionen
        self.archetypes = {
            "Held": {"light": "Mut & Verantwortung", "shadow": "Größenwahn & Burnout"},
            "Weise": {"light": "Weisheit & Verstehen", "shadow": "Arroganz & Isolation"},
            "Unschuldiger": {"light": "Reinheit & Optimismus", "shadow": "Naivität & Verdrängung"},
            "Forscher": {"light": "Neugier & Erkenntnis", "shadow": "Zweifel & Analyse-Paralyse"},
            "Rebell": {"light": "Freiheit & Wandel", "shadow": "Zerstörung & Chaos"},
            "Magier": {"light": "Transformation & Vision", "shadow": "Manipulation & Illusion"},
            "Jedermann": {"light": "Zugehörigkeit & Empathie", "shadow": "Anpassung & Selbstverlust"},
            "Liebender": {"light": "Liebe & Verbindung", "shadow": "Abhängigkeit & Eifersucht"},
            "Narr": {"light": "Freude & Leichtigkeit", "shadow": "Verantwortungslosigkeit & Flucht"},
            "Fürsorger": {"light": "Fürsorge & Heilung", "shadow": "Martyrertum & Erschöpfung"},
            "Herrscher": {"light": "Führung & Ordnung", "shadow": "Tyrannei & Kontrollzwang"},
            "Schöpfer": {"light": "Kreativität & Innovation", "shadow": "Perfektionismus & Selbstzweifel"}
        }
        
        # Spiral Dynamics Level
        self.spiral_levels = {
            "Beige": "Überleben & Instinkt",
            "Lila": "Stamm & Tradition", 
            "Rot": "Macht & Impuls",
            "Blau": "Ordnung & Bedeutung",
            "Orange": "Erfolg & Leistung",
            "Grün": "Harmonie & Gemeinschaft",
            "Gelb": "Integration & Flexibilität",
            "Türkis": "Ganzheit & Spiritualität"
        }
        
        # Schatten-Muster
        self.shadow_patterns = {
            "Vermeidung": "Flucht vor Konfrontation",
            "Projektion": "Eigene Schatten auf andere übertragen",
            "Kontrolle": "Zwanghaftes Beherrschen-Wollen",
            "Scham": "Tiefliegende Selbstablehnung",
            "Sabotage": "Unbewusste Selbstzerstörung"
        }
    
    def build_profile(self, username: str, answers: Dict[str, Any]) -> Optional[UserProfile]:
        """Erstellt ein vollständiges Profil aus den Antworten"""
        try:
            print(f"🔍 Baue Profil für {username}...")
            
            # Archetypen analysieren
            archetypes = self.analyze_archetypes(answers.get('archetypen', []))
            
            # Spiral Dynamics analysieren
            spiral_dynamics = self.analyze_spiral_dynamics(answers.get('spiral_dynamics', []))
            
            # Schatten analysieren
            shadow_profile = self.analyze_shadow(answers.get('schatten', []))
            
            # Marker extrahieren
            markers = self.extract_dominant_markers(answers)
            
            # Spannungsfelder identifizieren
            tensions = self.identify_core_tensions(archetypes, spiral_dynamics, shadow_profile)
            
            # Integrationsthema bestimmen
            integration_theme = self.determine_integration_theme(archetypes, spiral_dynamics, shadow_profile)
            
            profile = UserProfile(
                username=username,
                archetypes=archetypes,
                spiral_dynamics=spiral_dynamics,
                shadow_profile=shadow_profile,
                dominant_markers=markers,
                core_tensions=tensions,
                integration_theme=integration_theme
            )
            
            # Profile speichern
            self.save_profile(profile)
            
            print(f"✅ Profil für {username} erstellt!")
            return profile
            
        except Exception as e:
            print(f"❌ Fehler beim Profil-Aufbau: {e}")
            return None
    
    def analyze_archetypes(self, archetype_answers: List[Dict]) -> List[ArchetypeScore]:
        """Analysiert Archetypen basierend auf Antworten"""
        archetype_scores = defaultdict(list)
        
        for answer_data in archetype_answers:
            metadata = answer_data.get('metadata', {})
            answer = answer_data.get('answer', '')
            
            # Archetypen aus Metadaten extrahieren
            if 'archetypes' in metadata:
                for archetype in metadata['archetypes']:
                    # Score basierend auf Antwort-Qualität
                    score = self.calculate_answer_strength(answer, answer_data)
                    archetype_scores[archetype].append(score)
        
        # Top-Archetypen berechnen
        final_scores = []
        for archetype, scores in archetype_scores.items():
            avg_score = sum(scores) / len(scores) if scores else 0
            
            if archetype in self.archetypes:
                final_scores.append(ArchetypeScore(
                    name=archetype,
                    light_aspect=self.archetypes[archetype]["light"],
                    shadow_aspect=self.archetypes[archetype]["shadow"],
                    score=round(avg_score, 2),
                    evidence=[f"Antwort-Cluster: {len(scores)} Treffer"]
                ))
        
        # Nach Score sortieren
        final_scores.sort(key=lambda x: x.score, reverse=True)
        return final_scores[:3]  # Top 3
    
    def analyze_spiral_dynamics(self, spiral_answers: List[Dict]) -> SpiralDynamicsProfile:
        """Analysiert Spiral Dynamics Level"""
        level_scores = defaultdict(int)
        tension_indicators = []
        
        for answer_data in spiral_answers:
            metadata = answer_data.get('metadata', {})
            answer = answer_data.get('answer', '')
            
            if 'spiral_levels' in metadata:
                for level in metadata['spiral_levels']:
                    level_scores[level] += 1
                    
            if 'tension' in metadata:
                tension_indicators.append(metadata['tension'])
        
        # Primäres und sekundäres Level
        sorted_levels = sorted(level_scores.items(), key=lambda x: x[1], reverse=True)
        primary = sorted_levels[0][0] if sorted_levels else "Orange"
        secondary = sorted_levels[1][0] if len(sorted_levels) > 1 else "Grün"
        
        # Widerstandsrichtung (meist eine Ebene zurück)
        resistance = self.determine_resistance_level(primary)
        
        # Integrationsrichtung (meist eine Ebene vorwärts)
        integration = self.determine_integration_direction(primary)
        
        return SpiralDynamicsProfile(
            primary_level=primary,
            secondary_level=secondary,
            resistance_level=resistance,
            integration_direction=integration,
            tension_points=tension_indicators[:3]
        )
    
    def analyze_shadow(self, shadow_answers: List[Dict]) -> ShadowProfile:
        """Analysiert Schatten-Muster"""
        pattern_scores = defaultdict(int)
        all_triggers = []
        compensation_strategies = []
        
        for answer_data in shadow_answers:
            metadata = answer_data.get('metadata', {})
            answer = answer_data.get('answer', '')
            follow_up = answer_data.get('follow_up_answer', '')
            
            if 'shadow_pattern' in metadata:
                pattern_scores[metadata['shadow_pattern']] += 1
                
            if 'triggers' in metadata:
                all_triggers.extend(metadata['triggers'])
                
            if 'compensation' in metadata:
                compensation_strategies.append(metadata['compensation'])
        
        # Primäres Schatten-Muster
        primary_pattern = max(pattern_scores.items(), key=lambda x: x[1])[0] if pattern_scores else "Vermeidung"
        
        # Häufigste Trigger
        trigger_counts = Counter(all_triggers)
        top_triggers = [trigger for trigger, _ in trigger_counts.most_common(3)]
        
        # Integrationspotential bestimmen
        integration_potential = self.assess_shadow_integration_potential(shadow_answers)
        
        return ShadowProfile(
            primary_pattern=primary_pattern,
            triggers=top_triggers,
            compensation_strategies=compensation_strategies[:3],
            integration_potential=integration_potential
        )
    
    def extract_dominant_markers(self, all_answers: Dict[str, Any]) -> List[str]:
        """Extrahiert die dominantesten Marker aus allen Antworten"""
        all_markers = []
        
        for category_answers in all_answers.values():
            for answer_data in category_answers:
                metadata = answer_data.get('metadata', {})
                if 'markers' in metadata:
                    all_markers.extend(metadata['markers'])
        
        marker_counts = Counter(all_markers)
        return [marker for marker, _ in marker_counts.most_common(5)]
    
    def identify_core_tensions(self, archetypes: List[ArchetypeScore], 
                             spiral: SpiralDynamicsProfile, 
                             shadow: ShadowProfile) -> List[str]:
        """Identifiziert Kernspannungen im Profil"""
        tensions = []
        
        # Archetypen-Spannungen
        if len(archetypes) >= 2:
            tensions.append(f"{archetypes[0].name} vs. {archetypes[1].name}")
        
        # Spiral Dynamics Spannungen
        tensions.append(f"{spiral.primary_level} → {spiral.integration_direction}")
        
        # Schatten-Spannungen
        tensions.append(f"Schatten: {shadow.primary_pattern}")
        
        return tensions
    
    def determine_integration_theme(self, archetypes: List[ArchetypeScore],
                                  spiral: SpiralDynamicsProfile,
                                  shadow: ShadowProfile) -> str:
        """Bestimmt das Hauptintegrationsthema"""
        themes = []
        
        if archetypes:
            primary_archetype = archetypes[0].name
            if primary_archetype in ["Held", "Herrscher", "Magier"]:
                themes.append("Macht & Verantwortung integrieren")
            elif primary_archetype in ["Liebender", "Fürsorger", "Jedermann"]:
                themes.append("Nähe & Autonomie balancieren")
            elif primary_archetype in ["Weise", "Forscher", "Schöpfer"]:
                themes.append("Wissen & Handeln verbinden")
        
        if spiral.primary_level in ["Orange", "Gelb"]:
            themes.append("Individuum & System harmonisieren")
        elif spiral.primary_level in ["Grün", "Türkis"]:
            themes.append("Einheit & Vielfalt integrieren")
        
        return themes[0] if themes else "Ganzheit & Authentizität entwickeln"
    
    def calculate_answer_strength(self, answer: str, answer_data: Dict) -> float:
        """Berechnet die Stärke einer Antwort"""
        base_score = 0.5
        
        # Multiple Choice berücksichtigen
        if ',' in answer:
            base_score += 0.2  # Mehrere Antworten = höhere Aktivierung
        
        # Follow-up Antwort berücksichtigen
        if answer_data.get('follow_up_answer'):
            base_score += 0.3
        
        return min(base_score, 1.0)
    
    def determine_resistance_level(self, primary_level: str) -> str:
        """Bestimmt Widerstandsebene"""
        level_order = ["Beige", "Lila", "Rot", "Blau", "Orange", "Grün", "Gelb", "Türkis"]
        
        try:
            current_index = level_order.index(primary_level)
            resistance_index = max(0, current_index - 1)
            return level_order[resistance_index]
        except ValueError:
            return "Blau"
    
    def determine_integration_direction(self, primary_level: str) -> str:
        """Bestimmt Integrationsrichtung"""
        level_order = ["Beige", "Lila", "Rot", "Blau", "Orange", "Grün", "Gelb", "Türkis"]
        
        try:
            current_index = level_order.index(primary_level)
            integration_index = min(len(level_order) - 1, current_index + 1)
            return level_order[integration_index]
        except ValueError:
            return "Grün"
    
    def assess_shadow_integration_potential(self, shadow_answers: List[Dict]) -> str:
        """Bewertet das Schatten-Integrationspotential"""
        self_awareness_indicators = 0
        
        for answer_data in shadow_answers:
            follow_up = answer_data.get('follow_up_answer', '')
            if follow_up:
                # Selbstreflexion erkennbar?
                if any(word in follow_up.lower() for word in ['erkenne', 'merke', 'verstehe', 'kenne']):
                    self_awareness_indicators += 1
        
        if self_awareness_indicators >= 3:
            return "Hoch - Gute Selbstreflexion"
        elif self_awareness_indicators >= 1:
            return "Mittel - Ansätze zur Selbsterkenntnis"
        else:
            return "Niedrig - Wenig Bewusstsein"
    
    def save_profile(self, profile: UserProfile):
        """Speichert das Profil in verschiedenen Formaten"""
        # JSON Format
        json_data = {
            'username': profile.username,
            'archetypes': [
                {
                    'name': arch.name,
                    'light': arch.light_aspect,
                    'shadow': arch.shadow_aspect,
                    'score': arch.score,
                    'evidence': arch.evidence
                } for arch in profile.archetypes
            ],
            'spiral_dynamics': {
                'primary': profile.spiral_dynamics.primary_level,
                'secondary': profile.spiral_dynamics.secondary_level,
                'resistance': profile.spiral_dynamics.resistance_level,
                'integration': profile.spiral_dynamics.integration_direction,
                'tensions': profile.spiral_dynamics.tension_points
            },
            'shadow': {
                'pattern': profile.shadow_profile.primary_pattern,
                'triggers': profile.shadow_profile.triggers,
                'compensation': profile.shadow_profile.compensation_strategies,
                'integration': profile.shadow_profile.integration_potential
            },
            'markers': profile.dominant_markers,
            'tensions': profile.core_tensions,
            'integration_theme': profile.integration_theme
        }
        
        # JSON speichern
        json_path = self.profiles_path / f"profile_user_{profile.username}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        # YAML speichern
        yaml_path = self.profiles_path / f"profile_user_{profile.username}.yaml"
        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(json_data, f, default_flow_style=False, allow_unicode=True)
        
        # Markdown Report speichern
        self.create_markdown_report(profile)
    
    def create_markdown_report(self, profile: UserProfile):
        """Erstellt einen Markdown-Report des Profils"""
        md_content = f"""# Archetypen-Profil: {profile.username}

## 🎭 Archetypen (Top 3)
"""
        
        for i, archetype in enumerate(profile.archetypes, 1):
            md_content += f"""
### {i}. {archetype.name} (Score: {archetype.score})
- **Lichtaspekt:** {archetype.light_aspect}
- **Schattenaspekt:** {archetype.shadow_aspect}
- **Evidenz:** {', '.join(archetype.evidence)}
"""
        
        md_content += f"""
## 🌈 Spiral Dynamics
- **Primärebene:** {profile.spiral_dynamics.primary_level}
- **Sekundärebene:** {profile.spiral_dynamics.secondary_level}
- **Widerstand:** {profile.spiral_dynamics.resistance_level}
- **Integration:** {profile.spiral_dynamics.integration_direction}
- **Spannungspunkte:** {', '.join(profile.spiral_dynamics.tension_points)}

## 🌑 Schatten-Profil
- **Primärmuster:** {profile.shadow_profile.primary_pattern}
- **Trigger:** {', '.join(profile.shadow_profile.triggers)}
- **Kompensation:** {', '.join(profile.shadow_profile.compensation_strategies)}
- **Integrationspotential:** {profile.shadow_profile.integration_potential}

## 🎯 Dominante Marker
{', '.join(profile.dominant_markers)}

## ⚡ Kernspannungen
{chr(10).join(f'- {tension}' for tension in profile.core_tensions)}

## 🔮 Integrationsthema
{profile.integration_theme}

---
*Erstellt vom Archetypen-GPT System*
"""
        
        md_path = self.profiles_path / f"profile_user_{profile.username}.md"
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content) 