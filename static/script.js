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
const resumeText = document.getElementById("resume-text");
const jobRoleSelect = document.getElementById("job-role-select");
const jobDescription = document.getElementById("job-description");
const parseTextBtn = document.getElementById("parse-text-btn");
const matchTextBtn = document.getElementById("match-text-btn");
const showTaxonomyBtn = document.getElementById("show-taxonomy-btn");
const analysisResults = document.getElementById("analysis-results");
const toast = document.getElementById("toast");

const jobRoleTemplates = {
  "Frontend Developer": "Seeking a Frontend Developer with strong experience in HTML, CSS, JavaScript, React, responsive user interfaces, and collaboration with design teams.",
  "Backend Developer": "Looking for a Backend Developer skilled in Python, Node.js, REST APIs, database modeling, microservices, and cloud deployment.",
  "Data Scientist": "Hiring a Data Scientist with expertise in machine learning, data analysis, statistical modeling, Python, SQL, and communicating actionable insights.",
  "AI Engineer": "Seeking an AI Engineer experienced in deep learning, NLP, model deployment, TensorFlow/PyTorch, and building production-grade AI systems.",
};

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

jobRoleSelect.addEventListener("change", () => {
  const selectedRole = jobRoleSelect.value;
  if (selectedRole === "Custom") {
    jobDescription.value = "";
    jobDescription.focus();
    return;
  }
  jobDescription.value = selectedRole ? jobRoleTemplates[selectedRole] || "" : "";
});

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

parseTextBtn.addEventListener("click", async () => {
  const text = resumeText.value.trim();
  if (!text) {
    showToast("Enter resume text first.", "red");
    return;
  }

  try {
    const response = await fetch(`${BASE_URL}/api/parse-text`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    const data = await response.json();
    if (!response.ok) {
      showToast(data.error || "Parse failed.", "red");
      return;
    }
    renderResults(data);
    showToast("Resume parsed successfully!");
  } catch (err) {
    showToast("Server error while parsing.", "red");
  }
});

matchTextBtn.addEventListener("click", async () => {
  const text = resumeText.value.trim();
  const jd = jobDescription.value.trim();
  if (!text || !jd) {
    showToast("Provide both resume text and job description.", "red");
    return;
  }

  try {
    const response = await fetch(`${BASE_URL}/api/match-text`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ resume_text: text, job_description: jd }),
    });
    const data = await response.json();
    if (!response.ok) {
      showToast(data.error || "Match failed.", "red");
      return;
    }
    renderResults(data);
    showToast("Match result generated!");
  } catch (err) {
    showToast("Server error while matching.", "red");
  }
});

showTaxonomyBtn.addEventListener("click", async () => {
  try {
    const response = await fetch(`${BASE_URL}/api/skill-taxonomy`);
    const data = await response.json();
    if (!response.ok) {
      showToast("Unable to load taxonomy.", "red");
      return;
    }
    renderTaxonomy(data.skill_taxonomy);
  } catch (err) {
    showToast("Server error while loading taxonomy.", "red");
  }
});

function renderKeyValue(title, value, isHTML = false) {
  const row = document.createElement("div");
  row.className = "result-row";

  const label = document.createElement("div");
  label.className = "result-label";
  label.textContent = title;

  const content = document.createElement("div");
  content.className = "result-value";
  if (isHTML) {
    content.innerHTML = value;
  } else {
    content.textContent = value;
  }

  row.appendChild(label);
  row.appendChild(content);
  return row;
}

function renderResults(data) {
  analysisResults.innerHTML = "";

  if (data.parsed_resume) {
    const card = document.createElement("div");
    card.className = "result-card";

    const header = document.createElement("div");
    header.className = "result-card-header";
    header.innerHTML = data.match_score
      ? `<h3>Resume Match Result</h3><div class="match-score">Score: ${data.match_score}</div>`
      : `<h3>Parsed Resume</h3>`;
    card.appendChild(header);

    const parsed = data.parsed_resume;
    if (parsed.name) card.appendChild(renderKeyValue("Name", parsed.name));
    if (parsed.email) card.appendChild(renderKeyValue("Email", parsed.email));
    if (parsed.phone && parsed.phone.length)
      card.appendChild(renderKeyValue("Phone", parsed.phone.join(", ")));
    if (parsed.location && parsed.location.length)
      card.appendChild(renderKeyValue("Location", parsed.location.join(", ")));
    if (parsed.education && parsed.education.length)
      card.appendChild(renderKeyValue("Education", parsed.education.join("; ")));
    if (parsed.skills && Object.keys(parsed.skills).length) {
      const skillRows = Object.entries(parsed.skills)
        .map(([category, skills]) => `<strong>${category}:</strong> ${skills.join(", ")}`)
        .join("<br>");
      card.appendChild(renderKeyValue("Skills", skillRows, true));
    }
    if (parsed.summary && parsed.summary.length)
      card.appendChild(renderKeyValue("Summary", parsed.summary.join(" ")));
    if (parsed.experience && parsed.experience.length)
      card.appendChild(renderKeyValue("Experience", parsed.experience.join(", ")));

    analysisResults.appendChild(card);
    return;
  }

  const pre = document.createElement("pre");
  pre.textContent = JSON.stringify(data, null, 2);
  analysisResults.appendChild(pre);
}

function renderTaxonomy(taxonomy) {
  analysisResults.innerHTML = "";
  const container = document.createElement("div");
  container.className = "taxonomy-panel";

  Object.entries(taxonomy).forEach(([category, skills]) => {
    const section = document.createElement("div");
    section.className = "taxonomy-category";
    section.innerHTML = `<h3>${category}</h3><p>${skills.join(", ")}</p>`;
    container.appendChild(section);
  });

  analysisResults.appendChild(container);
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
  const selectedRole = jobRoleSelect.value;
  const fillJobDescription = jobDescription.value.trim() || (selectedRole ? jobRoleTemplates[selectedRole] : "");
  formData.append("job_description", fillJobDescription || "Candidate for technical role");

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
      if (result.resume_text) {
        resumeText.value = result.resume_text;
      }
      if (result.parsed_resume) {
        renderResults(result);
      }
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
