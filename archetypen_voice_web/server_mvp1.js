require('dotenv').config();
const express = require('express');
const cors = require('cors');
const compression = require('compression');
const helmet = require('helmet');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Security & Performance Middleware
app.use(helmet({
    contentSecurityPolicy: {
        directives: {
            defaultSrc: ["'self'"],
            scriptSrc: ["'self'", "'unsafe-inline'", "https://unpkg.com", "https://cdnjs.cloudflare.com"],
            styleSrc: ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com", "https://cdnjs.cloudflare.com"],
            fontSrc: ["'self'", "https://fonts.gstatic.com", "https://cdnjs.cloudflare.com"],
            imgSrc: ["'self'", "data:", "https:"],
            mediaSrc: ["'self'"],
            connectSrc: ["'self'", "https://api.elevenlabs.io", "wss://*.elevenlabs.io"],
            frameSrc: ["'self'", "https://elevenlabs.io"]
        }
    }
}));

app.use(compression());
app.use(cors());
app.use(express.json());

// Static Files
app.use(express.static(__dirname));

// Routes
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index_mvp1_enhanced.html'));
});

// Alternative simpler version
app.get('/simple', (req, res) => {
    res.sendFile(path.join(__dirname, 'index_mvp1.html'));
});

// Health Check
app.get('/health', (req, res) => {
    res.json({ 
        status: 'active',
        message: 'Archetypen-Schmied AIR-PI Interface operational',
        timestamp: new Date().toISOString()
    });
});

// Analytics Endpoint (for future use)
app.post('/api/analytics', (req, res) => {
    const { event, data } = req.body;
    console.log(`Analytics Event: ${event}`, data);
    res.json({ success: true });
});

// 404 Handler
app.use((req, res) => {
    res.status(404).send(`
        <!DOCTYPE html>
        <html>
        <head>
            <title>404 - Archetypen-Schmied</title>
            <style>
                body {
                    background: #000;
                    color: #fff;
                    font-family: 'Montserrat', sans-serif;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    height: 100vh;
                    margin: 0;
                    text-align: center;
                }
                h1 { color: #ff6b00; }
                a { color: #ff8c00; text-decoration: none; }
            </style>
        </head>
        <body>
            <div>
                <h1>404</h1>
                <p>Diese Seite wurde im Feuer der Transformation aufgelöst.</p>
                <a href="/">Zurück zur Schmiede</a>
            </div>
        </body>
        </html>
    `);
});

// Start Server
app.listen(PORT, () => {
    console.log(`
🔥 Archetypen-Schmied AIR-PI Interface
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Server läuft auf: http://localhost:${PORT}
Environment: ${process.env.NODE_ENV || 'development'}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    `);
});