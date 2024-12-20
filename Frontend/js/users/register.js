document.getElementById('register-form').addEventListener('submit', async function(e) {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const response = await fetch('/api/usuarios', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, email, password })
    });

    const data = await response.json();

    if (response.ok) {
        alert(data.message);
        window.location.href = 'login.html'; // Redirigir al login
    } else {
        alert(data.message); // Mostrar mensaje de error
    }
});