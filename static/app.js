const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const clearBtn = document.getElementById('clear-btn');

const extractedFactsEl = document.getElementById('extracted-facts');
const shortTermEl = document.getElementById('short-term');
const longTermEl = document.getElementById('long-term');

// 加载长期记忆
async function loadLongTermMemories() {
    try {
        const res = await fetch('/memories');
        const data = await res.json();
        renderList(longTermEl, data.memories || []);
    } catch (err) {
        console.error(err);
    }
}

// 渲染列表
function renderList(element, items) {
    element.innerHTML = '';
    if (items.length === 0) {
        element.innerHTML = '<li>（空）</li>';
        return;
    }
    items.forEach(item => {
        const li = document.createElement('li');
        li.textContent = item;
        element.appendChild(li);
    });
}

// 添加消息气泡
function addMessage(role, text) {
    const div = document.createElement('div');
    div.className = `message ${role}`;
    const span = document.createElement('span');
    span.textContent = text;
    div.appendChild(span);
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// 发送
async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    addMessage('user', message);
    userInput.value = '';
    sendBtn.disabled = true;

    try {
        const res = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });
        const data = await res.json();

        addMessage('assistant', data.reply);

        // 更新三个面板
        renderList(extractedFactsEl, data.extracted_facts || []);
        renderList(shortTermEl, data.short_term || []);
        renderList(longTermEl, data.retrieved_memories || []);

        // 刷新长期记忆总库
        loadLongTermMemories();
    } catch (err) {
        addMessage('assistant', '请求失败，请检查后端服务是否启动。');
    } finally {
        sendBtn.disabled = false;
        userInput.focus();
    }
}

// 清空
async function clearMemories() {
    if (!confirm('确定清空所有记忆？')) return;
    await fetch('/memories', { method: 'DELETE' });
    chatMessages.innerHTML = '';
    renderList(extractedFactsEl, []);
    renderList(shortTermEl, []);
    renderList(longTermEl, []);
    loadLongTermMemories();
}

sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', e => {
    if (e.key === 'Enter') sendMessage();
});
clearBtn.addEventListener('click', clearMemories);

// 初始化
loadLongTermMemories();