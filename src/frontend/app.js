const chatWindow = document.getElementById('chat-window');
const userInput = document.getElementById('user-input');
const costDisplay = document.getElementById('total-cost');
const latencyDisplay = document.getElementById('last-latency');

// Handle Enter key
userInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

let totalSessionCost = 0.0;

async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    // Add User Message
    addMessage(text, 'user');
    userInput.value = '';

    // Add Loading Indicator
    const loadingId = addMessage("Thinking...", 'ai', true);

    const startTime = performance.now();

    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                prompt: text,
                max_tokens: 100,
                provider: 'auto'
            })
        });

        const data = await response.json();

        // Remove loading
        removeMessage(loadingId);

        let providerClass = data.routed_to === 'local' ? 'local' : 'huggingface';

        // Format cost
        const reqCost = parseFloat(data.cost || 0);
        totalSessionCost += reqCost;
        updateMetrics(totalSessionCost, data.latency);

        const metaHtml = `
            Routed to: <span class="provider-tag ${providerClass}">${data.routed_to.toUpperCase()}</span> 
            | Cost: $${reqCost.toFixed(6)} 
            | Latency: ${(data.latency * 1000).toFixed(0)}ms
        `;

        addMessage(data.text, 'ai', false, metaHtml);

    } catch (error) {
        removeMessage(loadingId);
        addMessage(`Error: ${error.message}`, 'ai');
    }
}

function addMessage(text, sender, isLoading = false, meta = null) {
    const div = document.createElement('div');
    div.classList.add('message', sender);
    if (isLoading) div.id = 'loading-' + Date.now();

    let content = text;
    if (meta) {
        content += `<span class="meta-info">${meta}</span>`;
    }

    div.innerHTML = content;
    chatWindow.appendChild(div);
    chatWindow.scrollTop = chatWindow.scrollHeight;
    return div.id;
}

function removeMessage(id) {
    const msg = document.getElementById(id);
    if (msg) msg.remove();
}

function updateMetrics(cost, latency) {
    costDisplay.textContent = '$' + cost.toFixed(6);
    if (latency) {
        latencyDisplay.textContent = (latency * 1000).toFixed(0) + ' ms';
    }
}

// Poll for real system total cost from metrics endpoint on load
// DISABLED: User wants session-based cost (resets on refresh)
/*
async function fetchGlobalMetrics() {
    try {
        const response = await fetch('/metrics');
        const text = await response.text();

        // Parse Prometheus format for llm_total_cost_usd_total
        // We need to sum ALL occurrences (e.g. one for local model, one for HF model)
        // Matches: llm_total_cost_usd_total{...} 0.000123
        const regex = /llm_total_cost_usd_total(?:\{[^}]*\})?\s+([\d\.eE+-]+)/g;
        let match;
        let totalGlobalCost = 0;
        let found = false;

        while ((match = regex.exec(text)) !== null) {
            if (match[1]) {
                totalGlobalCost += parseFloat(match[1]);
                found = true;
            }
        }

        if (found) {
            // Sync local session cost base
            totalSessionCost = totalGlobalCost;
            updateMetrics(totalGlobalCost, null);
        } else {
            console.log("Global cost metric not found in response");
        }
    } catch (e) {
        console.log("Metrics fetch failed", e);
    }
}
// Initial fetch on load
// fetchGlobalMetrics();
*/
