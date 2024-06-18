document.addEventListener('DOMContentLoaded', function() {
    const addKidForm = document.getElementById('addKidForm');

    addKidForm.addEventListener('submit', async function(event) {
        event.preventDefault();
        const formData = new FormData(addKidForm);
        const data = {
            kid_first_name: formData.get('kidFirstName'),
            kid_last_name: formData.get('kidLastName'),
            kid_allergies: formData.get('kidAllergies'),
            kid_checked_in: formData.get('kidCheckedIn') === 'on',
            parent_first_name: formData.get('parentFirstName'),
            parent_last_name: formData.get('parentLastName'),
            parent_phone_number: formData.get('parentPhoneNumber'),
            parent_email: formData.get('parentEmail')
        };

        console.log(data); // Log the data to verify it's being collected correctly

        try {
            const response = await fetch('/add_kid_with_parent/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                console.log('Kid with parent added:', await response.json());
                refreshKidsList();
            } else {
                console.error('Failed to add kid with parent:', await response.text());
            }
        } catch (error) {
            console.error('Error adding kid:', error);
        }
    });
});
