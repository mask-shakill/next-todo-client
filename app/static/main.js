// API endpoint configuration
const API_URL = "http://localhost:8000/api/tts/convert";

function showStatus(message, isError = false) {
  const statusDiv = document.getElementById("status");
  statusDiv.textContent = message;
  statusDiv.style.color = isError ? "#dc2626" : "#059669";
}

function clearAudioPlayer() {
  const audioPlayer = document.getElementById("audioPlayer");
  audioPlayer.innerHTML = "";
}

function base64ToBlob(base64, mimeType) {
  const byteCharacters = atob(base64);
  const byteNumbers = new Array(byteCharacters.length);

  for (let i = 0; i < byteCharacters.length; i++) {
    byteNumbers[i] = byteCharacters.charCodeAt(i);
  }

  const byteArray = new Uint8Array(byteNumbers);
  return new Blob([byteArray], { type: mimeType });
}

function downloadAudio(base64Audio, filename) {
  const blob = base64ToBlob(base64Audio, "audio/mpeg");
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  window.URL.revokeObjectURL(url);
  a.remove();
}

function playAudio(base64Audio) {
  const blob = base64ToBlob(base64Audio, "audio/mpeg");
  const url = window.URL.createObjectURL(blob);
  const audioPlayer = document.getElementById("audioPlayer");
  audioPlayer.innerHTML = `
        <audio controls autoplay>
            <source src="${url}" type="audio/mpeg">
            Your browser does not support the audio element.
        </audio>
    `;
}

async function convertText() {
  const text = document.getElementById("textInput").value.trim();
  const voiceType = document.getElementById("voiceType").value;
  const outputType = document.getElementById("outputType").value;
  const convertBtn = document.getElementById("convertBtn");

  if (!text) {
    showStatus("Please enter some text to convert", true);
    return;
  }

  convertBtn.disabled = true;
  convertBtn.textContent = "Converting...";
  clearAudioPlayer();
  showStatus("Converting text to speech...");

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        text: text,
        voice_type: voiceType,
        output: outputType,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Failed to convert text to speech");
    }

    const data = await response.json();

    if (data.success) {
      if (outputType === "download") {
        downloadAudio(data.audio_content, data.filename);
        showStatus("Audio file downloaded successfully");
      } else {
        playAudio(data.audio_content);
        showStatus("Audio generated successfully");
      }
    } else {
      throw new Error(data.message);
    }
  } catch (error) {
    showStatus(`Error: ${error.message}`, true);
    console.error("Error:", error);
  } finally {
    convertBtn.disabled = false;
    convertBtn.textContent = "Convert";
  }
}

// Event Listeners
document.getElementById("textInput").addEventListener("input", () => {
  showStatus("");
});

document.getElementById("outputType").addEventListener("change", () => {
  clearAudioPlayer();
  showStatus("");
});
