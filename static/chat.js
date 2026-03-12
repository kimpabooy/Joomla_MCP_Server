// --- Dynamiskt hämta MCP tools och rendera i listan ---
fetch('/help')
    .then(resp => resp.json())
    .then(data => {
        const list = document.getElementById('endpoints-list');
        list.innerHTML = '';
        if (data.tools && data.tools.length > 0) {
            data.tools.forEach(tool => {
                const li = document.createElement('li');
                li.textContent = `${tool.endpoint}`;
                list.appendChild(li);
            });
        } else {
            list.innerHTML = '<li>Inga tools hittades</li>';
        }
    })
    .catch(() => {
        const list = document.getElementById('endpoints-list');
        list.innerHTML = '<li>Kunde inte hämta tools</li>';
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

    // --- Om användaren skriver /articles/create utan parametrar, visa modal ---
    if (!endpoint.startsWith('/')) endpoint = '/' + endpoint;
    if (endpoint === '/articles/create') {
        textarea.value = '';
        showCreateModal(chatlog, responseBox);
        return;
    }

    // --- Om användaren skriver /articles/{id}/edit, visa edit-modal ---
    const editMatch = endpoint.match(/^\/articles(?:\/([\d]+))?\/edit$/);
    if (editMatch) {
        textarea.value = '';
        showEditModal(chatlog, responseBox, editMatch[1] || '');
        return;
    }

    // --- Om användaren skriver /articles/{id}/remove, visa bekräftelse ---
    const removeMatch = endpoint.match(/^\/articles\/(\d+)\/remove$/);
    if (removeMatch) {
        textarea.value = '';
        showConfirmRemoveModal(chatlog, responseBox, removeMatch[1]);
        return;
    }
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

// --- Modal för att bekräfta borttagning ---
function showConfirmRemoveModal(chatlog, responseBox, articleId) {
    const modal = document.getElementById('confirm-remove-modal');
    document.getElementById('confirm-remove-text').textContent =
        `Vill du verkligen ta bort artikel ${articleId} permanent? Detta går inte att ångra.`;
    modal.showModal();

    document.getElementById('confirm-remove-cancel').onclick = function () {
        modal.close();
        document.getElementById('endpointInput').focus();
    };

    document.getElementById('confirm-remove-yes').onclick = async function () {
        modal.close();

        let userMsg = document.createElement('div');
        userMsg.className = 'chat-msg user';
        userMsg.textContent = `/articles/${articleId}/remove`;
        chatlog.appendChild(userMsg);
        chatlog.scrollTop = chatlog.scrollHeight;

        const proxyEndpoint = `/mcp-proxy?endpoint=${encodeURIComponent(`/articles/${articleId}/remove`)}`;
        responseBox.innerHTML = '<span style="color:#b3e5ff;">Laddar...</span>';

        try {
            const resp = await fetch(proxyEndpoint);
            if (resp.ok) {
                const data = await resp.json();
                responseBox.innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
            } else {
                let botMsg = document.createElement('div');
                botMsg.className = 'chat-msg bot';
                botMsg.innerHTML = 'Kunde inte ta bort artikel (HTTP ' + resp.status + ')';
                chatlog.appendChild(botMsg);
            }
        } catch (err) {
            let botMsg = document.createElement('div');
            botMsg.className = 'chat-msg bot';
            botMsg.textContent = 'Fel vid borttagning av artikel. Prova igen.';
            chatlog.appendChild(botMsg);
        }
        chatlog.scrollTop = chatlog.scrollHeight;
        document.getElementById('endpointInput').focus();
    };
}

// --- Modal för att redigera artikel ---
function showEditModal(chatlog, responseBox, prefillId) {
    const modal = document.getElementById('edit-modal');
    const idInput = document.getElementById('edit-modal-id');
    const titleInput = document.getElementById('edit-modal-title');
    const contentInput = document.getElementById('edit-modal-content');
    idInput.value = prefillId || '';
    titleInput.value = '';
    contentInput.value = '';
    modal.showModal();
    if (prefillId) {
        titleInput.focus();
    } else {
        idInput.focus();
    }

    document.getElementById('edit-modal-cancel').onclick = function () {
        modal.close();
        document.getElementById('endpointInput').focus();
    };

    document.getElementById('edit-modal-submit').onclick = async function () {
        const articleId = idInput.value.trim();
        const title = titleInput.value.trim();
        const content = contentInput.value.trim();
        if (!articleId || !title || !content) return;
        modal.close();

        let userMsg = document.createElement('div');
        userMsg.className = 'chat-msg user';
        userMsg.textContent = `/articles/${articleId}/edit title:${title} content:${content}`;
        chatlog.appendChild(userMsg);
        chatlog.scrollTop = chatlog.scrollHeight;

        const endpoint = `/articles/${articleId}/edit title:${title} content:${content}`;
        const proxyEndpoint = `/mcp-proxy?endpoint=${encodeURIComponent(endpoint)}`;
        responseBox.innerHTML = '<span style="color:#b3e5ff;">Laddar...</span>';

        try {
            const resp = await fetch(proxyEndpoint);
            if (resp.ok) {
                const data = await resp.json();
                responseBox.innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
            } else {
                let botMsg = document.createElement('div');
                botMsg.className = 'chat-msg bot';
                botMsg.innerHTML = 'Kunde inte redigera artikel (HTTP ' + resp.status + ')';
                chatlog.appendChild(botMsg);
            }
        } catch (err) {
            let botMsg = document.createElement('div');
            botMsg.className = 'chat-msg bot';
            botMsg.textContent = 'Fel vid redigering av artikel. Prova igen.';
            chatlog.appendChild(botMsg);
        }
        chatlog.scrollTop = chatlog.scrollHeight;
        document.getElementById('endpointInput').focus();
    };
}

// --- Modal för att skapa artikel ---
function showCreateModal(chatlog, responseBox) {
    const modal = document.getElementById('create-modal');
    const titleInput = document.getElementById('modal-title');
    const contentInput = document.getElementById('modal-content');
    titleInput.value = '';
    contentInput.value = '';
    modal.showModal();
    titleInput.focus();

    document.getElementById('modal-cancel').onclick = function () {
        modal.close();
        document.getElementById('endpointInput').focus();
    };

    document.getElementById('modal-submit').onclick = async function () {
        const title = titleInput.value.trim();
        const content = contentInput.value.trim();
        if (!title || !content) return;
        modal.close();

        // Visa i chatten vad som skickas
        let userMsg = document.createElement('div');
        userMsg.className = 'chat-msg user';
        userMsg.textContent = `/articles/create title:${title} content:${content}`;
        chatlog.appendChild(userMsg);
        chatlog.scrollTop = chatlog.scrollHeight;

        const endpoint = `/articles/create title:${title} content:${content}`;
        const proxyEndpoint = `/mcp-proxy?endpoint=${encodeURIComponent(endpoint)}`;
        responseBox.innerHTML = '<span style="color:#b3e5ff;">Laddar...</span>';

        try {
            const resp = await fetch(proxyEndpoint);
            if (resp.ok) {
                const data = await resp.json();
                responseBox.innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
            } else {
                let botMsg = document.createElement('div');
                botMsg.className = 'chat-msg bot';
                botMsg.innerHTML = 'Kunde inte skapa artikel (HTTP ' + resp.status + ')';
                chatlog.appendChild(botMsg);
            }
        } catch (err) {
            let botMsg = document.createElement('div');
            botMsg.className = 'chat-msg bot';
            botMsg.textContent = 'Fel vid skapande av artikel. Prova igen.';
            chatlog.appendChild(botMsg);
        }
        chatlog.scrollTop = chatlog.scrollHeight;
        document.getElementById('endpointInput').focus();
    };
}
