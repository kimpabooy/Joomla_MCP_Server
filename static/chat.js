const textarea = document.getElementById('endpointInput');
const chatlog = document.getElementById('chatlog');
const responseBox = document.getElementById('endpoint-response');

function addUserMessage(text) {
    const userMsg = document.createElement('div');
    userMsg.className = 'chat-msg user';
    userMsg.textContent = text;
    chatlog.appendChild(userMsg);
}

function addBotMessage(text) {
    const botMsg = document.createElement('div');
    botMsg.className = 'chat-msg bot';
    botMsg.textContent = text;
    chatlog.appendChild(botMsg);
}

async function sendToLLM(message, shownMessage = message) {
    addUserMessage(shownMessage);
    responseBox.innerHTML = '<span style="color:#b3e5ff;">Tänker...</span>';

    try {
        const resp = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });

        const data = await resp.json();

        if (data.response) {
            addBotMessage(data.response);
            responseBox.innerHTML = '';
        } else {
            responseBox.innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
        }
    } catch (err) {
        addBotMessage('Fel vid kommunikation med AI. Prova igen.');
        responseBox.innerHTML = '';
    }

    chatlog.scrollTop = chatlog.scrollHeight;
}

textarea.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        document.getElementById('chatForm').dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
    }
});

document.getElementById('chatForm').onsubmit = async function (e) {
    e.preventDefault();
    const prompt = textarea.value.trim();
    if (!prompt) return;

    if (prompt === '/clear' || prompt === 'clear') {
        chatlog.innerHTML = '<div class="chat-msg bot">Skriv vad du vill göra i Joomla och tryck <b>Enter</b></div>';
        responseBox.innerHTML = '';
        textarea.value = '';
        textarea.focus();
        return;
    }

    if (prompt === '/articles/create') {
        textarea.value = '';
        showCreateModal();
        return;
    }

    const editMatch = prompt.match(/^\/articles(?:\/([\d]+))?\/edit$/);
    if (editMatch) {
        textarea.value = '';
        showEditModal(editMatch[1] || '');
        return;
    }

    const removeMatch = prompt.match(/^\/articles\/(\d+)\/remove$/);
    if (removeMatch) {
        textarea.value = '';
        showConfirmRemoveModal(removeMatch[1]);
        return;
    }

    textarea.value = '';
    textarea.focus();
    await sendToLLM(prompt, prompt);
};

function showConfirmRemoveModal(articleId) {
    const modal = document.getElementById('confirm-remove-modal');
    document.getElementById('confirm-remove-text').textContent =
        `Vill du verkligen ta bort artikel ${articleId} permanent? Detta går inte att ångra.`;
    modal.showModal();

    document.getElementById('confirm-remove-cancel').onclick = function () {
        modal.close();
        textarea.focus();
    };

    document.getElementById('confirm-remove-yes').onclick = async function () {
        modal.close();
        const llmPrompt = `Ta bort artikel med ID ${articleId} permanent.`;
        const shownMessage = `/articles/${articleId}/remove`;
        await sendToLLM(llmPrompt, shownMessage);
        textarea.focus();
    };
}

function showEditModal(prefillId) {
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
        textarea.focus();
    };

    document.getElementById('edit-modal-submit').onclick = async function () {
        const articleId = idInput.value.trim();
        const title = titleInput.value.trim();
        const content = contentInput.value.trim();
        if (!articleId || !title || !content) return;
        modal.close();

        const shownMessage = `/articles/${articleId}/edit title:${title} content:${content}`;
        const llmPrompt = `Redigera artikel med ID ${articleId}. Sätt ny titel till "${title}" och nytt innehåll till "${content}".`;
        await sendToLLM(llmPrompt, shownMessage);
        textarea.focus();
    };
}

function showCreateModal() {
    const modal = document.getElementById('create-modal');
    const titleInput = document.getElementById('modal-title');
    const contentInput = document.getElementById('modal-content');
    titleInput.value = '';
    contentInput.value = '';
    modal.showModal();
    titleInput.focus();

    document.getElementById('modal-cancel').onclick = function () {
        modal.close();
        textarea.focus();
    };

    document.getElementById('modal-submit').onclick = async function () {
        const title = titleInput.value.trim();
        const content = contentInput.value.trim();
        if (!title || !content) return;
        modal.close();

        const shownMessage = `/articles/create title:${title} content:${content}`;
        const llmPrompt = `Skapa en ny artikel med titeln "${title}" och innehållet "${content}".`;
        await sendToLLM(llmPrompt, shownMessage);
        textarea.focus();
    };
}
