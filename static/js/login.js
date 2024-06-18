document.getElementById("loginForm").addEventListener("submit", async function (e) {
    e.preventDefault();
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch("/token", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`,
    });

    const data = await response.json();
    if (response.ok) {
        localStorage.setItem("token", data.access_token);
        document.getElementById("loginPopup").style.display = "none";
    } else {
        document.getElementById("loginError").innerText = data.detail;
    }
});

// Function to contact parent
async function contactParent(kidId) {
    const token = localStorage.getItem("token");
    const response = await fetch(`/contact_parent/${kidId}`, {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json",
        },
    });

    const data = await response.json();
    if (response.ok) {
        alert("Parent contacted successfully.");
    } else {
        alert(`Error: ${data.detail}`);
    }
}
