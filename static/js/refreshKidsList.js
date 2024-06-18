async function refreshKidsList() {
    try {
        const response = await fetch('/kids/');
        const kids = await response.json();
        console.log('Received kids:', kids);

        const checkedInKidsList = document.getElementById('checkedInKidsList');
        const checkedOutKidsList = document.getElementById('checkedOutKidsList');

        checkedInKidsList.innerHTML = '';
        checkedOutKidsList.innerHTML = '';

        kids.forEach(kid => {
            const listItem = document.createElement('li');
            listItem.textContent = `${kid.first_name} ${kid.last_name} - Allergies: ${kid.allergies}`;

            const button = document.createElement('button');
            button.textContent = kid.checked_in ? 'Check Out' : 'Check In';
            button.addEventListener('click', async function() {
                kid.checked_in = !kid.checked_in;
                const response = await fetch(`/kids/${kid.id}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(kid)
                });

                if (response.ok) {
                    console.log('Kid status updated:', await response.json());
                    refreshKidsList();
                } else {
                    console.error('Failed to update kid status:', await response.text());
                }
            });

            listItem.appendChild(button);

            if (kid.checked_in) {
                const contactButton = document.createElement('button');
                contactButton.textContent = 'Contact Parent';
                contactButton.addEventListener('click', async function() {
                    const token = localStorage.getItem('token');
                    if (!token) {
                        alert('You must be logged in to contact parents.');
                        return;
                    }
                    const response = await fetch(`/contact_parent/${kid.id}`, {
                        method: 'POST',
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    });

                    if (response.ok) {
                        console.log('Parent contacted:', await response.json());
                    } else {
                        alert('Failed to contact parent. Please ensure you are logged in.');
                    }
                });
                listItem.appendChild(contactButton);
                checkedInKidsList.appendChild(listItem);
            } else {
                checkedOutKidsList.appendChild(listItem);
            }
        });
    } catch (error) {
        console.error('Error refreshing kids list:', error);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    refreshKidsList();
});
