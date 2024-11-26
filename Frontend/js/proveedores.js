document.addEventListener('DOMContentLoaded', async () => {
    const supplierList = document.getElementById('supplier-list');
    const addSupplierBtn = document.getElementById('add-supplier-btn');

    // Cargar proveedores
    async function fetchSuppliers() {
        try {
            const response = await fetch('/api/proveedores', {
                headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` },
            });
            const data = await response.json();

            if (response.ok) {
                supplierList.innerHTML = data.proveedores.map(proveedor => `
                    <div>
                        <h4>${proveedor.name}</h4>
                        <p>Email: ${proveedor.contact_email || 'N/A'}</p>
                        <p>Teléfono: ${proveedor.contact_phone || 'N/A'}</p>
                    </div>
                `).join('');
            } else {
                alert(data.message || 'Error al cargar proveedores.');
            }
        } catch (error) {
            console.error('Error fetching suppliers:', error);
        }
    }

    // Agregar proveedor
    addSupplierBtn.addEventListener('click', () => {
        const name = prompt('Nombre del proveedor:');
        const contactEmail = prompt('Email del proveedor:');
        const contactPhone = prompt('Teléfono del proveedor:');

        if (name) {
            addSupplier({ name, contact_email: contactEmail, contact_phone: contactPhone });
        }
    });

    async function addSupplier(supplier) {
        try {
            const response = await fetch('/api/proveedores', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`,
                },
                body: JSON.stringify(supplier),
            });

            const data = await response.json();
            if (response.ok) {
                alert('Proveedor agregado con éxito.');
                fetchSuppliers();
            } else {
                alert(data.message || 'Error al agregar proveedor.');
            }
        } catch (error) {
            console.error('Error adding supplier:', error);
        }
    }

    // Cargar lista al cargar el dashboard
    fetchSuppliers();
});
