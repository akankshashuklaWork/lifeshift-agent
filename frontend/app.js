const APP_NAME = "app";
const USER_ID = "lifeshift-user";
const API_BASE = window.location.origin;

const messagesEl = document.getElementById("messages");
const welcomeEl = document.getElementById("welcome");
const scenarioGrid = document.getElementById("scenarioGrid");
const composer = document.getElementById("composer");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const statusDot = document.getElementById("statusDot");
const statusText = document.getElementById("statusText");
const thinkingBar = document.getElementById("thinkingBar");
const thinkingText = document.getElementById("thinkingText");
const newChatBtn = document.getElementById("newChatBtn");

const THINKING_STEPS = [
  "Understanding your situation…",
  "Building your transition plan…",
  "Estimating budget ranges…",
  "Preparing your next steps…",
];

let sessionId = null;
let isSending = false;
let thinkingTimer = null;
let hasConversation = false;

function setStatus(state, text) {
  statusDot.className = `status-dot ${state}`;
  statusText.textContent = text;
}

function showThinking(stepIndex = 0) {
  thinkingBar.classList.remove("hidden");
  thinkingText.textContent = THINKING_STEPS[stepIndex % THINKING_STEPS.length];
  clearInterval(thinkingTimer);
  let step = stepIndex;
  thinkingTimer = setInterval(() => {
    step += 1;
    thinkingText.textContent = THINKING_STEPS[step % THINKING_STEPS.length];
  }, 2800);
}

function hideThinking() {
  thinkingBar.classList.add("hidden");
  clearInterval(thinkingTimer);
  thinkingTimer = null;
}

function escapeHtml(text) {
  return text
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function formatInline(text) {
  return text
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.+?)\*/g, "<em>$1</em>")
    .replace(/`([^`]+)`/g, "<code>$1</code>");
}

function isTableRow(line) {
  return /^\s*\|.+\|\s*$/.test(line);
}

function isTableSeparator(line) {
  return /^\s*\|?[\s:-]+\|[\s|:-]+\|?\s*$/.test(line);
}

function parseTableRow(line) {
  return line
    .trim()
    .replace(/^\|/, "")
    .replace(/\|$/, "")
    .split("|")
    .map((cell) => cell.trim());
}

function formatMarkdown(text) {
  const lines = escapeHtml(text).split("\n");
  const html = [];
  let inList = false;
  let listType = null;
  let tableRows = [];

  function closeList() {
    if (inList) {
      html.push(listType === "ol" ? "</ol>" : "</ul>");
      inList = false;
      listType = null;
    }
  }

  function flushTable() {
    if (tableRows.length < 2) {
      for (const row of tableRows) {
        html.push(`<p>${formatInline(row.join(" | "))}</p>`);
      }
      tableRows = [];
      return;
    }
    const header = tableRows[0];
    const body = tableRows.slice(2);
    html.push('<div class="table-wrap"><table>');
    html.push("<thead><tr>");
    for (const cell of header) {
      html.push(`<th>${formatInline(cell)}</th>`);
    }
    html.push("</tr></thead><tbody>");
    for (const row of body) {
      html.push("<tr>");
      for (const cell of row) {
        html.push(`<td>${formatInline(cell)}</td>`);
      }
      html.push("</tr>");
    }
    html.push("</tbody></table></div>");
    tableRows = [];
  }

  for (const rawLine of lines) {
    const line = rawLine.trimEnd();

    if (isTableRow(line) || isTableSeparator(line)) {
      closeList();
      if (!isTableSeparator(line)) {
        tableRows.push(parseTableRow(line));
      }
      continue;
    }

    if (tableRows.length) {
      flushTable();
    }

    if (!line.trim()) {
      closeList();
      continue;
    }

    if (/^#{1,3}\s+/.test(line)) {
      closeList();
      const level = line.match(/^#+/)[0].length;
      const content = line.replace(/^#{1,3}\s+/, "");
      html.push(`<h${Math.min(level, 3)}>${formatInline(content)}</h${Math.min(level, 3)}>`);
      continue;
    }

    if (/^(\*\*\*|---)\s*$/.test(line.trim())) {
      closeList();
      html.push("<hr>");
      continue;
    }

    if (/^[-*]\s+/.test(line)) {
      if (!inList || listType !== "ul") {
        closeList();
        html.push("<ul>");
        inList = true;
        listType = "ul";
      }
      html.push(`<li>${formatInline(line.replace(/^[-*]\s+/, ""))}</li>`);
      continue;
    }

    if (/^\d+\.\s+/.test(line)) {
      if (!inList || listType !== "ol") {
        closeList();
        html.push("<ol>");
        inList = true;
        listType = "ol";
      }
      html.push(`<li>${formatInline(line.replace(/^\d+\.\s+/, ""))}</li>`);
      continue;
    }

    if (/^_.+_$/.test(line.trim())) {
      closeList();
      html.push(`<p class="disclaimer">${formatInline(line.trim().slice(1, -1))}</p>`);
      continue;
    }

    closeList();
    html.push(`<p>${formatInline(line)}</p>`);
  }

  closeList();
  if (tableRows.length) {
    flushTable();
  }

  return html.join("");
}

function scrollToBottom() {
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function formatTime(date = new Date()) {
  return date.toLocaleTimeString([], { hour: "numeric", minute: "2-digit" });
}

function createMessage(role, contentHtml, options = {}) {
  const article = document.createElement("article");
  article.className = `message ${role}`;
  article.innerHTML = `
    <div class="avatar" aria-hidden="true">${role === "user" ? "You" : "✦"}</div>
    <div class="message-body">
      <div class="bubble prose">${contentHtml}${options.streaming ? '<span class="stream-cursor" aria-hidden="true"></span>' : ""}</div>
      <div class="message-meta">
        <time datetime="${new Date().toISOString()}">${formatTime()}</time>
        ${
          role === "assistant" && !options.streaming
            ? '<button type="button" class="copy-btn" title="Copy response">Copy</button>'
            : ""
        }
      </div>
    </div>
  `;

  if (role === "assistant" && !options.streaming) {
    const copyBtn = article.querySelector(".copy-btn");
    copyBtn?.addEventListener("click", async () => {
      const text = article.querySelector(".bubble")?.innerText || "";
      await navigator.clipboard.writeText(text);
      copyBtn.textContent = "Copied";
      setTimeout(() => {
        copyBtn.textContent = "Copy";
      }, 1600);
    });
  }

  messagesEl.appendChild(article);
  scrollToBottom();
  return article;
}

function appendUserMessage(text) {
  hideWelcome();
  return createMessage("user", formatMarkdown(text));
}

function appendAssistantMessage(text, options = {}) {
  hideWelcome();
  return createMessage("assistant", formatMarkdown(text), options);
}

function hideWelcome() {
  if (!hasConversation) {
    hasConversation = true;
    welcomeEl.classList.add("hidden");
  }
}

function showWelcome() {
  hasConversation = false;
  welcomeEl.classList.remove("hidden");
  messagesEl.innerHTML = "";
}

async function createSession() {
  const response = await fetch(
    `${API_BASE}/apps/${APP_NAME}/users/${USER_ID}/sessions`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({}),
    },
  );
  if (!response.ok) {
    throw new Error(`Session creation failed (${response.status})`);
  }
  const data = await response.json();
  sessionId = data.id;
}

async function ensureSession() {
  if (!sessionId) {
    await createSession();
  }
}

function extractModelText(event) {
  const parts = event.content?.parts || [];
  return parts
    .map((part) => part.text || "")
    .join("")
    .trim();
}

function cleanResponseText(text) {
  let cleaned = text
    .replace(/\[tool:\s*[^\]]+\]/gi, "")
    .replace(/^\s*tool:\s*\S+\s*$/gim, "")
    .trim();
  const reminder =
    /_Reminder: LifeShift provides planning support only\.[\s\S]*?_/g;
  const hasReminder = reminder.test(cleaned);
  const withoutReminders = cleaned.replace(reminder, "").trim();
  if (!hasReminder) {
    return withoutReminders;
  }
  return (
    withoutReminders +
    "\n\n_Reminder: LifeShift provides planning support only. Confirm financial, legal, and medical decisions with qualified professionals._"
  );
}

async function runAgent(message, onUpdate) {
  await ensureSession();

  const response = await fetch(`${API_BASE}/run_sse`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      app_name: APP_NAME,
      user_id: USER_ID,
      session_id: sessionId,
      streaming: true,
      new_message: {
        role: "user",
        parts: [{ text: message }],
      },
    }),
  });

  if (!response.ok) {
    throw new Error(`Agent request failed (${response.status})`);
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  let fullText = "";
  let streamBuffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) {
      break;
    }

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split("\n");
    buffer = lines.pop() || "";

    for (const line of lines) {
      if (!line.startsWith("data:")) {
        continue;
      }
      const payload = line.slice(5).trim();
      if (!payload) {
        continue;
      }

      let event;
      try {
        event = JSON.parse(payload);
      } catch {
        continue;
      }

      if (event.error) {
        throw new Error(event.error);
      }

      if (event.content?.role !== "model") {
        continue;
      }

      const text = extractModelText(event);
      if (!text) {
        continue;
      }

      if (!event.partial) {
        fullText = text;
        streamBuffer = text;
      } else {
        streamBuffer += text;
        if (!fullText) {
          fullText = streamBuffer;
        }
      }

      const display = cleanResponseText((event.partial ? streamBuffer : fullText).trim());
      if (display) {
        onUpdate?.(display, Boolean(event.partial));
      }
    }
  }

  return {
    text:
      cleanResponseText(fullText.trim()) ||
      "I prepared a plan but couldn't render the response. Please try again.",
  };
}

async function sendMessage(text) {
  const message = text.trim();
  if (!message || isSending) {
    return;
  }

  isSending = true;
  sendBtn.disabled = true;
  appendUserMessage(message);
  userInput.value = "";
  userInput.style.height = "auto";

  showThinking(0);
  let streamMessage = null;

  try {
    const result = await runAgent(message, (partialText, isPartial) => {
      hideThinking();
      if (!streamMessage) {
        streamMessage = appendAssistantMessage(partialText, { streaming: true });
      } else {
        const bubble = streamMessage.querySelector(".bubble");
        bubble.innerHTML =
          formatMarkdown(partialText) +
          (isPartial ? '<span class="stream-cursor" aria-hidden="true"></span>' : "");
        scrollToBottom();
      }
    });

    hideThinking();

    if (streamMessage) {
      const bubble = streamMessage.querySelector(".bubble");
      bubble.innerHTML = formatMarkdown(result.text);
      streamMessage.querySelector(".message-meta")?.insertAdjacentHTML(
        "beforeend",
        '<button type="button" class="copy-btn" title="Copy response">Copy</button>',
      );
      const copyBtn = streamMessage.querySelector(".copy-btn");
      copyBtn?.addEventListener("click", async () => {
        await navigator.clipboard.writeText(result.text);
        copyBtn.textContent = "Copied";
        setTimeout(() => {
          copyBtn.textContent = "Copy";
        }, 1600);
      });
    } else {
      appendAssistantMessage(result.text);
    }

    setStatus("ready", "Ready");
  } catch (error) {
    hideThinking();
    streamMessage?.remove();
    appendAssistantMessage(
      `Something went wrong: ${error.message}. Make sure the LifeShift server is running and your GEMINI_API_KEY is set in .env.`,
    );
    setStatus("error", "Error");
  } finally {
    isSending = false;
    sendBtn.disabled = false;
    userInput.focus();
  }
}

async function startNewChat() {
  if (isSending) {
    return;
  }
  sessionId = null;
  showWelcome();
  setStatus("ready", "Ready");
  userInput.focus();
}

composer.addEventListener("submit", (event) => {
  event.preventDefault();
  sendMessage(userInput.value);
});

userInput.addEventListener("input", () => {
  userInput.style.height = "auto";
  userInput.style.height = `${Math.min(userInput.scrollHeight, 140)}px`;
});

userInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    sendMessage(userInput.value);
  }
});

function prefillComposer(text) {
  userInput.value = text;
  userInput.dispatchEvent(new Event("input"));
  userInput.focus();
  const firstBracket = text.indexOf("[");
  if (firstBracket !== -1) {
    const lastBracket = text.indexOf("]", firstBracket);
    if (lastBracket !== -1) {
      userInput.setSelectionRange(firstBracket, lastBracket + 1);
    }
  }
}

scenarioGrid.addEventListener("click", (event) => {
  const button = event.target.closest("button[data-prompt]");
  if (!button) {
    return;
  }
  prefillComposer(button.dataset.prompt);
});

newChatBtn.addEventListener("click", startNewChat);

async function init() {
  try {
    const version = await fetch(`${API_BASE}/version`);
    if (!version.ok) {
      throw new Error("API unavailable");
    }
    await createSession();
    setStatus("ready", "Ready");
  } catch {
    setStatus("error", "Start the LifeShift server first");
  }
}

init();
