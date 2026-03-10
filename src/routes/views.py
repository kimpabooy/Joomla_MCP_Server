from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def root():
    html_content = """
    <!DOCTYPE html>
    <html lang=\"en\">
    <head>
        <meta charset=\"UTF-8\">
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
        <title>MCP Server</title>
        <style>
            #chatbox { width: 400px; margin: 30px auto; padding: 20px; border: 1px solid #ccc; border-radius: 8px; background: #222; color: #eee; margin 50px auto; }
            #chatlog { min-height: 40px; margin: 10px; }
            #endpointInput { width: 80%; padding: 8px; border: 1px solid #555; border-radius: 4px; background: #333; color: #eee; margin-right: 16px; }
        </style>
    </head>
    
    <body style=\"background:#181818;color:#b3e5ff;font-family:sans-serif;\">
        <style>
            .chat-msg { margin: 8px 0; padding: 8px 12px; border-radius: 6px; max-width: 95%; word-break: break-word; }
            .chat-msg.user { background: #2660a5; color: #fff; text-align: right; margin-left: 30px; }
            .chat-msg.bot { background: #222; color: #b3e5ff; text-align: left; margin-right: 30px; }
            .chat-msg pre { background: none; color: inherit; margin: 0; padding: 0; font-size: 0.95em; }
            #main-flex { display: flex; flex-direction: row; justify-content: center; align-items: flex-start; }
            #chatbox { width: 400px; margin: 30px 30px 30px 0; padding: 20px; border: 1px solid #ccc; border-radius: 8px; background: #222; color: #eee; }
            #endpoints-box { min-width: 220px; max-width: 260px; margin: 30px 0 30px 0; padding: 20px; border: 1px solid #444; border-radius: 8px; background: #23272b; color: #b3e5ff; }
            #endpoints-box h3 { margin-top: 0; }
            #endpoints-list { list-style: none; padding-left: 0; }
            #endpoints-list li { margin-bottom: 8px; font-size: 1.08em; }
        </style>
        
        <h1 style=\"text-align:center;\">Welcome to the MCP Server!</h1>
        
        <div id="main-flex">
            <div id="response-box" style="min-width:260px;max-width:340px;margin:30px 30px 30px 0;padding:20px;border:1px solid #444;border-radius:8px;background:#23272b;color:#b3e5ff;min-height:200px;">
                <h3>Svar</h3>
                <div id="endpoint-response" style="white-space:pre-wrap;word-break:break-all;"></div>
            </div>
            
            <div id="chatbox">
                <div id="chatlog">
                    <div class="chat-msg bot">Skriv in en <b>Endpoint</b> och tryck <b>Enter</b></div>
                </div>
                <form id="chatForm" autocomplete="off">
                    <textarea id="endpointInput" placeholder="Skriv ett kommando..." rows="2" style="width: 95%; resize: vertical;" required></textarea>
                </form>
            </div>

            <div id="endpoints-box">
                <h3>Endpoints</h3>
                <ul id="endpoints-list">
                    <li>Laddar...</li>
                </ul>
                    <p> Extra: /clear, /help</p>
            </div>
        </div>

            <script>
            
            // --- Dynamiskt hämta endpoints och renderas i listan ---
            fetch('/help')
                .then(resp => resp.json())
                .then(data => {
                    const list = document.getElementById('endpoints-list');
                    list.innerHTML = '';
                    if (data.endpoints && data.endpoints.length > 0 ) {
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
            textarea.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    document.getElementById('chatForm').dispatchEvent(new Event('submit', {cancelable: true, bubbles: true}));
                }
            });

            // --- Hantera formulärets submit-event ---
            document.getElementById('chatForm').onsubmit = async function(e) {
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

                // --- Visar en laddnings indikator om endpointet tar tid att svara ---
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
            </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@router.get("/add_article", response_class=HTMLResponse)
def add_article_form():
    html_content = """
    <!DOCTYPE html>
    <html lang=\"en\">
    <head>
        <meta charset=\"UTF-8\">
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
        <title>Add Article</title>
    </head>
    <body>
        <h1>Add New Article</h1>
        <form id=\"articleForm\">
            <label for=\"title\">Title:</label><br>
            <input type=\"text\" id=\"title\" name=\"title\" required><br>
            <label for=\"content\">Content:</label><br>
            <textarea id=\"content\" name=\"content\" required></textarea><br><br>
            <button type=\"submit\">Add Article</button>
        </form>
        <div id=\"result\"></div>
        <script>
        document.getElementById('articleForm').onsubmit = async function(e) {
            e.preventDefault();
            const title = document.getElementById('title').value;
            const content = document.getElementById('content').value;
            const response = await fetch('/add_article', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({title, content })
            });
            const result = await response.json();
            document.getElementById('result').innerText = JSON.stringify(result, null, 2);
        };
        </script>
        <p><a href=\"/\">Back to Home</a></p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@router.get("/clear")
def clear_chat():
    return root()
