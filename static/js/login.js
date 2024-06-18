document.addEventListener('DOMContentLoaded', function() {
    const loginButton = document.getElementById('loginButton');
    const loginPopup = document.getElementById('loginPopup');
    const closeSpan = document.getElementsByClassName('close')[0];
    const loginForm = document.getElementById('loginForm');
    const loginError = document.getElementById('loginError');

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
});
