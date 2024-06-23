document.addEventListener("DOMContentLoaded", function() {
    // Event listener for form submission
    document.getElementById('addFamilyForm').addEventListener('submit', async function(event) {
        event.preventDefault(); // Prevent default form submission

        // Collect form data
        const formData = new FormData(event.target);
        const data = {
            kid_first_name: formData.get('kid_first_name'),
            kid_last_name: formData.get('kid_last_name'),
            kid_allergies: formData.get('kid_allergies'),
            parent_first_name: formData.get('parent_first_name'),
            parent_last_name: formData.get('parent_last_name'),
            parent_phone_number: formData.get('parent_phone_number'),
            parent_email: formData.get('parent_email'),
            kid_checked_in: formData.get('kid_checked_in') === 'true' // Convert checkbox value to boolean
        };

        try {
            // Send form data to the server
            const response = await fetch('/family/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                alert('Family added successfully!');
                // Optionally reset the form
                event.target.reset();
            } else {
                const errorData = await response.json();
                alert(`Error: ${JSON.stringify(errorData)}`);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while adding the family. Please try again later.');
        }
    });
});
