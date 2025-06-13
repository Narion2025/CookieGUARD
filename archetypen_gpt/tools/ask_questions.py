"""
Fragemodul für Archetypen-GPT System
Lädt und stellt Fragen aus den Markdown-Dateien
"""

import os
import re
import yaml
import json
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class Question:
    """Datenklasse für eine Frage"""
    id: str
    category: str
    title: str
    text: str
    options: List[str]
    metadata: Dict[str, Any]
    follow_up: Optional[str] = None

class QuestionManager:
    """Verwaltet und stellt Fragen aus Markdown-Dateien"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.questions_path = self.base_path / "questions"
        self.questions: Dict[str, List[Question]] = {}
        self.load_all_questions()
    
    def load_all_questions(self):
        """Lädt alle Fragen aus den Markdown-Dateien"""
        question_files = {
            'archetypen': 'archetypen.md',
            'schatten': 'schatten.md',
            'spiral_dynamics': 'spiral_dynamics.md'
        }
        
        for category, filename in question_files.items():
            file_path = self.questions_path / filename
            if file_path.exists():
                self.questions[category] = self.parse_questions_from_markdown(file_path, category)
                print(f"✅ {len(self.questions[category])} {category}-Fragen geladen")
            else:
                print(f"❌ Datei nicht gefunden: {file_path}")
                self.questions[category] = []
    
    def parse_questions_from_markdown(self, file_path: Path, category: str) -> List[Question]:
        """Parst Fragen aus einer Markdown-Datei"""
        questions = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Fragen-Blöcke finden
            question_blocks = re.split(r'\n---\n', content)
            
            for block in question_blocks:
                if not block.strip():
                    continue
                    
                question = self.parse_question_block(block, category)
                if question:
                    questions.append(question)
                    
        except Exception as e:
            print(f"❌ Fehler beim Parsen von {file_path}: {e}")
            
        return questions
    
    def parse_question_block(self, block: str, category: str) -> Optional[Question]:
        """Parst einen einzelnen Fragen-Block"""
        try:
            # YAML-Metadaten extrahieren
            yaml_match = re.search(r'```yaml\n(.*?)\n```', block, re.DOTALL)
            metadata = {}
            if yaml_match:
                metadata = yaml.safe_load(yaml_match.group(1))
            
            # Titel extrahieren
            title_match = re.search(r'## (.*?)\n', block)
            title = title_match.group(1) if title_match else "Unbekannt"
            
            # Hauptfrage extrahieren
            question_match = re.search(r'\*\*(.*?)\*\*', block)
            question_text = question_match.group(1) if question_match else ""
            
            # Optionen extrahieren
            options = []
            option_matches = re.findall(r'[a-h]\) (.*?)(?=\n|$)', block)
            options = [opt.strip() for opt in option_matches]
            
            # Follow-up Frage extrahieren
            follow_up_match = re.search(r'\*(.*?)\*\s*$', block, re.MULTILINE)
            follow_up = follow_up_match.group(1) if follow_up_match else None
            
            return Question(
                id=metadata.get('id', f"{category}_{len(options)}"),
                category=category,
                title=title,
                text=question_text,
                options=options,
                metadata=metadata,
                follow_up=follow_up
            )
            
        except Exception as e:
            print(f"❌ Fehler beim Parsen eines Fragen-Blocks: {e}")
            return None
    
    async def ask_all_questions(self) -> Dict[str, Any]:
        """Stellt alle Fragen interaktiv und sammelt Antworten"""
        print("\n🧬 ARCHETYPEN-ANALYSE STARTEN")
        print("=" * 50)
        print("Beantworte die folgenden Fragen so ehrlich wie möglich.")
        print("Bei Multiple-Choice-Fragen kannst du auch mehrere Antworten wählen (z.B. 'a,c').")
        print("=" * 50)
        
        all_answers = {}
        
        # Reihenfolge der Fragenkategorien
        categories = ['archetypen', 'schatten', 'spiral_dynamics']
        
        for category in categories:
            if category not in self.questions:
                continue
                
            print(f"\n🔍 {category.upper().replace('_', ' ')}-FRAGEN")
            print("-" * 40)
            
            category_answers = []
            questions = self.questions[category]
            
            for i, question in enumerate(questions, 1):
                print(f"\n📋 Frage {i}/{len(questions)}: {question.title}")
                print(f"🎯 {question.text}")
                
                # Optionen anzeigen
                if question.options:
                    print("\nOptionen:")
                    for j, option in enumerate(question.options):
                        letter = chr(97 + j)  # a, b, c, ...
                        print(f"  {letter}) {option}")
                
                # Antwort einlesen
                while True:
                    try:
                        if question.options:
                            answer = input(f"\nDeine Antwort (z.B. a oder a,c): ").strip().lower()
                            if self.validate_multiple_choice(answer, len(question.options)):
                                break
                            else:
                                print("❌ Ungültige Eingabe! Bitte verwende gültige Buchstaben.")
                        else:
                            answer = input(f"\nDeine Antwort: ").strip()
                            if answer:
                                break
                            else:
                                print("❌ Bitte gib eine Antwort ein!")
                    except KeyboardInterrupt:
                        print("\n\n❌ Abgebrochen!")
                        return {}
                
                # Follow-up Frage
                follow_up_answer = ""
                if question.follow_up:
                    print(f"\n💭 {question.follow_up}")
                    follow_up_answer = input("Antwort (optional): ").strip()
                
                # Antwort speichern
                question_answer = {
                    'question_id': question.id,
                    'question_text': question.text,
                    'answer': answer,
                    'follow_up_answer': follow_up_answer,
                    'metadata': question.metadata,
                    'timestamp': asyncio.get_event_loop().time()
                }
                
                category_answers.append(question_answer)
                
                # Kurze Pause für bessere UX
                await asyncio.sleep(0.1)
            
            all_answers[category] = category_answers
            print(f"\n✅ {category.upper().replace('_', ' ')}-Fragen abgeschlossen!")
        
        print(f"\n🎉 Alle Fragen beantwortet! Insgesamt {self.count_total_answers(all_answers)} Antworten.")
        return all_answers
    
    def validate_multiple_choice(self, answer: str, max_options: int) -> bool:
        """Validiert Multiple-Choice-Antworten"""
        if not answer:
            return False
            
        # Einzelne Antworten aufteilen
        choices = [choice.strip() for choice in answer.split(',')]
        
        for choice in choices:
            if len(choice) != 1 or not choice.isalpha():
                return False
            
            # Prüfen ob Buchstabe im gültigen Bereich
            option_index = ord(choice) - ord('a')
            if option_index < 0 or option_index >= max_options:
                return False
                
        return True
    
    def count_total_answers(self, answers: Dict[str, Any]) -> int:
        """Zählt die Gesamtanzahl der Antworten"""
        total = 0
        for category_answers in answers.values():
            total += len(category_answers)
        return total
    
    def get_question_by_id(self, question_id: str) -> Optional[Question]:
        """Findet eine Frage anhand ihrer ID"""
        for category_questions in self.questions.values():
            for question in category_questions:
                if question.id == question_id:
                    return question
        return None
    
    def get_questions_by_archetype(self, archetype: str) -> List[Question]:
        """Findet alle Fragen zu einem bestimmten Archetyp"""
        matching_questions = []
        
        for category_questions in self.questions.values():
            for question in category_questions:
                if 'archetypes' in question.metadata:
                    if archetype in question.metadata['archetypes']:
                        matching_questions.append(question)
                        
        return matching_questions
    
    def get_questions_by_marker(self, marker: str) -> List[Question]:
        """Findet alle Fragen zu einem bestimmten Marker"""
        matching_questions = []
        
        for category_questions in self.questions.values():
            for question in category_questions:
                if 'markers' in question.metadata:
                    if marker in question.metadata['markers']:
                        matching_questions.append(question)
                        
        return matching_questions 