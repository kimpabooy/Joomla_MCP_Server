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
        <div id=\"chatbox\">
            <div id=\"chatlog\">Type an endpoint ( <b>articles</b>, <b>add_article</b> ) and press Enter or Go:</div>
            <form id=\"chatForm\" autocomplete=\"off\">
                <input id=\"endpointInput\" type=\"text\" placeholder=\"Ange endpoint..\" autofocus required />
                <button id=\"goBtn\" type=\"submit\">Go</button>
            </form>
        </div>
        <script>
        document.getElementById('chatForm').onsubmit = async function(e) {
            e.preventDefault();
            let endpoint = document.getElementById('endpointInput').value.trim();
            if (!endpoint.startsWith('/')) endpoint = '/' + endpoint;
            try {
                const resp = await fetch(endpoint, { method: 'HEAD' });
                if (resp.ok) {
                    window.location.href = endpoint;
                } else if (resp.status === 405) {
                    const resp2 = await fetch(endpoint, { method: 'GET' });
                    if (resp2.ok) {
                        window.location.href = endpoint;
                    } else {
                        document.getElementById('chatlog').innerHTML =
                            'Endpoint <b>' + endpoint + '</b> finns inte (HTTP ' + resp2.status + '). Pröva igen:';
                    }
                } else {
                    document.getElementById('chatlog').innerHTML =
                        'Endpoint <b>' + endpoint + '</b> finns inte (HTTP ' + resp.status + '). Pröva igen:';
                }
            } catch (err) {
                document.getElementById('chatlog').innerHTML =
                    'Fel vid kontroll av endpoint. Pröva igen:';
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
