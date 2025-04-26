// Base URL for backend API
const BASE_URL = "http://localhost:5000";

// Get DOM elements
const openBtn = document.querySelector(".open-chatbot");
const chatbot = document.querySelector(".chatbot-container");
const closeBtn = document.querySelector(".close-chat");
const sendBtn = document.getElementById("send-btn");
const userInput = document.getElementById("user-input");
const chatBox = document.getElementById("chat-box");
const resumeInput = document.getElementById("resume");
const resumeStatus = document.getElementById("resume-status");
const toast = document.getElementById("toast");

// Show/hide chatbot
openBtn.addEventListener("click", () => {
  chatbot.classList.remove("hidden");
});
closeBtn.addEventListener("click", () => {
  chatbot.classList.add("hidden");
});

// Send message via button or Enter (without Shift)
sendBtn.addEventListener("click", sendMessage);
userInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

// Add message to chat box
function addMessage(sender, text) {
  const msgEl = document.createElement("div");
  msgEl.className = sender + "-message";
  msgEl.textContent = text;
  chatBox.appendChild(msgEl);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// Show toast message
function showToast(message, color = "#27ae60") {
  toast.textContent = message;
  toast.style.backgroundColor = color;
  toast.classList.remove("hidden");
  setTimeout(() => {
    toast.classList.add("hidden");
  }, 3000);
}

// Send chat message to Flask backend
async function sendMessage() {
  const msg = userInput.value.trim();
  if (!msg) return;

  addMessage("user", msg);
  userInput.value = "";

  // Typing animation
  const typingDots = document.createElement("div");
  typingDots.className = "bot-message typing";
  typingDots.textContent = "RecruitBot is typing...";
  chatBox.appendChild(typingDots);
  chatBox.scrollTop = chatBox.scrollHeight;

  try {
    const res = await fetch(`${BASE_URL}/api/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: msg }),
    });

    typingDots.remove();

    if (!res.ok) {
      addMessage("bot", "Oops! Server error.");
      return;
    }

    const data = await res.json();
    if (data.reply) {
      addMessage("bot", data.reply);
    } else {
      addMessage("bot", "Hmm, I didn’t get that.");
    }
  } catch (error) {
    typingDots.remove();
    addMessage("bot", "Sorry, I couldn’t reach the server.");
  }
}

// Upload resume file to Flask backend
resumeInput.addEventListener("change", async () => {
  const file = resumeInput.files[0];
  if (!file) return;

  const validTypes = [
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  ];

  if (!validTypes.includes(file.type)) {
    resumeStatus.textContent = "Please upload a valid PDF or Word document.";
    resumeStatus.style.color = "red";
    showToast("Invalid file type.", "red");
    return;
  }

  if (file.size > 5 * 1024 * 1024) {
    resumeStatus.textContent = "File too large. Max 5MB allowed.";
    resumeStatus.style.color = "red";
    showToast("File too large!", "red");
    return;
  }

  const formData = new FormData();
  formData.append("resume", file);
  formData.append("job_description", "Frontend Developer"); // default or dynamic

  resumeStatus.textContent = "Uploading...";
  resumeStatus.style.color = "#3498db";

  try {
    const response = await fetch(`${BASE_URL}/api/resume`, {
      method: "POST",
      body: formData,
    });

    const result = await response.json();

    if (response.ok) {
      resumeStatus.textContent = result.message;
      resumeStatus.style.color = "#27ae60";
      resumeInput.value = "";
      showToast("Resume uploaded successfully!");
    } else {
      resumeStatus.textContent = result.error || "Upload failed.";
      resumeStatus.style.color = "red";
      showToast(result.error || "Upload failed.", "red");
    }
  } catch (err) {
    resumeStatus.textContent = "Upload failed. Server may be offline.";
    resumeStatus.style.color = "red";
    showToast("Server not reachable.", "red");
  }
});
