document.getElementById('login-form').addEventListener('submit', async function (e) {
    e.preventDefault(); // Prevenir el comportamiento predeterminado del formulario

    // Obtener los valores de los campos
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();

    // Validar que los campos no estén vacíos
    if (!username || !password) {
        alert("Por favor, completa todos los campos.");
        return;
    }

    try {
        // Enviar la solicitud al backend
        const response = await fetch('/api/usuarios/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });

        // Parsear la respuesta
        const data = await response.json();

        if (response.ok) {
            // Guardar el token en el localStorage
            localStorage.setItem('token', data.token);

            // Redirigir al dashboard
            window.location.href = 'dashboard.html';
        } else {
            // Mostrar mensaje de error proporcionado por el servidor
            alert(data.message || "Error al iniciar sesión. Por favor, intenta de nuevo.");
        }
    } catch (error) {
        // Manejar errores de conexión u otros imprevistos
        console.error("Error durante el login:", error);
        alert("Hubo un problema al intentar iniciar sesión. Por favor, revisa tu conexión e intenta nuevamente.");
    }
});


