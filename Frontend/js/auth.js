document.getElementById('loginForm').addEventListener('submit', function (e) {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Credenciales predeterminadas para pruebas
    const defaultUser = 'admin';
    const defaultPass = '123456';

    if (username === defaultUser && password === defaultPass) {
        localStorage.setItem('token', 'dummyToken'); // Simula un token
        window.location.href = 'dashboard.html'; // Redirige al dashboard
    } else {
        alert('Usuario o contraseña incorrectos');
    }
});
