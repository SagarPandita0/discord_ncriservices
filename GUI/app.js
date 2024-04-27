async function fetchChannelData() {
  const channelId = document.getElementById("channelId").value;
  const loader = document.getElementById("loader");
  loader.style.display = "block"; // Show loader

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/export-discord-chats/?channel_id=${channelId}`
    );
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    loader.style.display = "none"; // Hide loader when done
  } catch (error) {
    console.error("Failed to fetch data: ", error);
    loader.style.display = "none"; // Hide loader on error
  }
}

function createMessageCard(message, containerId) {
  const messageCard = document.createElement("div");
  messageCard.className = "message-card";

  const avatarDiv = document.createElement("div");
  avatarDiv.className = "avatar";
  avatarDiv.innerHTML = `<img src="../GUI/profile.png" alt="User Icon">`;

  const contentDiv = document.createElement("div");
  contentDiv.className = "content";

  const authorSpan = document.createElement("span");
  authorSpan.className = "author";
  authorSpan.textContent = message.author_name;

  const textDiv = document.createElement("div");
  textDiv.className = "text";
  textDiv.innerHTML = message.content.replace(/\n/g, "<br>");

  const timestampDiv = document.createElement("div");
  timestampDiv.className = "timestamp";
  const timestamp = new Date(message.timestamp);
  timestampDiv.textContent =
    timestamp.toLocaleDateString() + " " + timestamp.toLocaleTimeString();

  contentDiv.appendChild(authorSpan);
  contentDiv.appendChild(textDiv);
  contentDiv.appendChild(timestampDiv);

  messageCard.appendChild(avatarDiv);
  messageCard.appendChild(contentDiv);

  document.getElementById(containerId).appendChild(messageCard);
}

async function searchByDate() {
  const startDate = document.getElementById("startDate").value + "T00:00:00";
  const endDate = document.getElementById("endDate").value + "T23:59:59";
  const container = document.getElementById("searchByDateOutput");
  container.innerHTML = "";

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/search_by_date?start_date=${startDate}&end_date=${endDate}`
    );
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    const data = await response.json();
    if (data.length === 0) {
      const noDataText = document.createElement("div");
      noDataText.textContent = "No data found!";
      noDataText.style.color = "red";
      container.appendChild(noDataText);
    } else {
      data.forEach((message) =>
        createMessageCard(message, "searchByDateOutput")
      );
    }
  } catch (error) {
    container.textContent = "Failed to load data: " + error.message;
  }
}

async function searchByKeyword() {
  const searchTerm = document.getElementById("searchTerm").value;
  const container = document.getElementById("keywordSearchOutput");
  container.innerHTML = "";

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/search?search_term=${searchTerm}`
    );
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    const data = await response.json();
    if (data.length === 0) {
      const noDataText = document.createElement("div");
      noDataText.textContent = "No data found!";
      noDataText.style.color = "red";
      container.appendChild(noDataText);
    } else {
      data.forEach((message) =>
        createMessageCard(message, "keywordSearchOutput")
      );
    }
  } catch (error) {
    container.textContent = "Failed to load data: " + error.message;
  }
}

async function searchByAuthor() {
  const authorName = document.getElementById("authorName").value;
  const container = document.getElementById("authorSearchOutput");
  container.innerHTML = "";

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/search_by_author?author_name=${authorName}`
    );
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    const data = await response.json();
    if (data.length === 0) {
      const noDataText = document.createElement("div");
      noDataText.textContent = "No data found!";
      noDataText.style.color = "red";
      container.appendChild(noDataText);
    } else {
      data.forEach((message) =>
        createMessageCard(message, "authorSearchOutput")
      );
    }
  } catch (error) {
    container.textContent = "Failed to load data: " + error.message;
  }
}
