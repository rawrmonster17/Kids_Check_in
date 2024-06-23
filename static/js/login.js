// login.js
document.getElementById("loginForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("/token", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: new URLSearchParams({
                username: username,
                password: password
            })
        });

        if (!response.ok) {
            throw new Error("Network response was not ok " + response.statusText);
        }

        const data = await response.json();
        localStorage.setItem("token", data.access_token);
        document.getElementById("loginSuccess").innerText = "Login successful!";
        document.getElementById("loginPopup").style.display = "none";

        // Optionally refresh the list of kids or any other action on successful login
        // refreshKidsList();
    } catch (error) {
        document.getElementById("loginError").innerText = "Login failed: " + error.message;
    }
});
