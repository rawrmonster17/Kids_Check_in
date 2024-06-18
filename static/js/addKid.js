document.getElementById("addKidForm").addEventListener("submit", async function (e) {
    e.preventDefault();
    
    const kidFirstName = document.getElementById("kidFirstName").value;
    const kidLastName = document.getElementById("kidLastName").value;
    const kidAllergies = document.getElementById("kidAllergies").value;
    const parentFirstName = document.getElementById("parentFirstName").value;
    const parentLastName = document.getElementById("parentLastName").value;
    const parentPhoneNumber = document.getElementById("parentPhoneNumber").value;
    const parentEmail = document.getElementById("parentEmail").value;

    const kidWithParent = {
        kid_first_name: kidFirstName,
        kid_last_name: kidLastName,
        kid_allergies: kidAllergies,
        parent_first_name: parentFirstName,
        parent_last_name: parentLastName,
        parent_phone_number: parentPhoneNumber,
        parent_email: parentEmail
    };

    const response = await fetch("/add_kid_with_parent/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(kidWithParent)
    });

    if (response.ok) {
        alert("Kid and parent added successfully");
        document.getElementById("addKidForm").reset();
        refreshKidsList(); // Call this function to refresh the list of kids
    } else {
        const data = await response.json();
        alert(`Error: ${data.detail}`);
    }
});

