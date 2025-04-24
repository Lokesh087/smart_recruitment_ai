const openBtn = document.querySelector(".open-chatbot");
const chatbot = document.querySelector(".chatbot-container");
const closeBtn = document.querySelector(".close-chat");
const sendBtn = document.getElementById("send-btn");
const userInput = document.getElementById("user-input");
const chatBox = document.getElementById("chat-box");

openBtn.addEventListener("click", () => {
  chatbot.classList.remove("hidden");
});

closeBtn.addEventListener("click", () => {
  chatbot.classList.add("hidden");
});

sendBtn.addEventListener("click", sendMessage);
userInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") sendMessage();
});

function sendMessage() {
  const msg = userInput.value.trim();
  if (!msg) return;

  addMessage("user", msg);
  userInput.value = "";

  setTimeout(() => {
    addMessage("bot", getBotReply(msg));
  }, 800);
}

function addMessage(sender, text) {
  const msgEl = document.createElement("div");
  msgEl.className = sender + "-message";
  msgEl.textContent = text;
  chatBox.appendChild(msgEl);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function getBotReply(msg) {
  msg = msg.toLowerCase();
  if (msg.includes("job")) return "We currently have openings in Software Development and UI/UX Design.";
  if (msg.includes("resume")) return "Make sure your resume is clear, concise, and tailored to the job.";
  if (msg.includes("interview")) return "Practice common questions and focus on your experiences!";
  return "I'm here to help with anything related to jobs, resumes, or interviews.";
}

const resumeInput = document.getElementById("resume");
const resumeStatus = document.getElementById("resume-status");

resumeInput.addEventListener("change", () => {
  const file = resumeInput.files[0];
  if (file) {
    if (!["application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"].includes(file.type)) {
      resumeStatus.textContent = "Please upload a valid PDF or Word document.";
      resumeStatus.style.color = "red";
      return;
    }

    resumeStatus.textContent = `Uploaded: ${file.name}`;
    resumeStatus.style.color = "#27ae60";

    // Here you can send the file to a backend server
    // Example: uploadResume(file);
  }
});

