const video = document.getElementById('video');
const resultBox = document.getElementById('result');
const overlay = document.getElementById('overlay');
const ctx = overlay.getContext('2d');
const logContainer = document.getElementById('attendanceLog');
const clockDisplay = document.getElementById('clockDisplay');

// Start webcam
navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    video.srcObject = stream;
    video.onloadedmetadata = () => video.play();
  })
  .catch(err => {
    console.error("Camera error:", err);
    resultBox.innerText = "❌ Webcam access denied";
  });

// Capture frame and send to backend
function captureFrame() {
  const className = document.getElementById('classSelector').value;
  const periodTime = document.getElementById('periodSelector').value;

  if (video.videoWidth === 0 || video.videoHeight === 0) {
    resultBox.innerText = "⚠️ Webcam not ready. Try again.";
    return;
  }

  const canvas = document.createElement('canvas');
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext('2d').drawImage(video, 0, 0);
  const imageData = canvas.toDataURL('image/jpeg');

  fetch('/mark', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ image: imageData, class: className, period: periodTime })
  })
  .then(res => res.json())
  .then(data => {
    ctx.clearRect(0, 0, overlay.width, overlay.height);

    if (data.error) {
      resultBox.innerText = "⚠️ " + data.error;
      logUnknown(className, periodTime);
      return;
    }

    if (!data.faces || data.faces.length === 0) {
      resultBox.innerText = "⚠️ No recognizable faces found.";
      logUnknown(className, periodTime);
      return;
    }

    resultBox.innerText = `✅ Processed ${data.faces.length} face(s)`;

    data.faces.forEach((face, index) => {
      const { x, y, w, h, name, status, timestamp, class_name, period_time } = face;
      const color = status === "known" ? "green" : "red";
      ctx.strokeStyle = color;
      ctx.lineWidth = 2;
      ctx.strokeRect(x, y, w, h);

      const label = status === "known" ? `${name} (${timestamp})` : "Unknown";
      ctx.fillStyle = color;
      ctx.font = "16px Arial";
      ctx.fillText(label, x, y - 10);

      const entry = document.createElement('div');
      entry.className = `log-entry ${color}`;
      entry.style.animationDelay = `${index * 0.1}s`;
      entry.innerHTML = `
        <div class="log-name">${label}</div>
        <div class="log-time">${timestamp || "—"}</div>
        <div class="log-status">${status === "known" ? "✅ Present" : "❌ Unknown"}</div>
        <div class="log-status">Class: ${class_name}, Period: ${period_time}</div>
      `;
      logContainer.appendChild(entry);
    });
  })
  .catch(err => {
    resultBox.innerText = "⚠️ Error sending image";
    console.error(err);
    logUnknown(className, periodTime);
  });
}

// Log unknown entry
function logUnknown(className, periodTime) {
  const entry = document.createElement('div');
  entry.className = `log-entry red`;
  entry.innerHTML = `
    <div class="log-name">Unknown</div>
    <div class="log-time">—</div>
    <div class="log-status">❌ Unknown</div>
    <div class="log-status">Class: ${className}, Period: ${periodTime}</div>
  `;
  logContainer.appendChild(entry);
}

// Clear attendance log
function clearLog() {
  logContainer.innerHTML = '<h3>Attendance Log</h3>';
  resultBox.innerText = '';
}

// Live clock
function updateClock() {
  const now = new Date();
  clockDisplay.innerText = now.toLocaleString();
}
setInterval(updateClock, 1000);
