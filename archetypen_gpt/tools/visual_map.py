"""
Visualisierungsmodul für Archetypen-GPT System
Erstellt interaktive Grafiken und Charts der Profile
"""

import json
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns

class VisualMapper:
    """Erstellt Visualisierungen für Archetypen-Profile"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.profiles_path = self.base_path / "profiles"
        
        # Farb-Schema für Archetypen
        self.archetype_colors = {
            "Held": "#FF6B35",
            "Weise": "#4A90E2", 
            "Unschuldiger": "#F5A623",
            "Forscher": "#7ED321",
            "Rebell": "#D0021B",
            "Magier": "#9013FE",
            "Jedermann": "#50E3C2",
            "Liebender": "#E91E63",
            "Narr": "#FF9500",
            "Fürsorger": "#8E44AD",
            "Herrscher": "#2C3E50",
            "Schöpfer": "#E67E22"
        }
        
        # Spiral Dynamics Farben
        self.spiral_colors = {
            "Beige": "#D2B48C",
            "Lila": "#8A2BE2",
            "Rot": "#DC143C",
            "Blau": "#4169E1",
            "Orange": "#FF8C00",
            "Grün": "#228B22",
            "Gelb": "#FFD700",
            "Türkis": "#40E0D0"
        }
    
    def create_visualization(self, username: str) -> bool:
        """Erstellt eine umfassende Visualisierung für einen Benutzer"""
        try:
            # Profil laden
            profile_data = self.load_profile(username)
            if not profile_data:
                print(f"❌ Profil für {username} nicht gefunden!")
                return False
            
            # Interaktive Plotly-Visualisierung erstellen
            fig = self.create_comprehensive_dashboard(username, profile_data)
            
            # HTML-Datei speichern
            output_path = self.base_path / f"visualization_{username}.html"
            fig.write_html(str(output_path))
            
            print(f"✅ Visualisierung erstellt: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Fehler bei Visualisierung: {e}")
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
    
    def create_comprehensive_dashboard(self, username: str, profile_data: Dict[str, Any]) -> go.Figure:
        """Erstellt ein umfassendes Dashboard"""
        
        # Subplots erstellen
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=(
                'Archetypen-Verteilung',
                'Spiral Dynamics Level',
                'Schatten-Profil',
                'Marker-Intensität',
                'Entwicklungsrichtung',
                'Integrations-Radar'
            ),
            specs=[
                [{"type": "bar"}, {"type": "pie"}],
                [{"type": "bar"}, {"type": "bar"}],
                [{"type": "scatter"}, {"type": "scatterpolar"}]
            ]
        )
        
        # 1. Archetypen-Balkendiagramm
        archetypes = profile_data.get('archetypes', [])
        if archetypes:
            names = [arch['name'] for arch in archetypes]
            scores = [arch['score'] for arch in archetypes]
            colors = [self.archetype_colors.get(name, '#888888') for name in names]
            
            fig.add_trace(
                go.Bar(
                    x=names,
                    y=scores,
                    marker_color=colors,
                    name="Archetypen",
                    text=[f"{score:.2f}" for score in scores],
                    textposition='auto'
                ),
                row=1, col=1
            )
        
        # 2. Spiral Dynamics Pie Chart
        spiral = profile_data.get('spiral_dynamics', {})
        if spiral:
            levels = [spiral.get('primary', 'Orange'), spiral.get('secondary', 'Grün')]
            values = [70, 30]  # Gewichtung
            pie_colors = [self.spiral_colors.get(level, '#888888') for level in levels]
            
            fig.add_trace(
                go.Pie(
                    labels=levels,
                    values=values,
                    marker_colors=pie_colors,
                    name="Spiral Dynamics"
                ),
                row=1, col=2
            )
        
        # 3. Schatten-Profil
        shadow = profile_data.get('shadow', {})
        if shadow:
            triggers = shadow.get('triggers', [])[:5]  # Top 5
            trigger_values = [1] * len(triggers)  # Gleiche Gewichtung
            
            fig.add_trace(
                go.Bar(
                    x=triggers,
                    y=trigger_values,
                    marker_color='#FF4444',
                    name="Schatten-Trigger"
                ),
                row=2, col=1
            )
        
        # 4. Marker-Intensität
        markers = profile_data.get('markers', [])[:6]  # Top 6
        if markers:
            marker_scores = np.random.uniform(0.6, 1.0, len(markers))  # Simulierte Intensität
            
            fig.add_trace(
                go.Bar(
                    x=markers,
                    y=marker_scores,
                    marker_color='#44AA44',
                    name="Marker-Intensität"
                ),
                row=2, col=2
            )
        
        # 5. Entwicklungsrichtung (Scatter)
        if spiral:
            levels_order = ["Beige", "Lila", "Rot", "Blau", "Orange", "Grün", "Gelb", "Türkis"]
            current_pos = levels_order.index(spiral.get('primary', 'Orange'))
            target_pos = levels_order.index(spiral.get('integration', 'Grün'))
            
            fig.add_trace(
                go.Scatter(
                    x=[current_pos, target_pos],
                    y=[1, 2],
                    mode='markers+lines+text',
                    marker=dict(size=[20, 15], color=['red', 'green']),
                    text=[spiral.get('primary', 'Orange'), spiral.get('integration', 'Grün')],
                    textposition="top center",
                    name="Entwicklung"
                ),
                row=3, col=1
            )
        
        # 6. Integrations-Radar
        if archetypes:
            categories = ['Bewusstsein', 'Integration', 'Authentizität', 'Beziehungen', 'Sinn', 'Wachstum']
            values = np.random.uniform(0.4, 0.9, len(categories))  # Simulierte Werte
            
            fig.add_trace(
                go.Scatterpolar(
                    r=values,
                    theta=categories,
                    fill='toself',
                    name='Integrations-Potential',
                    line_color='purple'
                ),
                row=3, col=2
            )
        
        # Layout anpassen
        fig.update_layout(
            height=1200,
            title_text=f"🧬 Archetypen-Profil Dashboard: {username}",
            title_x=0.5,
            showlegend=True,
            template="plotly_white"
        )
        
        return fig
    
    def create_archetype_radar(self, username: str) -> Optional[go.Figure]:
        """Erstellt ein Archetypen-Radar-Chart"""
        profile_data = self.load_profile(username)
        if not profile_data:
            return None
        
        archetypes = profile_data.get('archetypes', [])
        if not archetypes:
            return None
        
        # Radar-Chart Daten vorbereiten
        categories = []
        values = []
        
        for arch in archetypes[:6]:  # Max 6 Archetypen
            categories.append(arch['name'])
            values.append(arch['score'])
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Archetypen-Profil',
            line_color='rgb(255, 107, 53)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )),
            showlegend=True,
            title=f"🎭 Archetypen-Radar: {username}"
        )
        
        return fig
    
    def create_spiral_development_path(self, username: str) -> Optional[go.Figure]:
        """Erstellt eine Spiral Dynamics Entwicklungspfad-Visualisierung"""
        profile_data = self.load_profile(username)
        if not profile_data:
            return None
        
        spiral = profile_data.get('spiral_dynamics', {})
        levels_order = ["Beige", "Lila", "Rot", "Blau", "Orange", "Grün", "Gelb", "Türkis"]
        
        current = spiral.get('primary', 'Orange')
        target = spiral.get('integration', 'Grün')
        resistance = spiral.get('resistance', 'Blau')
        
        # Positionen bestimmen
        current_pos = levels_order.index(current) if current in levels_order else 4
        target_pos = levels_order.index(target) if target in levels_order else 5
        resistance_pos = levels_order.index(resistance) if resistance in levels_order else 3
        
        fig = go.Figure()
        
        # Entwicklungspfad
        fig.add_trace(go.Scatter(
            x=list(range(len(levels_order))),
            y=[1] * len(levels_order),
            mode='markers+text',
            marker=dict(
                size=[30 if i == current_pos else 20 if i == target_pos else 15 if i == resistance_pos else 10 
                      for i in range(len(levels_order))],
                color=[self.spiral_colors.get(level, '#888888') for level in levels_order],
                line=dict(width=2, color='white')
            ),
            text=levels_order,
            textposition="bottom center",
            name="Spiral Dynamics Level"
        ))
        
        # Entwicklungsrichtung zeigen
        fig.add_annotation(
            x=current_pos,
            y=1.2,
            text="AKTUELL",
            showarrow=True,
            arrowhead=2,
            arrowcolor="red"
        )
        
        fig.add_annotation(
            x=target_pos,
            y=1.2,
            text="ZIEL",
            showarrow=True,
            arrowhead=2,
            arrowcolor="green"
        )
        
        fig.add_annotation(
            x=resistance_pos,
            y=0.8,
            text="WIDERSTAND",
            showarrow=True,
            arrowhead=2,
            arrowcolor="orange"
        )
        
        fig.update_layout(
            title=f"🌈 Spiral Dynamics Entwicklungspfad: {username}",
            xaxis_title="Bewusstseinsebenen",
            yaxis_title="Entwicklung",
            showlegend=False,
            height=400
        )
        
        return fig
    
    def create_shadow_integration_chart(self, username: str) -> Optional[go.Figure]:
        """Erstellt ein Schatten-Integrations-Chart"""
        profile_data = self.load_profile(username)
        if not profile_data:
            return None
        
        shadow = profile_data.get('shadow', {})
        
        # Schatten-Aspekte
        aspects = ['Vermeidung', 'Projektion', 'Kontrolle', 'Scham', 'Sabotage']
        
        # Simulierte Werte basierend auf Profil
        primary_pattern = shadow.get('pattern', 'Vermeidung')
        values = []
        
        for aspect in aspects:
            if aspect == primary_pattern:
                values.append(0.8)  # Hauptmuster hoch
            else:
                values.append(np.random.uniform(0.2, 0.6))  # Andere niedriger
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=aspects,
            y=values,
            marker_color=['#FF4444' if asp == primary_pattern else '#FFAAAA' for asp in aspects],
            text=[f"{val:.1f}" for val in values],
            textposition='auto'
        ))
        
        fig.update_layout(
            title=f"🌑 Schatten-Muster Profil: {username}",
            xaxis_title="Schatten-Aspekte",
            yaxis_title="Intensität",
            yaxis=dict(range=[0, 1])
        )
        
        return fig
    
    def create_integration_matrix(self, username: str) -> Optional[go.Figure]:
        """Erstellt eine Integrations-Matrix"""
        profile_data = self.load_profile(username)
        if not profile_data:
            return None
        
        archetypes = profile_data.get('archetypes', [])[:3]  # Top 3
        
        if len(archetypes) < 2:
            return None
        
        # Matrix-Daten vorbereiten
        matrix_size = 3
        integration_matrix = np.random.uniform(0.3, 0.8, (matrix_size, matrix_size))
        
        # Diagonale auf 1 setzen (Selbst-Integration)
        np.fill_diagonal(integration_matrix, 1.0)
        
        arch_names = [arch['name'] for arch in archetypes]
        
        fig = go.Figure(data=go.Heatmap(
            z=integration_matrix,
            x=arch_names,
            y=arch_names,
            colorscale='RdYlGn',
            text=np.round(integration_matrix, 2),
            texttemplate="%{text}",
            textfont={"size": 12}
        ))
        
        fig.update_layout(
            title=f"🔮 Archetypen-Integrations-Matrix: {username}",
            width=500,
            height=500
        )
        
        return fig
    
    def export_all_visualizations(self, username: str) -> bool:
        """Exportiert alle Visualisierungen für einen Benutzer"""
        try:
            viz_dir = self.base_path / f"visualizations_{username}"
            viz_dir.mkdir(exist_ok=True)
            
            # Dashboard
            dashboard = self.create_comprehensive_dashboard(username, self.load_profile(username))
            if dashboard:
                dashboard.write_html(str(viz_dir / "dashboard.html"))
            
            # Radar Chart
            radar = self.create_archetype_radar(username)
            if radar:
                radar.write_html(str(viz_dir / "archetypen_radar.html"))
            
            # Spiral Path
            spiral_path = self.create_spiral_development_path(username)
            if spiral_path:
                spiral_path.write_html(str(viz_dir / "spiral_development.html"))
            
            # Shadow Chart
            shadow_chart = self.create_shadow_integration_chart(username)
            if shadow_chart:
                shadow_chart.write_html(str(viz_dir / "shadow_integration.html"))
            
            # Integration Matrix
            matrix = self.create_integration_matrix(username)
            if matrix:
                matrix.write_html(str(viz_dir / "integration_matrix.html"))
            
            print(f"✅ Alle Visualisierungen exportiert: {viz_dir}")
            return True
            
        except Exception as e:
            print(f"❌ Fehler beim Export: {e}")
            return False 