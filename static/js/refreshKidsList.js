// refreshKidsList.js
async function refreshKidsList() {
    try {
        const response = await fetch("/families/");
        const families = await response.json();

        const checkedInKidsList = document.getElementById("checkedInKidsList");
        const checkedOutKidsList = document.getElementById("checkedOutKidsList");

        // Clear the existing list items
        checkedInKidsList.innerHTML = "";
        checkedOutKidsList.innerHTML = "";

        families.forEach(family => {
            console.log(family);  // Debugging: Log family data to check if id is present

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

// Call refreshKidsList to load the list on page load
refreshKidsList();
