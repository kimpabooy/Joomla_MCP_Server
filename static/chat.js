// --- Dynamiskt hämta endpoints och rendera i listan ---
fetch('/help')
    .then(resp => resp.json())
    .then(data => {
        const list = document.getElementById('endpoints-list');
        list.innerHTML = '';
        if (data.endpoints && data.endpoints.length > 0) {
            data.endpoints.forEach(ep => {
                if (ep.path !== "/mcp-proxy" && ep.path !== "/endpoints" && ep.path !== "/help") {
                    const li = document.createElement('li');
                    li.textContent = ep.path;
                    list.appendChild(li);
                }
            });
        } else {
            list.innerHTML = '<li>Inga endpoints hittades</li>';
        }
    })
    .catch(() => {
        const list = document.getElementById('endpoints-list');
        list.innerHTML = '<li>Kunde inte hämta endpoints</li>';
    });

// --- Hantera Enter-tangenten i textarean ---
const textarea = document.getElementById('endpointInput');
textarea.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        document.getElementById('chatForm').dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
    }
});

// --- Hantera formulärets submit-event ---
document.getElementById('chatForm').onsubmit = async function (e) {
    e.preventDefault();
    let endpoint = textarea.value.trim();
    if (!endpoint) return;
    let chatlog = document.getElementById('chatlog');
    let responseBox = document.getElementById('endpoint-response');

    // --- Om användaren skriver /clear eller clear, rensa chatten ---
    if (endpoint === '/clear' || endpoint === 'clear') {
        chatlog.innerHTML = '<div class="chat-msg bot">Skriv in en <b>Endpoint</b> och tryck <b>Enter</b></div>';
        responseBox.innerHTML = '';
        textarea.value = '';
        textarea.focus();
        return;
    }

    // --- Lägg till användarens meddelande i chatten ---
    if (!endpoint.startsWith('/')) endpoint = '/' + endpoint;
    let userMsg = document.createElement('div');
    userMsg.className = 'chat-msg user';
    userMsg.textContent = textarea.value;
    chatlog.appendChild(userMsg);

    // --- Automatiskt skicka via /mcp-proxy ---
    const proxyEndpoint = `/mcp-proxy?endpoint=${encodeURIComponent(endpoint)}`;

    // --- Visar en laddningsindikator om endpointet tar tid att svara ---
    responseBox.innerHTML = '<span style="color:#b3e5ff;">Laddar...</span>';
    textarea.value = '';
    textarea.focus();
    try {
        // --- Skicka en förfrågan till proxy-endpointen ---
        const resp = await fetch(proxyEndpoint);
        if (resp.ok) {
            const data = await resp.json();
            responseBox.innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
        } else {
            let botMsg = document.createElement('div');
            botMsg.className = 'chat-msg bot';
            botMsg.innerHTML = 'Endpoint <b>' + endpoint + '</b> finns inte (HTTP ' + resp.status + '). Prova igen:';
            chatlog.appendChild(botMsg);
            chatlog.scrollTop = chatlog.scrollHeight;
        }
    } catch (err) {
        let botMsg = document.createElement('div');
        botMsg.className = 'chat-msg bot';
        botMsg.textContent = 'Fel vid kontroll av endpoint. Prova igen:';
        chatlog.appendChild(botMsg);
        chatlog.scrollTop = chatlog.scrollHeight;
    }
};
