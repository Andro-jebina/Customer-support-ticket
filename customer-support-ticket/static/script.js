// Sends the ticket to Flask (/analyze) and shows the result without reloading the page.

const form = document.getElementById("ticketForm");
const errorMessage = document.getElementById("errorMessage");
const resultCard = document.getElementById("resultCard");

form.addEventListener("submit", async function (event) {
  event.preventDefault();
  errorMessage.textContent = "";

  const ticket = {
    account_name: document.getElementById("accountName").value,
    issue_type: document.getElementById("issueType").value,
    description: document.getElementById("description").value
  };

  try {
    const response = await fetch("/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(ticket)
    });
    const data = await response.json();

    if (!response.ok) {
      errorMessage.textContent = data.error;
      resultCard.hidden = true;
      return;
    }
    showResult(data);
  } catch (error) {
    errorMessage.textContent = "Could not reach the server. Make sure Flask is running.";
  }
});

function showResult(data) {
  const priority = data.priority.toLowerCase();   // high / medium / low

  document.getElementById("resultAccount").textContent =
    "Account: " + data.account_name + " | Issue Type: " + data.issue_type;

  const badge = document.getElementById("resultPriority");
  badge.textContent = data.priority.toUpperCase();
  badge.className = "badge " + priority;

  document.getElementById("resultAgent").textContent = data.assigned_agent;
  document.getElementById("resultAction").textContent = data.action_message;

  document.getElementById("resultKeyword").textContent = data.matched_keyword
    ? 'Keyword found in description: "' + data.matched_keyword + '"'
    : "No High or Medium keyword found, so the default priority is Low.";

  // Urgent task message is shown only for High priority
  document.getElementById("resultTask").hidden = (data.priority !== "High");

  resultCard.hidden = false;
  resultCard.scrollIntoView({ behavior: "smooth", block: "nearest" });
}
