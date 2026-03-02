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
            #chatbox { width: 400px; margin: 30px auto; padding: 20px; border: 1px solid #ccc; border-radius: 8px; background: #222; color: #eee; }
            #chatlog { min-height: 40px; margin-bottom: 10px; }
            #endpointInput { width: 80%; padding: 8px; }
            #goBtn { padding: 8px 16px; }
        </style>
    </head>
    <body style=\"background:#181818;color:#eee;font-family:sans-serif;\">
        <h1 style=\"text-align:center;\">Welcome to the MCP Server!</h1>
            <style>
            .chat-msg { margin: 8px 0; padding: 8px 12px; border-radius: 6px; max-width: 95%; word-break: break-word; }
            .chat-msg.user { background: #333; color: #fff; text-align: right; margin-left: 30px; }
            .chat-msg.bot { background: #222; color: #b3e5fc; text-align: left; margin-right: 30px; }
            .chat-msg pre { background: none; color: inherit; margin: 0; padding: 0; font-size: 0.95em; }
            </style>
            <div id="chatbox">
                <div id="chatlog">
                    <div class="chat-msg bot">Skriv in en endpoint ( <b>articles</b>, <b>add_article</b> ) och tryck Enter eller Go:</div>
                </div>
                <form id="chatForm" autocomplete="off">
                    <textarea id="endpointInput" placeholder="Skriv ett kommando..." rows="2" style="width: 100%; resize: vertical;" required></textarea>
                    <button id="goBtn" type="submit" style="display:none;">Go</button>
                </form>
            </div>
            <script>
            const textarea = document.getElementById('endpointInput');
            textarea.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    document.getElementById('chatForm').dispatchEvent(new Event('submit', {cancelable: true, bubbles: true}));
                }
            });

            document.getElementById('chatForm').onsubmit = async function(e) {
                e.preventDefault();
                let endpoint = textarea.value.trim();
                if (!endpoint) return;
                if (!endpoint.startsWith('/')) endpoint = '/' + endpoint;
                let chatlog = document.getElementById('chatlog');
                let userMsg = document.createElement('div');
                userMsg.className = 'chat-msg user';
                userMsg.textContent = textarea.value;
                chatlog.appendChild(userMsg);
                textarea.value = '';
                textarea.focus();
                try {
                    const resp = await fetch(endpoint, { method: 'GET' });
                    let botMsg = document.createElement('div');
                    botMsg.className = 'chat-msg bot';
                    if (resp.ok) {
                        const data = await resp.json();
                        botMsg.innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
                    } else {
                        botMsg.innerHTML = 'Endpoint <b>' + endpoint + '</b> finns inte (HTTP ' + resp.status + '). Prova igen:';
                    }
                    chatlog.appendChild(botMsg);
                    chatlog.scrollTop = chatlog.scrollHeight;
                } catch (err) {
                    let botMsg = document.createElement('div');
                    botMsg.className = 'chat-msg bot';
                    botMsg.textContent = 'Fel vid kontroll av endpoint. Prova igen:';
                    chatlog.appendChild(botMsg);
                    chatlog.scrollTop = chatlog.scrollHeight;
                }
                textarea.value = '';
                textarea.focus();
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
