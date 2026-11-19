
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
            message.textContent= typeof result.detail === "string" ? result.detail : "Please check your details and try again.";
            message.style.color = "red";
        }
    });
}