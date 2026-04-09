const API_URL = "http://18.222.251.28:8000/products"; // <--- REVISA TU IP AQUÍ

// Función para cargar los productos
async function cargarProductos() {
    const listado = document.getElementById("product-list");
    if(!listado) return; // Seguridad por si el ID no existe

    listado.innerHTML = `<p class="text-gray-500">Cargando productos desde AWS...</p>`;

    try {
        const res = await fetch(API_URL);
        const productos = await res.json();
        
        if (productos.length === 0) {
            listado.innerHTML = `<p class="text-orange-500 italic">La base de datos está vacía. ¡Agrega el primer producto!</p>`;
            return;
        }

        listado.innerHTML = "";
        productos.forEach(p => {
            listado.innerHTML += `
                <div class="bg-white rounded-lg shadow-md overflow-hidden border border-gray-100">
                    <img src="${p.image_url || 'https://via.placeholder.com/300'}" class="w-full h-48 object-cover" onerror="this.src='https://via.placeholder.com/300'">
                    <div class="p-4">
                        <h3 class="font-bold text-lg text-gray-800">${p.name}</h3>
                        <p class="text-gray-500 text-sm mb-3">${p.description || ''}</p>
                        <div class="flex justify-between items-center">
                            <span class="text-blue-600 font-bold text-xl">$${p.price}</span>
                            <span class="bg-gray-100 text-gray-600 text-xs px-2 py-1 rounded">Stock: ${p.stock}</span>
                        </div>
                    </div>
                </div>
            `;
        });
    } catch (err) {
        console.error(err);
        listado.innerHTML = `<p class="text-red-500 font-bold">Error: No se pudo conectar a la API. Revisa el CORS y la IP.</p>`;
    }
}

// Escuchar el formulario para crear productos
document.getElementById("productForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    
    const nuevoProducto = {
        name: document.getElementById("name").value,
        description: document.getElementById("description").value,
        price: parseFloat(document.getElementById("price").value),
        stock: parseInt(document.getElementById("stock").value),
        image_url: document.getElementById("image_url").value
    };

    try {
        const res = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(nuevoProducto)
        });

        if (res.ok) {
            alert("¡Producto guardado exitosamente!");
            document.getElementById("productForm").reset();
            cargarProductos(); // Recargar la lista
        }
    } catch (err) {
        alert("Error al conectar con el servidor.");
    }
});

// Cargar al inicio
document.addEventListener("DOMContentLoaded", cargarProductos);