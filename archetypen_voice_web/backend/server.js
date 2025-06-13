const express = require('express');
const cors = require('cors');
const path = require('path');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, '../')));

// Serve static files
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '../index.html'));
});

// API Routes
app.post('/api/analyze', async (req, res) => {
    try {
        const { answers, userName } = req.body;
        
        // Here you would integrate with OpenAI API for advanced analysis
        // For now, we'll use the client-side analysis
        
        res.json({
            success: true,
            message: 'Analysis completed',
            data: {
                userName,
                timestamp: new Date().toISOString()
            }
        });
    } catch (error) {
        console.error('Analysis error:', error);
        res.status(500).json({
            success: false,
            error: 'Analysis failed'
        });
    }
});

// ElevenLabs TTS Proxy (to avoid CORS issues)
app.post('/api/tts', async (req, res) => {
    try {
        const { text } = req.body;
        const ELEVENLABS_API_KEY = process.env.ELEVENLABS_API_KEY;
        const VOICE_ID = process.env.ELEVENLABS_VOICE_ID;
        
        if (!ELEVENLABS_API_KEY || !VOICE_ID) {
            return res.status(400).json({
                success: false,
                error: 'ElevenLabs API not configured'
            });
        }
        
        const response = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${VOICE_ID}`, {
            method: 'POST',
            headers: {
                'Accept': 'audio/mpeg',
                'Content-Type': 'application/json',
                'xi-api-key': ELEVENLABS_API_KEY
            },
            body: JSON.stringify({
                text: text,
                model_id: 'eleven_multilingual_v2',
                voice_settings: {
                    stability: 0.5,
                    similarity_boost: 0.5
                }
            })
        });
        
        if (response.ok) {
            const audioBuffer = await response.arrayBuffer();
            res.set({
                'Content-Type': 'audio/mpeg',
                'Content-Length': audioBuffer.byteLength
            });
            res.send(Buffer.from(audioBuffer));
        } else {
            throw new Error('ElevenLabs API error');
        }
    } catch (error) {
        console.error('TTS error:', error);
        res.status(500).json({
            success: false,
            error: 'TTS generation failed'
        });
    }
});

// OpenAI Integration for advanced analysis
app.post('/api/openai-analysis', async (req, res) => {
    try {
        const { answers, userName } = req.body;
        const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
        
        if (!OPENAI_API_KEY) {
            return res.status(400).json({
                success: false,
                error: 'OpenAI API not configured'
            });
        }
        
        // Prepare prompt for OpenAI
        const analysisPrompt = `
        Analysiere die folgenden Archetypen-Fragebogen-Antworten für ${userName}:
        
        ${answers.map((answer, index) => 
            `Frage ${index + 1}: ${answer.originalInput} (Score: ${answer.score})`
        ).join('\n')}
        
        Erstelle eine detaillierte psychologische Analyse basierend auf:
        1. Jung'schen Archetypen
        2. Spiral Dynamics
        3. Schattenmuster
        4. Integrationspotential
        
        Antworte im JSON-Format mit den Feldern: topArchetypes, spiralLevel, shadowPattern, integrationTheme, detailedAnalysis.
        `;
        
        const response = await fetch('https://api.openai.com/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${OPENAI_API_KEY}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                model: 'gpt-4',
                messages: [
                    {
                        role: 'system',
                        content: 'Du bist ein Experte für Jung\'sche Archetypen und Spiral Dynamics. Analysiere Persönlichkeitsprofile präzise und empathisch.'
                    },
                    {
                        role: 'user',
                        content: analysisPrompt
                    }
                ],
                temperature: 0.7,
                max_tokens: 2000
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            const analysis = JSON.parse(data.choices[0].message.content);
            
            res.json({
                success: true,
                analysis: {
                    ...analysis,
                    userName
                }
            });
        } else {
            throw new Error('OpenAI API error');
        }
    } catch (error) {
        console.error('OpenAI analysis error:', error);
        res.status(500).json({
            success: false,
            error: 'Advanced analysis failed'
        });
    }
});

// Health check
app.get('/api/health', (req, res) => {
    res.json({
        success: true,
        message: 'Archetypen Voice Bot API is running',
        timestamp: new Date().toISOString()
    });
});

app.listen(PORT, () => {
    console.log(`🎭 Archetypen Voice Bot Server running on port ${PORT}`);
    console.log(`🌐 Open http://localhost:${PORT} to start`);
}); 