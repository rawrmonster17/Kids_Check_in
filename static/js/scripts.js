document.addEventListener('DOMContentLoaded', function() {
    const loginButton = document.getElementById('loginButton');
    const loginPopup = document.getElementById('loginPopup');
    const closeSpan = document.getElementsByClassName('close')[0];
    const loginForm = document.getElementById('loginForm');
    const loginError = document.getElementById('loginError');
    const addKidForm = document.getElementById('addKidForm');
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

    async function refreshKidsList() {
        try {
            const response = await fetch('/kids/');
            const kids = await response.json();
            console.log('Received kids:', kids);

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

    refreshKidsList();
});
