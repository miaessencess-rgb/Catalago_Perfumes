import os
import pandas as pd
from flask import Flask, render_template_string, url_for
import urllib.request
import io

app = Flask(__name__)

# ⚠️ PEGA AQUÍ TU ENLACE CSV
URL_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRAPuJtY8lL5Ikn-aOZpSiHyUz9slXX7a2AYtBCdDXBMeOfWQbuawPFrYMZbzQJ3GsYuXFaHDs3FiwA/pub?gid=1300626180&single=true&output=csv"

def limpiar_precio(val):
    try:
        if pd.isna(val) or val == '': return 0.0
        limpio = str(val).replace('$', '').replace(' ', '').replace(',', '.').strip()
        return float(limpio)
    except:
        return 0.0

def limpiar_stock(val):
    try:
        if pd.isna(val) or val == '': return 1
        return int(float(str(val).replace(' ', '').strip()))
    except:
        return 1

def cargar_catalogo():
    catalogo = []
    error_msg = ""
    
    try:
        req = urllib.request.Request(URL_CSV, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = response.read().decode('utf-8')
        
        df = pd.read_csv(io.StringIO(data))
        df.columns = df.columns.str.strip()
        
        ruta_carpeta = os.path.join(app.root_path, 'static', 'fotos')
        
        for _, row in df.iterrows():
            nombre = str(row.get('Nombre', '')).strip()
            marca = str(row.get('marca', '')).strip()
            
            if not nombre or nombre == 'nan':
                continue

            detal = limpiar_precio(row.get('precio_venta', 0))
            mayor = limpiar_precio(row.get('precio_mayor', 0))
            gran_mayor = limpiar_precio(row.get('precio_gran_mayor', 0))
            stock = limpiar_stock(row.get('stock', 1))
            
            slug = nombre.lower().replace(' ', '-').replace("'", "").replace('"', '').replace('&', 'and')
            imagen = f"/static/fotos/{slug}.jpg" 
            
            if os.path.exists(ruta_carpeta):
                for archivo in os.listdir(ruta_carpeta):
                    nombre_archivo, extension = os.path.splitext(archivo)
                    if nombre_archivo.lower() == slug.lower():
                        imagen = f"/static/fotos/{archivo}"
                        break
            
            nombre_lower = nombre.lower()
            genero = 'Unisex'
            if any(w in nombre_lower for w in ['men', 'man', 'hombre', 'sauvage', 'eros', 'bleu', 'one million', 'bad boy', 'elixir']):
                genero = 'Hombre'
            elif any(w in nombre_lower for w in ['fem', 'woman', 'girl', 'yara', 'good girl', 'libre', 'black opium', 'oud gold']):
                genero = 'Mujer'
                
            catalogo.append({
                "marca": marca,
                "producto": nombre,
                "detal": detal,
                "mayor": mayor,
                "gran_mayor": gran_mayor,
                "genero": genero,
                "imagen": imagen,
                "stock": stock
            })
    except Exception as e:
        error_msg = str(e)
        
    return catalogo, error_msg

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Catálogo Digital de Perfumes</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f4f6f8; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0; padding-bottom: 80px; }
        
        .header-bg { 
            background: linear-gradient(rgba(17, 24, 39, 0.7), rgba(17, 24, 39, 0.7)), url("{{ url_for('static', filename='fotos/banner.jpg') }}");
            background-size: cover;
            background-position: center;
            color: white; 
            text-align: center; 
            border-bottom: 4px solid #d97706; 
            padding: 3rem 1rem; 
        }

        .logo-header {
            width: 120px; height: 120px; object-fit: cover; 
            margin-bottom: 15px; border-radius: 50%; 
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            border: 4px solid #FFD700; background-color: #000; 
        }

        .card-perfume { border: none; border-radius: 12px; transition: transform 0.2s, box-shadow 0.2s; background: #ffffff; }
        .card-perfume:hover { transform: translateY(-3px); box-shadow: 0 10px 20px rgba(0,0,0,0.08); }
        .badge-brand { background-color: #f3f4f6; color: #374151; font-weight: 600; font-size: 0.75rem; padding: 0.35em 0.65em; border-radius: 6px; }
        .price-box { background-color: #f9fafb; border-radius: 8px; padding: 8px; font-size: 0.85rem; border: 1px solid #e5e7eb; }
        .price-detal { font-weight: bold; color: #059669; font-size: 1.05rem; }
        .price-label { color: #6b7280; font-size: 0.75rem; display: block; }
        .img-container { height: 140px; display: flex; align-items: center; justify-content: center; background-color: #fafafa; border-radius: 8px; overflow: hidden; margin-bottom: 10px; }
        .img-container img { max-height: 100%; max-width: 100%; object-fit: contain; }
        
        .card-agotado { opacity: 0.7; filter: grayscale(80%); }
        .badge-agotado { position: absolute; top: 20px; right: 20px; background-color: #dc3545; color: white; font-weight: bold; font-size: 0.8rem; padding: 0.4em 0.7em; border-radius: 6px; z-index: 10; box-shadow: 0 2px 4px rgba(0,0,0,0.2); }

        .btn-whatsapp { background-color: #25D366; color: white; font-weight: bold; border: none; }
        .btn-whatsapp:hover { background-color: #1ebe57; color: white; }
        .btn-agotado { background-color: #6c757d; color: white; font-weight: bold; border: none; cursor: not-allowed; }
        
        .cart-float {
            position: fixed; bottom: 20px; right: 20px; z-index: 1000;
            background-color: #25D366; color: white; border-radius: 50%;
            width: 65px; height: 65px; display: flex; align-items: center; justify-content: center;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3); cursor: pointer;
            font-size: 1.8rem; text-decoration: none; transition: transform 0.2s;
        }
        .cart-float:hover { transform: scale(1.1); color: white; }
        .cart-badge {
            position: absolute; top: -5px; right: -5px;
            background-color: #dc3545; color: white; border-radius: 50%;
            padding: 0.25em 0.6em; font-size: 0.8rem; font-weight: bold;
        }

        .toast-notification {
            position: fixed; bottom: 100px; left: 50%; transform: translateX(-50%);
            background-color: #333; color: white; padding: 10px 20px;
            border-radius: 20px; font-size: 0.9rem; z-index: 2000;
            opacity: 0; transition: opacity 0.3s; pointer-events: none;
        }
        .toast-notification.show { opacity: 1; }
    </style>
</head>
<body>

    <div class="header-bg shadow-sm mb-4">
        <img src="{{ url_for('static', filename='logo.jpg') }}" alt="Mi Logo" class="logo-header">
        <h1 class="fw-bold m-0">✨ Catálogo de Perfumes</h1>
        <p class="text-light opacity-75 mt-1 small">Detal, Mayor (6+ unds) y Gran Mayor (15+ unds)</p>
    </div>

    <div class="container pb-5">
        {% if error_msg %}
        <div class="alert alert-danger text-center">
            <strong>Error al cargar los productos:</strong> {{ error_msg }}
        </div>
        {% endif %}

        <div class="row justify-content-center mb-4">
            <div class="col-12 col-md-8 col-lg-6">
                <input type="text" id="searchInput" class="form-control form-control-lg shadow-sm" placeholder="🔍 Buscar perfume o marca..." onkeyup="filterProducts()">
            </div>
        </div>

        <div class="row g-3" id="productList">
            {% for item in catalogo %}
            <div class="col-6 col-md-4 col-lg-3 product-item" data-search="{{ item.marca.lower() }} {{ item.producto.lower() }}">
                
                <div class="card card-perfume h-100 p-3 shadow-sm d-flex flex-column justify-content-between position-relative {% if item.stock <= 0 %}card-agotado{% endif %}">
                    
                    {% if item.stock <= 0 %}
                        <div class="badge-agotado">AGOTADO</div>
                    {% endif %}

                    <div>
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <span class="badge badge-brand text-uppercase">{{ item.marca }}</span>
                            {% if item.genero == 'Mujer' %}
                                <span class="badge bg-danger-subtle text-danger" style="font-size:0.7rem;">Mujer</span>
                            {% elif item.genero == 'Hombre' %}
                                <span class="badge bg-primary-subtle text-primary" style="font-size:0.7rem;">Hombre</span>
                            {% else %}
                                <span class="badge bg-warning-subtle text-warning-emphasis" style="font-size:0.7rem;">Unisex</span>
                            {% endif %}
                        </div>
                        <div class="img-container">
                            <img src="{{ item.imagen }}" onerror="this.onerror=null; this.parentElement.innerHTML='<span class=\'text-muted small\'>📷 Sin imagen</span>';" alt="{{ item.producto }}">
                        </div>
                        <h6 class="card-title fw-bold text-dark mb-2" style="font-size: 0.9rem; min-height: 2.2em;">{{ item.producto }}</h6>
                    </div>
                    <div class="price-box mt-auto">
                        <div class="d-flex justify-content-between align-items-center mb-1 pb-1 border-bottom">
                            <span class="price-label">Detal:</span>
                            <span class="price-detal">${{ "%.2f"|format(item.detal) }}</span>
                        </div>
                        <div class="d-flex justify-content-between align-items-center mb-1">
                            <span class="price-label">Mayor (6+):</span>
                            <span class="fw-bold text-dark">${{ "%.2f"|format(item.mayor) }}</span>
                        </div>
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <span class="price-label">Gran Mayor (15+):</span>
                            <span class="fw-bold text-primary">${{ "%.2f"|format(item.gran_mayor) }}</span>
                        </div>
                        
                        {% if item.stock > 0 %}
                            <!-- CORREGIDO: Usamos el filtro tojson para escapar comillas y apóstrofes -->
                            <button onclick='addToCart({{ {"nombre": item.producto, "detal": item.detal, "mayor": item.mayor, "gran_mayor": item.gran_mayor} | tojson }})' class="btn btn-outline-dark btn-sm w-100 fw-bold" style="border-radius: 8px;">
                               ➕ Agregar al Pedido
                            </button>
                        {% else %}
                            <button class="btn btn-agotado btn-sm w-100" disabled>
                               ❌ Agotado por los momentos
                            </button>
                        {% endif %}
                        
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>

    <!-- Notificación Toast -->
    <div id="toast" class="toast-notification">✅ Producto agregado al carrito</div>

    <!-- Botón flotante del carrito -->
    <div id="cartButton" class="cart-float" onclick="sendOrder(event)">
        🛒
        <span id="cartCount" class="cart-badge">0</span>
    </div>

    <script>
    function filterProducts() {
        let input = document.getElementById('searchInput').value.toLowerCase();
        let items = document.getElementsByClassName('product-item');
        for (let i = 0; i < items.length; i++) {
            let searchData = items[i].getAttribute('data-search');
            if (searchData.includes(input)) { items[i].style.display = ""; } 
            else { items[i].style.display = "none"; }
        }
    }

    let cart = [];
    
    function updateCartUI() {
        let totalItems = cart.reduce((sum, item) => sum + item.qty, 0);
        let badge = document.getElementById('cartCount');
        badge.innerText = totalItems;
    }

    function showToast() {
        let toast = document.getElementById('toast');
        toast.classList.add('show');
        setTimeout(() => { toast.classList.remove('show'); }, 2000);
    }

    function addToCart(producto) {
        let existingItem = cart.find(item => item.nombre === producto.nombre);
        if (existingItem) {
            existingItem.qty += 1;
        } else {
            producto.qty = 1;
            cart.push(producto);
        }
        updateCartUI();
        showToast();
    }

    function sendOrder(event) {
        event.preventDefault();
        if (cart.length === 0) {
            alert("Tu carrito está vacío. Agrega algún perfume primero.");
            return;
        }
        
        let totalUnidades = cart.reduce((sum, item) => sum + item.qty, 0);
        
        let tipoPrecio = "Detal";
        if (totalUnidades >= 15) {
            tipoPrecio = "Gran Mayor";
        } else if (totalUnidades >= 6) {
            tipoPrecio = "Mayor";
        }
        
        let mensaje = "Hola, quiero hacer el siguiente pedido (" + tipoPrecio + "):\n\n";
        let totalPagar = 0;
        
        cart.forEach(item => {
            let precioUnitario = item.detal;
            if (tipoPrecio === "Gran Mayor") precioUnitario = item.gran_mayor;
            else if (tipoPrecio === "Mayor") precioUnitario = item.mayor;
            
            let subtotal = precioUnitario * item.qty;
            totalPagar += subtotal;
            
            mensaje += "- " + item.qty + "x " + item.nombre + " ($" + precioUnitario.toFixed(2) + " c/u) = $" + subtotal.toFixed(2) + "\n";
        });
        
        mensaje += "\n*Total estimado: $" + totalPagar.toFixed(2) + "*";
        mensaje += "\n\nPor favor, confírmame disponibilidad y método de pago.";
        
        let url = "https://wa.me/584228490047?text=" + encodeURIComponent(mensaje);
        window.location.href = url;
        
        cart = [];
        updateCartUI();
    }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    catalogo, error_msg = cargar_catalogo()
    return render_template_string(HTML_TEMPLATE, catalogo=catalogo, error_msg=error_msg)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
