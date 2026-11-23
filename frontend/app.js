
const API_URL = "http://localhost:8000";
const registerForm = document.getElementById("registerForm");
if (registerForm) {
    registerForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const formData = new FormData(registerForm);
        const data = Object.fromEntries(formData.entries());
        const message = document.getElementById("message");
        const response = await fetch(`${API_URL}/register`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        });
        const result = await response.json();
        if (response.ok) {
            message.textContent = result.message || "Account created! You can now log in.";
            message.style.color = "green";
        } else {
            message.textContent = typeof result.detail === "string" ? result.detail : "Please check your details and try again.";
            message.style.color = "red";
        }
    });
}

const loginForm = document.getElementById("loginForm");
if (loginForm) {
    loginForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const formData = new FormData(loginForm);
        const data = Object.fromEntries(formData.entries());
        const message = document.getElementById("message");
        const response = await fetch(`${API_URL}/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        });
        const result = await response.json();
        if (response.ok) {
            localStorage.setItem("access_token", result.access_token);
            message.textContent = "Login successful!";
            message.style.color = "green";
            // Redirect to the dashboard or another page
            window.location.href = "tickets.html"; // Change this to your desired page
        } else {
            message.textContent = typeof result.detail === "string" ? result.detail : "Please check your details and try again.";
            message.style.color = "red";
        }
    });
}

const ticketForm = document.getElementById("ticketForm");
if (ticketForm) {
    // 1. Not logged in? Go to the login page
    const token = localStorage.getItem("access_token");
    if (!token) {
        window.location.href = "login.html";
    } else {
        // 2. Get my tickets from the API and show them on the page
        async function loadTickets() {
            const response = await fetch(`${API_URL}/tickets`, {
                headers: {
                    "Authorization": `Bearer ${token}`,
                },
            });

            // Token expired or invalid remove it and go back to login
            if (response.status === 401) {
                localStorage.removeItem("access_token");
                window.location.href = "login.html";
                return;
            }
            // Find the <ul> and empty it (so tickets aren't shown twice)
            const tickets = await response.json();
            const ticketList = document.getElementById("ticketList");
            ticketList.innerHTML = "";
            for (const ticket of tickets) {
                // a new row
                const row = document.createElement("tr");
                //cell1:title
                const titleCell = document.createElement("td");
                titleCell.textContent = ticket.title;
                row.appendChild(titleCell);
                // cell 2: priority, with a badge
                const priorityCell = document.createElement("td");
                const priorityBadge = document.createElement("span");
                priorityBadge.className = `badge ${ticket.priority.toLowerCase()}`;
                priorityBadge.textContent = ticket.priority;
                priorityCell.appendChild(priorityBadge);
                row.appendChild(priorityCell);

                // cell 3: status, with a badge
                const statusCell = document.createElement("td");
                const statusBadge = document.createElement("span");
                statusBadge.className = `badge ${ticket.status.toLowerCase()}`;
                statusBadge.textContent = ticket.status;
                statusCell.appendChild(statusBadge);
                row.appendChild(statusCell);

                ticketList.appendChild(row);

            }
        }
        // 3. Show the tickets as soon as the page opens
        loadTickets();
        // ADD THE LOG OUT CODE HERE
        const logoutButton = document.getElementById("logoutButton");
        logoutButton.addEventListener("click", () => {
            // forget the token, then go to login
            localStorage.removeItem("access_token");
            window.location.href = "login.html";
        });
        // 4. Submit a new ticket

        ticketForm.addEventListener("submit", async (event) => {
            event.preventDefault();
            const formData = new FormData(ticketForm);
            const data = Object.fromEntries(formData.entries());
            const message = document.getElementById("message");
            const response = await fetch(`${API_URL}/tickets`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`,
                },
                body: JSON.stringify(data),
            });
            const result = await response.json();
            if (response.ok) {
                message.textContent = result.message || "Ticket created successfully!";
                message.style.color = "green";
                ticketForm.reset();   // clear the form
                loadTickets();    // refresh the list so the new ticket appears
            } else {
                message.textContent = typeof result.detail === "string" ? result.detail : "Please check your details and try again.";
                message.style.color = "red";
            }
        });
    }
}