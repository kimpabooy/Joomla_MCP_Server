const textarea = document.getElementById('endpointInput');
const chatlog = document.getElementById('chatlog');
const responseBox = document.getElementById('endpoint-response');
const WELCOME_MESSAGE = 'Hej! Jag kan hjälpa dig att hantera Joomla-artiklar. Vad vill du göra?';

function scrollChatToBottom() {
    chatlog.scrollTop = chatlog.scrollHeight;
}

function messageSentTime() {
    const now = new Date();
    return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

// Adds a user message to the chat log with the current timestamp.
function addUserMessage(text) {
    const userMsg = document.createElement('div');
    userMsg.className = 'chat-msg user';
    const textSpan = document.createElement('span');
    textSpan.className = 'msg-text';
    textSpan.textContent = text;
    const timeSpan = document.createElement('span');
    timeSpan.className = 'timestamp';
    timeSpan.textContent = messageSentTime();
    userMsg.appendChild(textSpan);
    userMsg.appendChild(timeSpan);
    chatlog.appendChild(userMsg);
    scrollChatToBottom();
}

// Adds a bot message to the chat log. If options.pending is true, it shows a "thinking" state without a timestamp.
function addBotMessage(text, options = {}) {
    const botMsg = document.createElement('div');
    botMsg.className = 'chat-msg bot';
    if (options.pending) {
        botMsg.classList.add('pending');
    }
    const textSpan = document.createElement('span');
    textSpan.className = 'msg-text';
    // Rendera Markdown till HTML med marked.js
    if (window.marked) {
        textSpan.innerHTML = window.marked.parse(text);
    } else {
        textSpan.textContent = text;
    }
    botMsg.appendChild(textSpan);

    // Add a timestamp if not a pending message.
    if (!options.pending) {
        const timeSpan = document.createElement('span');
        timeSpan.className = 'timestamp';
        timeSpan.textContent = messageSentTime();
        botMsg.appendChild(timeSpan);
    }
    chatlog.appendChild(botMsg);
    scrollChatToBottom();
    return botMsg;
}

// Sends a message to the LLM and handles the response, including any required confirmations or errors.
async function sendToLLM(message, shownMessage = message, extraPayload = {}) {
    addUserMessage(shownMessage);
    responseBox.innerHTML = '<span class="status-thinking">AI bearbetar begäran...</span>';
    const pendingBotMsg = addBotMessage('AI tänker...', { pending: true });

    try {
        const resp = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message, ...extraPayload })
        });
        let data = await resp.json();

        // Backwards-compatible unwrap in case backend accidentally returns a single-item array.
        if (Array.isArray(data) && data.length === 1 && typeof data[0] === 'object' && data[0] !== null) {
            data = data[0];
        }

        // If the response indicates that a confirmation is required, prompt the user and handle their decision.
        if (data.requires_confirmation) {
            pendingBotMsg.remove();
            addBotMessage(data.response || 'Åtgärden kräver bekräftelse.');
            responseBox.innerHTML = '';

            const confirmed = window.confirm('Destruktiv åtgärd upptäckt. Är du säker på att du vill fortsätta?');
            if (confirmed) {
                await sendToLLM(
                    'bekräfta',
                    `Bekräftar: ${data.proposed_action?.tool || data.proposed_actions?.[0]?.tool || 'destruktiv åtgärd'}`,
                    {
                        confirm: true,
                        confirmation_id: data.confirmation_id
                    }
                );
            } else {
                addBotMessage('Åtgärden avbröts.');
            }
            return;
        }

        if (data.error) {
            pendingBotMsg.remove();
            addBotMessage(data.error);
            responseBox.innerHTML = '';
            return;
        }

        // Visa alltid response-texten i chatten om den finns, även om tool_results finns.
        const hasToolResults = Array.isArray(data.tool_results) && data.tool_results.length > 0;
        if (data.response || hasToolResults) {
            pendingBotMsg.remove();

            // Visa response-texten om den finns
            const responseText = typeof data.response === 'string' && data.response.trim()
                ? data.response
                : null;
            if (responseText) {
                addBotMessage(responseText);
            }

            // Visa verktygsresultat i Händelse Resultat om de finns
            if (hasToolResults) {
                const display = data.tool_results.length === 1 ? data.tool_results[0] : data.tool_results;
                responseBox.innerHTML = '<pre>' + JSON.stringify(display, null, 2) + '</pre>';
                // Om det inte fanns någon response-text, visa fallback-meddelande i chatten
                if (!responseText) {
                    addBotMessage('Klart! Se Händelse Resultat till vänster för detaljer.');
                }
            } else {
                responseBox.innerHTML = '';
            }
        } else {
            pendingBotMsg.remove();
            responseBox.innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
            addBotMessage('Klart! Se Händelse Resultat till vänster för detaljer.');
        }
    } catch (err) {
        pendingBotMsg.remove();
        addBotMessage('Fel vid kommunikation med AI. Prova igen.');
        responseBox.innerHTML = '';
    }
}

// Handles the Enter key in the textarea to submit the form, while allowing Shift+Enter for new lines.
textarea.addEventListener('keydown', function (event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        document.getElementById('chatForm').dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
    }
});

// Handles form submission, including special commands for clearing the chat and managing articles, and sends user input to the LLM.
document.getElementById('chatForm').onsubmit = async function (event) {
    event.preventDefault();
    const prompt = textarea.value.trim();
    if (!prompt) return;

    if (prompt === '/clear' || prompt === 'clear') {
        chatlog.innerHTML = `<div class="chat-msg bot">${WELCOME_MESSAGE}</div>`;
        responseBox.innerHTML = '';
        textarea.value = '';
        textarea.focus();
        scrollChatToBottom();
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

// Shows a confirmation modal when the user attempts to remove an article.
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
