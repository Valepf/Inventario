document.addEventListener('DOMContentLoaded', async () => {
    const productList = document.getElementById('product-list');
    const addProductBtn = document.getElementById('add-product-btn');

    // Cargar productos
    async function fetchProducts() {
        try {
            const response = await fetch('/api/productos', {
                headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` },
            });
            const data = await response.json();

            if (response.ok) {
                productList.innerHTML = data.productos.map(producto => `
                    <div>
                        <h4>${producto.name}</h4>
                        <p>${producto.description}</p>
                        <p>Stock: ${producto.stock}</p>
                        <button onclick="editProduct(${producto.id})">Editar</button>
                        <button onclick="deleteProduct(${producto.id})">Eliminar</button>
                    </div>
                `).join('');
            } else {
                alert(data.message || 'Error al cargar productos.');
            }
        } catch (error) {
            console.error('Error fetching products:', error);
        }
    }

    // Agregar producto
    addProductBtn.addEventListener('click', () => {
        const name = prompt('Nombre del producto:');
        const description = prompt('Descripción:');
        const stock = prompt('Stock inicial:');
        const price = prompt('Precio:');
        const categoryId = prompt('ID de categoría:');

        if (name && description && stock && price && categoryId) {
            addProduct({ name, description, stock, price, category_id: categoryId });
        }
    });

    async function addProduct(product) {
        try {
            const response = await fetch('/api/productos', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`,
                },
                body: JSON.stringify(product),
            });

            const data = await response.json();
            if (response.ok) {
                alert('Producto agregado con éxito.');
                fetchProducts();
            } else {
                alert(data.message || 'Error al agregar producto.');
            }
        } catch (error) {
            console.error('Error adding product:', error);
        }
    }

    // Cargar lista al cargar el dashboard
    fetchProducts();
});
