document.addEventListener('DOMContentLoaded', async () => {
    const orderList = document.getElementById('order-list');
    const addOrderBtn = document.createElement('button');
    addOrderBtn.textContent = 'Registrar Nueva Orden';
    addOrderBtn.addEventListener('click', () => registerOrder());
    orderList.parentNode.insertBefore(addOrderBtn, orderList);

    // Cargar órdenes
    async function fetchOrders() {
        try {
            const response = await fetch('/api/ordenes', {
                headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` },
            });
            const data = await response.json();

            if (response.ok) {
                orderList.innerHTML = data.ordenes.map(orden => `
                    <div>
                        <h4>Orden #${orden.id}</h4>
                        <p>Productos: ${orden.productos.map(p => `${p.nombre} (x${p.cantidad})`).join(', ')}</p>
                        <p>Estado: ${orden.estado}</p>
                        <p>Fecha: ${new Date(orden.fecha_pedido).toLocaleDateString()}</p>
                        <button onclick="viewOrder(${orden.id})">Ver Detalles</button>
                    </div>
                `).join('');
            } else {
                alert(data.message || 'Error al cargar órdenes.');
            }
        } catch (error) {
            console.error('Error fetching orders:', error);
        }
    }

    // Registrar una nueva orden
    async function registerOrder() {
        const productId = prompt('ID del producto:');
        const quantity = prompt('Cantidad solicitada:');
        if (productId && quantity) {
            try {
                const response = await fetch('/api/ordenes', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('token')}`,
                    },
                    body: JSON.stringify({
                        productos: [{ id: productId, cantidad: parseInt(quantity) }],
                        estado: 'Pendiente',
                        fecha_pedido: new Date().toISOString(),
                    }),
                });

                const data = await response.json();
                if (response.ok) {
                    alert('Orden registrada con éxito.');
                    fetchOrders();
                } else {
                    alert(data.message || 'Error al registrar orden.');
                }
            } catch (error) {
                console.error('Error registering order:', error);
            }
        }
    }

    // Ver detalles de una orden (demostración)
    window.viewOrder = async function (id) {
        try {
            const response = await fetch(`/api/ordenes/${id}`, {
                headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` },
            });
            const data = await response.json();

            if (response.ok) {
                alert(`Detalles de la orden #${id}:\n${JSON.stringify(data, null, 2)}`);
            } else {
                alert('Error al obtener detalles de la orden.');
            }
        } catch (error) {
            console.error('Error fetching order details:', error);
        }
    };

    // Cargar lista de órdenes al cargar el dashboard
    fetchOrders();
});
