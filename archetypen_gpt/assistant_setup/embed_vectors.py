"""
Vektor-Embedding-Modul für Archetypen-GPT System
Erstellt und verwaltet Embeddings für semantische Suche
"""

import os
import json
import numpy as np
import faiss
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from openai import AsyncOpenAI
from dotenv import load_dotenv
import pickle

# Umgebungsvariablen laden
load_dotenv()

class VectorEmbedder:
    """Erstellt und verwaltet Vektor-Embeddings für Profile"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.profiles_path = self.base_path / "profiles"
        self.embeddings_path = self.base_path / "embeddings"
        self.embeddings_path.mkdir(exist_ok=True)
        
        # OpenAI Client für Embeddings
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY nicht in Umgebungsvariablen gefunden!")
        
        self.client = AsyncOpenAI(api_key=api_key)
        self.embedding_model = "text-embedding-3-small"
        
        # FAISS Index
        self.index = None
        self.metadata = {}
        
        # Embedding-Dimension (für text-embedding-3-small)
        self.embedding_dim = 1536
        
        # Index laden falls vorhanden
        self.load_existing_index()
    
    def load_existing_index(self):
        """Lädt bestehenden FAISS-Index"""
        index_path = self.embeddings_path / "profile_index.faiss"
        metadata_path = self.embeddings_path / "profile_metadata.pkl"
        
        if index_path.exists() and metadata_path.exists():
            try:
                self.index = faiss.read_index(str(index_path))
                with open(metadata_path, 'rb') as f:
                    self.metadata = pickle.load(f)
                print(f"✅ Bestehender Index geladen: {self.index.ntotal} Einträge")
            except Exception as e:
                print(f"⚠️ Fehler beim Laden des Index: {e}")
                self.create_new_index()
        else:
            self.create_new_index()
    
    def create_new_index(self):
        """Erstellt einen neuen FAISS-Index"""
        self.index = faiss.IndexFlatIP(self.embedding_dim)  # Inner Product für Similarity
        self.metadata = {}
        print("✅ Neuer FAISS-Index erstellt")
    
    def save_index(self):
        """Speichert den FAISS-Index"""
        try:
            index_path = self.embeddings_path / "profile_index.faiss"
            metadata_path = self.embeddings_path / "profile_metadata.pkl"
            
            faiss.write_index(self.index, str(index_path))
            with open(metadata_path, 'wb') as f:
                pickle.dump(self.metadata, f)
                
            print(f"✅ Index gespeichert: {self.index.ntotal} Einträge")
        except Exception as e:
            print(f"❌ Fehler beim Speichern des Index: {e}")
    
    async def create_embeddings(self, username: str) -> bool:
        """Erstellt Embeddings für ein Benutzerprofil"""
        try:
            print(f"🧠 Erstelle Embeddings für {username}...")
            
            # Profil laden
            profile_data = self.load_profile(username)
            if not profile_data:
                print(f"❌ Profil für {username} nicht gefunden!")
                return False
            
            # Text-Chunks aus Profil extrahieren
            text_chunks = self.extract_text_chunks(username, profile_data)
            if not text_chunks:
                print(f"❌ Keine Text-Chunks für {username} extrahiert!")
                return False
            
            # Embeddings erstellen
            embeddings = []
            for i, chunk in enumerate(text_chunks):
                print(f"  📝 Verarbeite Chunk {i+1}/{len(text_chunks)}")
                embedding = await self.get_embedding(chunk['text'])
                if embedding is not None:
                    embeddings.append(embedding)
                    chunk['embedding_id'] = len(embeddings) - 1
                else:
                    print(f"⚠️ Embedding für Chunk {i+1} fehlgeschlagen")
            
            if not embeddings:
                print(f"❌ Keine Embeddings erstellt für {username}!")
                return False
            
            # Embeddings zum Index hinzufügen
            self.add_embeddings_to_index(username, embeddings, text_chunks)
            
            # Index speichern
            self.save_index()
            
            print(f"✅ {len(embeddings)} Embeddings für {username} erstellt!")
            return True
            
        except Exception as e:
            print(f"❌ Fehler beim Embedding-Erstellen: {e}")
            return False
    
    def load_profile(self, username: str) -> Optional[Dict[str, Any]]:
        """Lädt Profil-Daten"""
        try:
            profile_path = self.profiles_path / f"profile_user_{username}.json"
            if profile_path.exists():
                with open(profile_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"❌ Fehler beim Profil-Laden: {e}")
        return None
    
    def extract_text_chunks(self, username: str, profile_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extrahiert sinnvolle Text-Chunks aus dem Profil"""
        chunks = []
        
        # 1. Archetypen-Beschreibungen
        archetypes = profile_data.get('archetypes', [])
        for arch in archetypes:
            chunk_text = f"Archetyp {arch['name']}: Lichtaspekt - {arch['light']}, Schattenaspekt - {arch['shadow']}, Score: {arch['score']}"
            chunks.append({
                'text': chunk_text,
                'type': 'archetype',
                'archetype': arch['name'],
                'username': username
            })
        
        # 2. Spiral Dynamics
        spiral = profile_data.get('spiral_dynamics', {})
        if spiral:
            spiral_text = f"Spiral Dynamics: Primärebene {spiral.get('primary')}, Entwicklungsrichtung {spiral.get('integration')}, Widerstand gegen {spiral.get('resistance')}"
            chunks.append({
                'text': spiral_text,
                'type': 'spiral_dynamics',
                'username': username
            })
        
        # 3. Schatten-Profil
        shadow = profile_data.get('shadow', {})
        if shadow:
            shadow_text = f"Schatten-Muster: {shadow.get('pattern')}, Trigger: {', '.join(shadow.get('triggers', []))}, Integrationspotential: {shadow.get('integration')}"
            chunks.append({
                'text': shadow_text,
                'type': 'shadow',
                'username': username
            })
        
        # 4. Marker und Themen
        markers = profile_data.get('markers', [])
        if markers:
            markers_text = f"Dominante Marker: {', '.join(markers)}"
            chunks.append({
                'text': markers_text,
                'type': 'markers',
                'username': username
            })
        
        # 5. Integrationsthema
        integration_theme = profile_data.get('integration_theme', '')
        if integration_theme:
            chunks.append({
                'text': f"Integrationsthema: {integration_theme}",
                'type': 'integration',
                'username': username
            })
        
        # 6. Markdown-Profil laden falls vorhanden
        md_content = self.load_markdown_profile(username)
        if md_content:
            # Markdown in kleinere Chunks aufteilen
            md_chunks = self.split_markdown_content(md_content, username)
            chunks.extend(md_chunks)
        
        return chunks
    
    def load_markdown_profile(self, username: str) -> Optional[str]:
        """Lädt Markdown-Profil"""
        try:
            md_path = self.profiles_path / f"profile_user_{username}.md"
            if md_path.exists():
                with open(md_path, 'r', encoding='utf-8') as f:
                    return f.read()
        except:
            pass
        return None
    
    def split_markdown_content(self, content: str, username: str) -> List[Dict[str, Any]]:
        """Teilt Markdown-Inhalt in sinnvolle Chunks auf"""
        chunks = []
        sections = content.split('\n##')  # Nach Überschriften splitten
        
        for i, section in enumerate(sections):
            if section.strip():
                # Erste 500 Zeichen als Chunk nehmen
                chunk_text = section.strip()[:500]
                if len(chunk_text) > 50:  # Nur sinnvolle Chunks
                    chunks.append({
                        'text': chunk_text,
                        'type': 'markdown_section',
                        'section_index': i,
                        'username': username
                    })
        
        return chunks
    
    async def get_embedding(self, text: str) -> Optional[np.ndarray]:
        """Erstellt Embedding für einen Text"""
        try:
            response = await self.client.embeddings.create(
                model=self.embedding_model,
                input=text
            )
            
            embedding = np.array(response.data[0].embedding, dtype=np.float32)
            # Normalisieren für bessere Similarity-Berechnung
            embedding = embedding / np.linalg.norm(embedding)
            
            return embedding
            
        except Exception as e:
            print(f"❌ Fehler beim Embedding erstellen: {e}")
            return None
    
    def add_embeddings_to_index(self, username: str, embeddings: List[np.ndarray], chunks: List[Dict[str, Any]]):
        """Fügt Embeddings zum FAISS-Index hinzu"""
        try:
            # Embeddings zu Matrix konvertieren
            embedding_matrix = np.array(embeddings, dtype=np.float32)
            
            # Aktuelle Index-Größe
            current_size = self.index.ntotal
            
            # Embeddings zum Index hinzufügen
            self.index.add(embedding_matrix)
            
            # Metadaten speichern
            for i, chunk in enumerate(chunks):
                if 'embedding_id' in chunk:
                    vector_id = current_size + chunk['embedding_id']
                    self.metadata[vector_id] = chunk
            
            print(f"✅ {len(embeddings)} Embeddings zum Index hinzugefügt")
            
        except Exception as e:
            print(f"❌ Fehler beim Index-Update: {e}")
    
    async def semantic_search(self, query: str, k: int = 5, username_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """Führt semantische Suche durch"""
        try:
            if self.index is None or self.index.ntotal == 0:
                print("❌ Kein Index vorhanden!")
                return []
            
            # Query-Embedding erstellen
            query_embedding = await self.get_embedding(query)
            if query_embedding is None:
                print("❌ Query-Embedding fehlgeschlagen!")
                return []
            
            # Suche durchführen
            query_vector = query_embedding.reshape(1, -1)
            similarities, indices = self.index.search(query_vector, min(k * 2, self.index.ntotal))
            
            # Ergebnisse filtern und formatieren
            results = []
            for sim, idx in zip(similarities[0], indices[0]):
                if idx == -1:  # Ungültiger Index
                    continue
                    
                if idx in self.metadata:
                    chunk_data = self.metadata[idx].copy()
                    chunk_data['similarity'] = float(sim)
                    
                    # Username-Filter anwenden
                    if username_filter and chunk_data.get('username') != username_filter:
                        continue
                    
                    results.append(chunk_data)
            
            # Nach Similarity sortieren und auf k begrenzen
            results.sort(key=lambda x: x['similarity'], reverse=True)
            return results[:k]
            
        except Exception as e:
            print(f"❌ Fehler bei semantischer Suche: {e}")
            return []
    
    async def find_similar_profiles(self, username: str, k: int = 3) -> List[Dict[str, Any]]:
        """Findet ähnliche Profile zu einem Benutzer"""
        try:
            # Archetypen des Benutzers als Query verwenden
            profile_data = self.load_profile(username)
            if not profile_data:
                return []
            
            archetypes = profile_data.get('archetypes', [])[:2]  # Top 2 Archetypen
            query = " ".join([f"{arch['name']} {arch['light']}" for arch in archetypes])
            
            # Suche durchführen (anderen Benutzer ausschließen)
            all_results = await self.semantic_search(query, k * 3)
            
            # Nach anderen Benutzern filtern
            other_users = {}
            for result in all_results:
                other_username = result.get('username')
                if other_username and other_username != username:
                    if other_username not in other_users:
                        other_users[other_username] = []
                    other_users[other_username].append(result)
            
            # Top-ähnliche Benutzer
            similar_users = []
            for other_username, user_results in other_users.items():
                avg_similarity = np.mean([r['similarity'] for r in user_results])
                similar_users.append({
                    'username': other_username,
                    'similarity': avg_similarity,
                    'matching_aspects': len(user_results)
                })
            
            similar_users.sort(key=lambda x: x['similarity'], reverse=True)
            return similar_users[:k]
            
        except Exception as e:
            print(f"❌ Fehler bei ähnlichen Profilen: {e}")
            return []
    
    async def update_embeddings(self, username: str) -> bool:
        """Aktualisiert Embeddings für einen Benutzer"""
        try:
            # Alte Embeddings entfernen
            self.remove_user_embeddings(username)
            
            # Neue Embeddings erstellen
            return await self.create_embeddings(username)
            
        except Exception as e:
            print(f"❌ Fehler beim Embedding-Update: {e}")
            return False
    
    def remove_user_embeddings(self, username: str):
        """Entfernt alle Embeddings eines Benutzers aus dem Index"""
        try:
            # IDs der zu entfernenden Embeddings finden
            ids_to_remove = []
            for vector_id, metadata in self.metadata.items():
                if metadata.get('username') == username:
                    ids_to_remove.append(vector_id)
            
            # Da FAISS keine direkten Löschungen unterstützt, Index neu aufbauen
            if ids_to_remove:
                self.rebuild_index_without_user(username)
                print(f"✅ {len(ids_to_remove)} Embeddings für {username} entfernt")
            
        except Exception as e:
            print(f"❌ Fehler beim Entfernen der Embeddings: {e}")
    
    def rebuild_index_without_user(self, username_to_remove: str):
        """Baut Index ohne einen bestimmten Benutzer neu auf"""
        try:
            # Alle Embeddings außer dem zu entfernenden Benutzer sammeln
            remaining_embeddings = []
            remaining_metadata = {}
            
            for vector_id, metadata in self.metadata.items():
                if metadata.get('username') != username_to_remove:
                    # Embedding aus Index extrahieren
                    embedding = self.index.reconstruct(vector_id)
                    remaining_embeddings.append(embedding)
                    remaining_metadata[len(remaining_embeddings) - 1] = metadata
            
            # Neuen Index erstellen
            self.create_new_index()
            
            if remaining_embeddings:
                embedding_matrix = np.array(remaining_embeddings, dtype=np.float32)
                self.index.add(embedding_matrix)
                self.metadata = remaining_metadata
            
        except Exception as e:
            print(f"❌ Fehler beim Index-Neuaufbau: {e}")
    
    def get_index_stats(self) -> Dict[str, Any]:
        """Liefert Statistiken über den Index"""
        try:
            total_vectors = self.index.ntotal if self.index else 0
            
            # Benutzer zählen
            users = set()
            types = {}
            
            for metadata in self.metadata.values():
                username = metadata.get('username')
                if username:
                    users.add(username)
                
                chunk_type = metadata.get('type', 'unknown')
                types[chunk_type] = types.get(chunk_type, 0) + 1
            
            return {
                'total_vectors': total_vectors,
                'total_users': len(users),
                'users': list(users),
                'chunk_types': types,
                'embedding_dimension': self.embedding_dim,
                'model': self.embedding_model
            }
            
        except Exception as e:
            print(f"❌ Fehler bei Index-Statistiken: {e}")
            return {}
    
    async def profile_query(self, username: str, query: str) -> List[Dict[str, Any]]:
        """Führt eine spezifische Suche im Profil eines Benutzers durch"""
        return await self.semantic_search(query, k=5, username_filter=username) 