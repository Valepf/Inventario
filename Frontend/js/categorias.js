document.addEventListener('DOMContentLoaded', async () => {
    const categoryList = document.getElementById('category-list');
    const addCategoryBtn = document.getElementById('add-category-btn');

    // Cargar categorías
    async function fetchCategories() {
        try {
            const response = await fetch('/api/categorias', {
                headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` },
            });
            const data = await response.json();

            if (response.ok) {
                categoryList.innerHTML = data.categorias.map(categoria => `
                    <div>
                        <h4>${categoria.name}</h4>
                    </div>
                `).join('');
            } else {
                alert(data.message || 'Error al cargar categorías.');
            }
        } catch (error) {
            console.error('Error fetching categories:', error);
        }
    }

    // Agregar categoría
    addCategoryBtn.addEventListener('click', () => {
        const name = prompt('Nombre de la categoría:');
        if (name) {
            addCategory({ name });
        }
    });

    async function addCategory(category) {
        try {
            const response = await fetch('/api/categorias', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`,
                },
                body: JSON.stringify(category),
            });

            const data = await response.json();
            if (response.ok) {
                alert('Categoría agregada con éxito.');
                fetchCategories();
            } else {
                alert(data.message || 'Error al agregar categoría.');
            }
        } catch (error) {
            console.error('Error adding category:', error);
        }
    }

    // Cargar lista al cargar el dashboard
    fetchCategories();
});
