document.addEventListener('DOMContentLoaded', function() {
    const loginButton = document.getElementById('loginButton');
    const loginPopup = document.getElementById('loginPopup');
    const closeSpan = document.getElementsByClassName('close')[0];
    const loginForm = document.getElementById('loginForm');
    const loginError = document.getElementById('loginError');
    const checkedInKidsList = document.getElementById('checkedInKidsList');
    const checkedOutKidsList = document.getElementById('checkedOutKidsList');

    loginButton.onclick = function() {
        loginPopup.style.display = 'block';
    };

    closeSpan.onclick = function() {
        loginPopup.style.display = 'none';
    };

    window.onclick = function(event) {
        if (event.target === loginPopup) {
            loginPopup.style.display = 'none';
        }
    };

    loginForm.addEventListener('submit', async function(event) {
        event.preventDefault();
        const formData = new FormData(loginForm);
        const data = Object.fromEntries(formData.entries());

        try {
            const response = await fetch('/token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: new URLSearchParams(data)
            });

            if (response.ok) {
                const result = await response.json();
                localStorage.setItem('token', result.access_token);
                loginPopup.style.display = 'none';
            } else {
                loginError.textContent = 'Invalid username or password';
            }
        } catch (error) {
            console.error('Login failed:', error);
        }
    });

    async function refreshKidsList() {
        try {
            const response = await fetch("/families/");
            const families = await response.json();

            checkedInKidsList.innerHTML = "";
            checkedOutKidsList.innerHTML = "";

            families.forEach(family => {
                const listItem = document.createElement("li");
                listItem.innerText = `${family.kid_first_name} ${family.kid_last_name}`;

                const contactButton = document.createElement("button");
                contactButton.innerText = "Contact Parent";
                contactButton.addEventListener("click", async function() {
                    const token = localStorage.getItem("token");
                    if (!token) {
                        alert("You must be logged in to contact parents.");
                        return;
                    }
                    const response = await fetch(`/contact_parent/${family.id}`, {
                        method: "POST",
                        headers: {
                            "Authorization": `Bearer ${token}`
                        }
                    });

                    if (response.ok) {
                        alert("Parent contacted successfully!");
                    } else {
                        alert("Failed to contact parent. Please ensure you are logged in.");
                    }
                });

                const checkInOutButton = document.createElement("button");
                checkInOutButton.innerText = family.kid_checked_in ? "Check Out" : "Check In";
                checkInOutButton.addEventListener("click", async function() {
                    const newStatus = !family.kid_checked_in;
                    const response = await fetch(`/families/${family.id}`, {
                        method: "PUT",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({ kid_checked_in: newStatus })
                    });

                    if (response.ok) {
                        refreshKidsList();
                    } else {
                        alert("Failed to update check-in status.");
                    }
                });

                listItem.appendChild(contactButton);
                listItem.appendChild(checkInOutButton);

                if (family.kid_checked_in) {
                    checkedInKidsList.appendChild(listItem);
                } else {
                    checkedOutKidsList.appendChild(listItem);
                }
            });
        } catch (error) {
            console.error("Error refreshing kids list:", error);
        }
    }

    refreshKidsList();
});
