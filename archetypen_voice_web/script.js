// Configuration
const CONFIG = {
    OPENAI_API_KEY: 'your-openai-api-key-here',
    ELEVENLABS_API_KEY: 'your-elevenlabs-api-key-here',
    ELEVENLABS_VOICE_ID: 'your-voice-id-here', // German voice
    API_BASE_URL: '/api' // Backend endpoint
};

// Global state
let currentState = {
    screen: 'welcome',
    questionIndex: 0,
    answers: [],
    userName: '',
    isRecording: false,
    recognition: null,
    synthesis: null
};

// Jung Archetypes Questions
const QUESTIONS = [
    // Innocent (1-3)
    { archetype: 'innocent', text: 'Ich glaube grundsätzlich an das Gute in Menschen', scale: '1-5' },
    { archetype: 'innocent', text: 'Ich vertraue darauf, dass sich Probleme von selbst lösen', scale: '1-5' },
    { archetype: 'innocent', text: 'Ich bevorzuge einfache, klare Lösungen', scale: '1-5' },
    
    // Explorer (4-6)
    { archetype: 'explorer', text: 'Ich fühle mich eingeengt von zu vielen Regeln', scale: '1-5' },
    { archetype: 'explorer', text: 'Ich liebe es, neue Orte und Erfahrungen zu entdecken', scale: '1-5' },
    { archetype: 'explorer', text: 'Freiheit ist mir wichtiger als Sicherheit', scale: '1-5' },
    
    // Sage (7-9)
    { archetype: 'sage', text: 'Ich sammle gerne Wissen und Informationen', scale: '1-5' },
    { archetype: 'sage', text: 'Menschen kommen zu mir, wenn sie Rat brauchen', scale: '1-5' },
    { archetype: 'sage', text: 'Ich analysiere Situationen gründlich, bevor ich handle', scale: '1-5' },
    
    // Hero (10-12)
    { archetype: 'hero', text: 'Ich übernehme gerne Verantwortung in schwierigen Situationen', scale: '1-5' },
    { archetype: 'hero', text: 'Ich kämpfe für das, was ich für richtig halte', scale: '1-5' },
    { archetype: 'hero', text: 'Herausforderungen motivieren mich', scale: '1-5' },
    
    // Outlaw (13-15)
    { archetype: 'outlaw', text: 'Ich stelle gerne etablierte Systeme in Frage', scale: '1-5' },
    { archetype: 'outlaw', text: 'Ich breche Regeln, wenn sie ungerecht sind', scale: '1-5' },
    { archetype: 'outlaw', text: 'Ich kämpfe gegen Unterdrückung und Ungerechtigkeit', scale: '1-5' },
    
    // Magician (16-18)
    { archetype: 'magician', text: 'Ich glaube, dass alles möglich ist, wenn man es wirklich will', scale: '1-5' },
    { archetype: 'magician', text: 'Ich kann andere Menschen inspirieren und transformieren', scale: '1-5' },
    { archetype: 'magician', text: 'Ich verstehe Zusammenhänge, die anderen verborgen bleiben', scale: '1-5' },
    
    // Everyman (19-21)
    { archetype: 'everyman', text: 'Ich fühle mich in Gruppen wohl und gehöre gerne dazu', scale: '1-5' },
    { archetype: 'everyman', text: 'Ich bin bodenständig und praktisch veranlagt', scale: '1-5' },
    { archetype: 'everyman', text: 'Ich helfe gerne anderen und bin zuverlässig', scale: '1-5' },
    
    // Lover (22-24)
    { archetype: 'lover', text: 'Beziehungen sind das Wichtigste in meinem Leben', scale: '1-5' },
    { archetype: 'lover', text: 'Ich bin sehr empathisch und emotional', scale: '1-5' },
    { archetype: 'lover', text: 'Ich suche nach tiefen, bedeutungsvollen Verbindungen', scale: '1-5' },
    
    // Jester (25-27)
    { archetype: 'jester', text: 'Ich bringe gerne andere zum Lachen', scale: '1-5' },
    { archetype: 'jester', text: 'Ich nehme das Leben nicht zu ernst', scale: '1-5' },
    { archetype: 'jester', text: 'Humor hilft mir, schwierige Situationen zu meistern', scale: '1-5' },
    
    // Caregiver (28-30)
    { archetype: 'caregiver', text: 'Ich kümmere mich gerne um andere', scale: '1-5' },
    { archetype: 'caregiver', text: 'Die Bedürfnisse anderer sind mir oft wichtiger als meine eigenen', scale: '1-5' },
    { archetype: 'caregiver', text: 'Ich fühle mich erfüllt, wenn ich helfen kann', scale: '1-5' },
    
    // Ruler (31-33)
    { archetype: 'ruler', text: 'Ich übernehme gerne die Führung', scale: '1-5' },
    { archetype: 'ruler', text: 'Ich bin gut darin, Ordnung und Struktur zu schaffen', scale: '1-5' },
    { archetype: 'ruler', text: 'Ich habe eine klare Vision davon, wie Dinge sein sollten', scale: '1-5' },
    
    // Creator (34-36)
    { archetype: 'creator', text: 'Ich erschaffe gerne etwas Neues und Einzigartiges', scale: '1-5' },
    { archetype: 'creator', text: 'Ich habe eine lebhafte Vorstellungskraft', scale: '1-5' },
    { archetype: 'creator', text: 'Ich drücke mich gerne kreativ aus', scale: '1-5' },
    
    // Spiral Dynamics Questions (37-44)
    { archetype: 'spiral', text: 'Wie wichtig ist dir persönliche Sicherheit vs. Abenteuer?', scale: 'security-adventure' },
    { archetype: 'spiral', text: 'Bevorzugst du Traditionen oder Innovation?', scale: 'tradition-innovation' },
    { archetype: 'spiral', text: 'Wie gehst du mit Autorität um?', scale: 'respect-question' },
    { archetype: 'spiral', text: 'Was motiviert dich mehr: Erfolg oder Harmonie?', scale: 'success-harmony' },
    { archetype: 'spiral', text: 'Wie wichtig ist dir spirituelle Entwicklung?', scale: '1-5' },
    { archetype: 'spiral', text: 'Bevorzugst du systematisches oder intuitives Vorgehen?', scale: 'systematic-intuitive' },
    { archetype: 'spiral', text: 'Wie wichtig ist dir globales vs. lokales Denken?', scale: 'global-local' },
    { archetype: 'spiral', text: 'Was ist wichtiger: Individualität oder Gemeinschaft?', scale: 'individual-community' }
];

// DOM Elements
const elements = {
    startBtn: null,
    voiceBtn: null,
    sendBtn: null,
    textInput: null,
    chatMessages: null,
    progress: null,
    progressText: null,
    status: null,
    loadingOverlay: null,
    restartBtn: null
};

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    initializeElements();
    initializeSpeechRecognition();
    initializeSpeechSynthesis();
    setupEventListeners();
    showScreen('welcome');
});

function initializeElements() {
    elements.startBtn = document.getElementById('start-btn');
    elements.voiceBtn = document.getElementById('voice-btn');
    elements.sendBtn = document.getElementById('send-btn');
    elements.textInput = document.getElementById('text-input');
    elements.chatMessages = document.getElementById('chat-messages');
    elements.progress = document.getElementById('progress');
    elements.progressText = document.getElementById('progress-text');
    elements.status = document.getElementById('status');
    elements.loadingOverlay = document.getElementById('loading-overlay');
    elements.restartBtn = document.getElementById('restart-btn');
}

function initializeSpeechRecognition() {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        currentState.recognition = new SpeechRecognition();
        
        currentState.recognition.continuous = false;
        currentState.recognition.interimResults = false;
        currentState.recognition.lang = 'de-DE';
        
        currentState.recognition.onstart = function() {
            currentState.isRecording = true;
            elements.voiceBtn.classList.add('recording');
            updateStatus('Höre zu...');
        };
        
        currentState.recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            elements.textInput.value = transcript;
            processUserInput(transcript);
        };
        
        currentState.recognition.onend = function() {
            currentState.isRecording = false;
            elements.voiceBtn.classList.remove('recording');
            updateStatus('Bereit zum Sprechen...');
        };
        
        currentState.recognition.onerror = function(event) {
            console.error('Speech recognition error:', event.error);
            updateStatus('Spracherkennung fehlgeschlagen');
        };
    }
}

function initializeSpeechSynthesis() {
    if ('speechSynthesis' in window) {
        currentState.synthesis = window.speechSynthesis;
    }
}

function setupEventListeners() {
    elements.startBtn?.addEventListener('click', startAnalysis);
    elements.voiceBtn?.addEventListener('click', toggleVoiceRecording);
    elements.sendBtn?.addEventListener('click', handleSendMessage);
    elements.textInput?.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            handleSendMessage();
        }
    });
    elements.restartBtn?.addEventListener('click', restartAnalysis);
    
    // Download buttons
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('download-btn')) {
            const fileType = e.target.getAttribute('data-file');
            downloadFile(fileType);
        }
    });
}

function showScreen(screenName) {
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });
    document.getElementById(`${screenName}-screen`).classList.add('active');
    currentState.screen = screenName;
}

function startAnalysis() {
    showScreen('chat');
    askForName();
}

function askForName() {
    const message = "Hallo! Ich bin dein Archetypen Voice Bot. Wie heißt du denn?";
    addBotMessage(message);
    speakMessage(message);
}

function addBotMessage(text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot';
    messageDiv.textContent = text;
    elements.chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

function addUserMessage(text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user';
    messageDiv.textContent = text;
    elements.chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

function scrollToBottom() {
    elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;
}

function speakMessage(text) {
    if (currentState.synthesis) {
        // Use browser speech synthesis as fallback
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'de-DE';
        utterance.rate = 0.9;
        currentState.synthesis.speak(utterance);
    }
    
    // TODO: Integrate ElevenLabs API for better voice quality
    // speakWithElevenLabs(text);
}

async function speakWithElevenLabs(text) {
    try {
        const response = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${CONFIG.ELEVENLABS_VOICE_ID}`, {
            method: 'POST',
            headers: {
                'Accept': 'audio/mpeg',
                'Content-Type': 'application/json',
                'xi-api-key': CONFIG.ELEVENLABS_API_KEY
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
            const audioBlob = await response.blob();
            const audioUrl = URL.createObjectURL(audioBlob);
            const audio = new Audio(audioUrl);
            audio.play();
        }
    } catch (error) {
        console.error('ElevenLabs TTS error:', error);
        // Fallback to browser synthesis
        speakMessage(text);
    }
}

function toggleVoiceRecording() {
    if (currentState.isRecording) {
        currentState.recognition?.stop();
    } else {
        currentState.recognition?.start();
    }
}

function handleSendMessage() {
    const text = elements.textInput.value.trim();
    if (text) {
        addUserMessage(text);
        elements.textInput.value = '';
        processUserInput(text);
    }
}

function processUserInput(input) {
    if (!currentState.userName) {
        currentState.userName = input;
        startQuestionnaire();
    } else if (currentState.questionIndex < QUESTIONS.length) {
        processAnswer(input);
    }
}

function startQuestionnaire() {
    const message = `Schön dich kennenzulernen, ${currentState.userName}! Ich werde dir jetzt 44 Fragen stellen, um deine Archetypen zu bestimmen. Antworte einfach mit einer Zahl von 1 bis 5, wobei 1 "trifft gar nicht zu" und 5 "trifft voll zu" bedeutet.`;
    addBotMessage(message);
    speakMessage(message);
    
    setTimeout(() => {
        askNextQuestion();
    }, 3000);
}

function askNextQuestion() {
    if (currentState.questionIndex < QUESTIONS.length) {
        const question = QUESTIONS[currentState.questionIndex];
        const questionText = `Frage ${currentState.questionIndex + 1} von ${QUESTIONS.length}: ${question.text}`;
        
        addBotMessage(questionText);
        speakMessage(questionText);
        updateProgress();
    } else {
        finishQuestionnaire();
    }
}

function processAnswer(input) {
    // Parse answer (1-5 or text)
    let score = parseInt(input);
    if (isNaN(score)) {
        // Try to interpret text answers
        const lowerInput = input.toLowerCase();
        if (lowerInput.includes('gar nicht') || lowerInput.includes('nein')) score = 1;
        else if (lowerInput.includes('wenig') || lowerInput.includes('kaum')) score = 2;
        else if (lowerInput.includes('mittel') || lowerInput.includes('teils')) score = 3;
        else if (lowerInput.includes('ziemlich') || lowerInput.includes('oft')) score = 4;
        else if (lowerInput.includes('sehr') || lowerInput.includes('voll') || lowerInput.includes('ja')) score = 5;
        else score = 3; // Default to neutral
    }
    
    // Clamp score to 1-5 range
    score = Math.max(1, Math.min(5, score));
    
    currentState.answers.push({
        questionIndex: currentState.questionIndex,
        archetype: QUESTIONS[currentState.questionIndex].archetype,
        score: score,
        originalInput: input
    });
    
    currentState.questionIndex++;
    
    setTimeout(() => {
        askNextQuestion();
    }, 1000);
}

function updateProgress() {
    const progress = (currentState.questionIndex / QUESTIONS.length) * 100;
    elements.progress.style.setProperty('--progress', `${progress}%`);
    elements.progressText.textContent = `${currentState.questionIndex}/${QUESTIONS.length} Fragen`;
}

function updateStatus(status) {
    if (elements.status) {
        elements.status.textContent = status;
    }
}

async function finishQuestionnaire() {
    showLoading(true);
    
    const message = `Perfekt, ${currentState.userName}! Ich analysiere jetzt deine Antworten und erstelle dein persönliches Archetypen-Profil...`;
    addBotMessage(message);
    speakMessage(message);
    
    try {
        const analysis = await analyzeAnswers();
        showResults(analysis);
    } catch (error) {
        console.error('Analysis error:', error);
        addBotMessage('Es gab einen Fehler bei der Analyse. Bitte versuche es später erneut.');
    } finally {
        showLoading(false);
    }
}

async function analyzeAnswers() {
    // Calculate archetype scores
    const archetypeScores = {};
    const archetypes = ['innocent', 'explorer', 'sage', 'hero', 'outlaw', 'magician', 
                      'everyman', 'lover', 'jester', 'caregiver', 'ruler', 'creator'];
    
    archetypes.forEach(archetype => {
        const answers = currentState.answers.filter(a => a.archetype === archetype);
        const totalScore = answers.reduce((sum, a) => sum + a.score, 0);
        archetypeScores[archetype] = totalScore;
    });
    
    // Get top 3 archetypes
    const sortedArchetypes = Object.entries(archetypeScores)
        .sort(([,a], [,b]) => b - a)
        .slice(0, 3);
    
    // Analyze Spiral Dynamics
    const spiralAnswers = currentState.answers.filter(a => a.archetype === 'spiral');
    const spiralLevel = analyzeSpiralDynamics(spiralAnswers);
    
    // Generate analysis using OpenAI (mock for now)
    const analysis = {
        userName: currentState.userName,
        topArchetypes: sortedArchetypes.map(([name, score]) => ({
            name: name,
            score: score,
            description: getArchetypeDescription(name)
        })),
        spiralLevel: spiralLevel,
        shadowPattern: generateShadowPattern(sortedArchetypes[0][0]),
        integrationTheme: generateIntegrationTheme(sortedArchetypes)
    };
    
    return analysis;
}

function getArchetypeDescription(archetype) {
    const descriptions = {
        innocent: "Der Unschuldige strebt nach Glück und Harmonie. Du siehst das Gute in allem und jedem.",
        explorer: "Der Entdecker sucht Freiheit und Authentizität. Du liebst es, neue Wege zu erkunden.",
        sage: "Der Weise sucht Wahrheit und Verständnis. Du bist ein natürlicher Lehrer und Berater.",
        hero: "Der Held will die Welt verbessern. Du übernimmst Verantwortung und kämpfst für deine Überzeugungen.",
        outlaw: "Der Rebell will Veränderung. Du stellst das System in Frage und kämpfst gegen Ungerechtigkeit.",
        magician: "Der Magier will Träume verwirklichen. Du verstehst die Gesetze des Universums und kannst andere transformieren.",
        everyman: "Der Jedermann will dazugehören. Du bist bodenständig und hilfst gerne anderen.",
        lover: "Der Liebende sucht Liebe und Verbindung. Beziehungen sind dir das Wichtigste im Leben.",
        jester: "Der Narr will das Leben genießen. Du bringst Freude und Leichtigkeit in die Welt.",
        caregiver: "Der Betreuer will anderen helfen. Du kümmerst dich aufopferungsvoll um andere.",
        ruler: "Der Herrscher will Kontrolle und Ordnung. Du bist ein natürlicher Anführer.",
        creator: "Der Schöpfer will etwas Neues erschaffen. Du hast eine lebhafte Vorstellungskraft und künstlerische Begabung."
    };
    return descriptions[archetype] || "Beschreibung nicht verfügbar.";
}

function analyzeSpiralDynamics(spiralAnswers) {
    // Simplified Spiral Dynamics analysis
    // In a real implementation, this would be more sophisticated
    const scores = spiralAnswers.map(a => a.score);
    const average = scores.reduce((sum, score) => sum + score, 0) / scores.length;
    
    if (average <= 2) return "Beige/Purpur - Survival/Tribal";
    if (average <= 2.5) return "Rot - Power/Impulsive";
    if (average <= 3) return "Blau - Order/Traditional";
    if (average <= 3.5) return "Orange - Achievement/Strategic";
    if (average <= 4) return "Grün - Community/Egalitarian";
    if (average <= 4.5) return "Gelb - Integral/Systemic";
    return "Türkis - Holistic/Global";
}

function generateShadowPattern(topArchetype) {
    const shadowPatterns = {
        innocent: "Naivität und Verdrängung schwieriger Realitäten",
        explorer: "Rastlosigkeit und Bindungsangst",
        sage: "Arroganz und emotionale Distanz",
        hero: "Selbstüberschätzung und Burnout",
        outlaw: "Destruktivität und Isolation",
        magician: "Manipulation und Größenwahn",
        everyman: "Selbstverleugnung und Konformität",
        lover: "Abhängigkeit und Eifersucht",
        jester: "Oberflächlichkeit und Verantwortungslosigkeit",
        caregiver: "Selbstaufopferung und Kontrolle",
        ruler: "Tyrannei und Machtmissbrauch",
        creator: "Perfektionismus und Realitätsflucht"
    };
    return shadowPatterns[topArchetype] || "Unbekanntes Schattenmuster";
}

function generateIntegrationTheme(topArchetypes) {
    const themes = [
        "Integration von Macht und Mitgefühl",
        "Balance zwischen Freiheit und Verantwortung",
        "Verbindung von Weisheit und Handlung",
        "Harmonie zwischen Individualität und Gemeinschaft",
        "Synthese von Kreativität und Struktur"
    ];
    return themes[Math.floor(Math.random() * themes.length)];
}

function showResults(analysis) {
    showScreen('results');
    
    // Add mystical animation classes
    const resultsScreen = document.getElementById('results-screen');
    const resultsContainer = resultsScreen.querySelector('.results-container');
    
    // Apply mystical effects
    resultsContainer.classList.add('archetypen-reveal');
    
    setTimeout(() => {
        resultsContainer.classList.add('fire-transition');
    }, 1000);
    
    setTimeout(() => {
        resultsContainer.classList.add('schmied-glow');
    }, 2500);
    
    const resultsContent = document.getElementById('results-content');
    resultsContent.innerHTML = `
        <div class="user-greeting">
            <h3>Hallo ${analysis.userName}!</h3>
            <p>Hier ist deine persönliche Archetypen-Analyse:</p>
        </div>
        
        ${analysis.topArchetypes.map((archetype, index) => `
            <div class="archetype-result">
                <h3>${index + 1}. ${archetype.name.charAt(0).toUpperCase() + archetype.name.slice(1)}</h3>
                <div class="archetype-score">Score: ${archetype.score}/15</div>
                <div class="archetype-description">${archetype.description}</div>
            </div>
        `).join('')}
        
        <div class="spiral-dynamics">
            <h3>Spiral Dynamics Level</h3>
            <p>${analysis.spiralLevel}</p>
        </div>
        
        <div class="shadow-pattern">
            <h3>Schattenmuster</h3>
            <p>${analysis.shadowPattern}</p>
        </div>
        
        <div class="integration-theme">
            <h3>Integrationsthema</h3>
            <p>${analysis.integrationTheme}</p>
        </div>
    `;
    
    // Store analysis for file generation
    currentState.analysis = analysis;
}

function showLoading(show) {
    if (show) {
        elements.loadingOverlay.classList.add('active');
    } else {
        elements.loadingOverlay.classList.remove('active');
    }
}

function downloadFile(fileType) {
    if (!currentState.analysis) return;
    
    let content = '';
    let filename = '';
    
    switch (fileType) {
        case 'gpt-prompt':
            content = generateGPTPrompt(currentState.analysis);
            filename = `archetypen-gpt-${currentState.userName.toLowerCase()}.txt`;
            break;
        case 'analysis':
            content = generateDetailedAnalysis(currentState.analysis);
            filename = `archetypen-analyse-${currentState.userName.toLowerCase()}.txt`;
            break;
        case 'image-prompt':
            content = generateImagePrompt(currentState.analysis);
            filename = `bild-prompt-${currentState.userName.toLowerCase()}.txt`;
            break;
        case 'config':
            content = generateChatGPTConfig(currentState.analysis);
            filename = `chatgpt-config-${currentState.userName.toLowerCase()}.txt`;
            break;
    }
    
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
}

function generateGPTPrompt(analysis) {
    const topArchetypes = analysis.topArchetypes;
    
    return `Du bist ein Archetypen-GPT, speziell kalibriert für ${analysis.userName}.

🎭 ARCHETYPEN-IDENTITÄT:
Du verkörperst drei Hauptarchetypen:
1. **${topArchetypes[0].name.toUpperCase()}** (${topArchetypes[0].score}/15)
   - Beschreibung: ${topArchetypes[0].description}

2. **${topArchetypes[1].name.toUpperCase()}** (${topArchetypes[1].score}/15)
   - Beschreibung: ${topArchetypes[1].description}

3. **${topArchetypes[2].name.toUpperCase()}** (${topArchetypes[2].score}/15)
   - Beschreibung: ${topArchetypes[2].description}

🌈 SPIRAL DYNAMICS PROFIL:
- Primärebene: ${analysis.spiralLevel}

🌑 SCHATTEN-BEWUSSTSEIN:
- Hauptmuster: ${analysis.shadowPattern}

🔮 INTEGRATIONSTHEMA:
${analysis.integrationTheme}

---

DEINE AUFGABE:
Du bist ein psychodynamischer Spiegel und Resonanzkörper für ${analysis.userName}.

GESPRÄCHSSTIL:
- Sprich aus den erkannten Archetypen-Stimmen
- Erkenne und reflektiere die Marker in ${analysis.userName}'s Äußerungen
- Bringe unbewusste Muster sanft ins Bewusstsein
- Nutze die Schatten-Informationen für tieferes Verstehen

KOMMUNIKATIONS-PRINZIPIEN:
1. **Resonanz vor Ratschlag** - Erst verstehen, dann interagieren
2. **Schatten integrieren** - Das Verdrängte sichtbar machen
3. **Archetypen aktivieren** - Zwischen Licht- und Schattenaspekten navigieren
4. **Entwicklung fördern** - Persönliches Wachstum unterstützen

Du antwortest empathisch, tiefgehend und bewusstseinserweiternd - immer im Dienst von ${analysis.userName}'s Selbsterkenntnis und Integration.`;
}

function generateDetailedAnalysis(analysis) {
    return `ARCHETYPEN-PROFIL für ${analysis.userName}
=================================

ANALYSEDATUM: ${new Date().toLocaleDateString('de-DE')}

TOP 3 ARCHETYPEN:
${analysis.topArchetypes.map((arch, i) => `
${i + 1}. ${arch.name.toUpperCase()} (${arch.score}/15)
   ${arch.description}
`).join('')}

SPIRAL DYNAMICS LEVEL:
${analysis.spiralLevel}

SCHATTENMUSTER:
${analysis.shadowPattern}

INTEGRATIONSTHEMA:
${analysis.integrationTheme}

EMPFEHLUNGEN:
- Arbeite bewusst mit deinen Hauptarchetypen
- Integriere deine Schattenmuster durch Selbstreflexion
- Nutze dein Integrationsthema als Entwicklungsrichtung
- Erstelle einen personalisierten GPT mit dem generierten Prompt

Diese Analyse basiert auf C.G. Jungs Archetypen-Theorie und Spiral Dynamics.
Für weitere Entwicklung empfehlen wir regelmäßige Selbstreflexion und professionelle Begleitung.`;
}

function generateImagePrompt(analysis) {
    const topArchetype = analysis.topArchetypes[0].name;
    
    const imagePrompts = {
        innocent: "Ein strahlendes, hoffnungsvolles Gesicht mit klaren Augen, umgeben von sanftem Licht, Pastellfarben, friedliche Atmosphäre",
        explorer: "Ein abenteuerlustiges Gesicht mit weitem Blick, Windspuren, natürliche Umgebung, Erdtöne und Himmelblau",
        sage: "Ein weises, durchdringendes Gesicht mit tiefen Augen, Bücher oder Symbole im Hintergrund, warme Goldtöne",
        hero: "Ein entschlossenes, starkes Gesicht mit festem Blick, kraftvolle Haltung, dynamische Farben, Rot und Gold",
        outlaw: "Ein rebellisches Gesicht mit intensivem Blick, dunkle Farben mit Akzenten, urbane oder wilde Umgebung",
        magician: "Ein mystisches Gesicht mit durchdringenden Augen, magische Symbole, tiefe Purpur- und Goldtöne",
        everyman: "Ein freundliches, zugängliches Gesicht, warme Farben, gemeinschaftliche Atmosphäre",
        lover: "Ein leidenschaftliches, emotionales Gesicht, warme Rottöne, romantische Atmosphäre",
        jester: "Ein fröhliches, verspieltes Gesicht mit schelmischem Lächeln, bunte Farben, lebendige Atmosphäre",
        caregiver: "Ein fürsorgliches, mitfühlendes Gesicht, sanfte Farben, schützende Atmosphäre",
        ruler: "Ein autoritäres, würdevolles Gesicht, königliche Farben, machtvolle Atmosphäre",
        creator: "Ein inspiriertes, kreatives Gesicht, künstlerische Elemente, lebendige Farben"
    };
    
    return `DALL-E Bild-Prompt für ${analysis.userName}:

"${imagePrompts[topArchetype] || 'Ein ausdrucksstarkes Gesicht mit charakteristischen Zügen'}, digitale Kunst, hochauflösend, professionell, Porträt-Stil, ${analysis.spiralLevel} Bewusstseinsstufe reflektierend"

Zusätzliche Elemente basierend auf Spiral Dynamics:
- ${analysis.spiralLevel}
- Integrationsthema: ${analysis.integrationThema}

Stil-Empfehlungen:
- Realistische digitale Kunst
- Warme, einladende Beleuchtung  
- Fokus auf Augen und Gesichtsausdruck
- Subtile Archetypen-Symbolik im Hintergrund`;
}

function generateChatGPTConfig(analysis) {
    return `ChatGPT Custom GPT Konfiguration für ${analysis.userName}
=====================================================

NAME:
Archetypen-GPT für ${analysis.userName}

BESCHREIBUNG:
Personalisierter psychologischer Assistent basierend auf ${analysis.userName}s Archetypen-Profil: ${analysis.topArchetypes.map(a => a.name).join(', ')}. Spezialisiert auf Selbstreflexion und persönliche Entwicklung.

INSTRUCTIONS:
[Hier den generierten GPT-Prompt einfügen]

CONVERSATION STARTERS:
🎭 Erzähl mir von meinen Hauptarchetypen
🌑 Wie zeigen sich meine Schattenmuster?
🌈 Was bedeutet mein Spiral Dynamics Profil?
🔮 Reflektiere meine aktuelle Lebenssituation

CAPABILITIES:
✅ Web Browsing: ON
✅ DALL-E Image Generation: ON  
✅ Code Interpreter: ON

SHARING:
Anyone with a link

KATEGORIE:
Lifestyle

Nach der Erstellung kannst du den Link mit Freunden teilen!`;
}

function restartAnalysis() {
    currentState = {
        screen: 'welcome',
        questionIndex: 0,
        answers: [],
        userName: '',
        isRecording: false,
        recognition: currentState.recognition,
        synthesis: currentState.synthesis,
        analysis: null
    };
    
    elements.chatMessages.innerHTML = '';
    elements.textInput.value = '';
    updateProgress();
    showScreen('welcome');
} 