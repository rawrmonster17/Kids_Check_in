// addFamily.js
document.getElementById("addFamilyForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    const kidFirstName = document.getElementById("kidFirstName").value;
    const kidLastName = document.getElementById("kidLastName").value;
    const kidAllergies = document.getElementById("kidAllergies").value;
    const parentFirstName = document.getElementById("parentFirstName").value;
    const parentLastName = document.getElementById("parentLastName").value;
    const parentPhoneNumber = document.getElementById("parentPhoneNumber").value;
    const parentEmail = document.getElementById("parentEmail").value;
    const kidCheckedIn = true; // Default to true on creation

    const familyData = {
        parent_first_name: parentFirstName,
        parent_last_name: parentLastName,
        parent_phone_number: parentPhoneNumber,
        parent_email: parentEmail,
        kid_first_name: kidFirstName,
        kid_last_name: kidLastName,
        kid_allergies: kidAllergies,
        kid_checked_in: kidCheckedIn
    };

    try {
        const response = await fetch("/family/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(familyData)
        });

        if (!response.ok) {
            throw new Error("Network response was not ok " + response.statusText);
        }

        const result = await response.json();
        alert("Family added successfully!");

        // Optionally refresh the list of kids
        refreshKidsList();
    } catch (error) {
        console.error("There was a problem with the fetch operation:", error);
    }
});
