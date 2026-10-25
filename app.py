import os
import pandas as pd
from flask import Flask, render_template_string, url_for

app = Flask(__name__)

def cargar_catalogo():
    df = pd.read_excel('aroma2.xlsx', sheet_name='catalogo')
    catalogo = []
    
    ruta_carpeta = os.path.join(app.root_path, 'static', 'fotos')
    
    for _, row in df.iterrows():
        nombre = str(row['Nombre'])
        marca = str(row['marca']).strip()
        
        detal = float(row['precio_venta']) if pd.notna(row['precio_venta']) else 0.0
        mayor = float(row['precio_mayor']) if pd.notna(row['precio_mayor']) else 0.0
        gran_mayor = float(row['precio_gran_mayor']) if pd.notna(row['precio_gran_mayor']) else 0.0
        
        slug = nombre.lower().replace(' ', '-').replace("'", "").replace('"', '').replace('&', 'and')
        imagen = f"/static/fotos/{slug}.jpg" 
        
        if os.path.exists(ruta_carpeta):
            for archivo in os.listdir(ruta_carpeta):
                nombre_archivo, extension = os.path.splitext(archivo)
                if nombre_archivo == slug and extension.lower() in ['.jpg', '.jpeg', '.png', '.webp']:
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
            "imagen": imagen
        })
    return catalogo

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Catálogo Digital de Perfumes</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f4f6f8; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0; }
        
        .header-bg { 
            background: linear-gradient(rgba(17, 24, 39, 0.7), rgba(17, 24, 39, 0.7)), url("{{ url_for('static', filename='fotos/banner.jpg') }}");
            background-size: cover;
            background-position: center;
            color: white; 
            text-align: center; 
            border-bottom: 4px solid #d97706; 
            padding: 3rem 1rem; 
        }

        .card-perfume { border: none; border-radius: 12px; transition: transform 0.2s, box-shadow 0.2s; background: #ffffff; }
        .card-perfume:hover { transform: translateY(-3px); box-shadow: 0 10px 20px rgba(0,0,0,0.08); }
        .badge-brand { background-color: #f3f4f6; color: #374151; font-weight: 600; font-size: 0.75rem; padding: 0.35em 0.65em; border-radius: 6px; }
        .price-box { background-color: #f9fafb; border-radius: 8px; padding: 8px; font-size: 0.85rem; border: 1px solid #e5e7eb; }
        .price-detal { font-weight: bold; color: #059669; font-size: 1.05rem; }
        .price-label { color: #6b7280; font-size: 0.75rem; display: block; }
        .img-container { height: 140px; display: flex; align-items: center; justify-content: center; background-color: #fafafa; border-radius: 8px; overflow: hidden; margin-bottom: 10px; }
        .img-container img { max-height: 100%; max-width: 100%; object-fit: contain; }
        
        /* Estilo para el botón de WhatsApp */
        .btn-whatsapp { background-color: #25D366; color: white; font-weight: bold; border: none; }
        .btn-whatsapp:hover { background-color: #1ebe57; color: white; }
    </style>
</head>
<body>

    <div class="header-bg shadow-sm mb-4">
        <h1 class="fw-bold m-0">✨ Catálogo de Perfumes</h1>
        <p class="text-light opacity-75 mt-1 small">Detal, Mayor (6+ unds) y Gran Mayor (15+ unds)</p>
    </div>

    <div class="container pb-5">
        <div class="row justify-content-center mb-4">
            <div class="col-12 col-md-8 col-lg-6">
                <input type="text" id="searchInput" class="form-control form-control-lg shadow-sm" placeholder="🔍 Buscar perfume o marca..." onkeyup="filterProducts()">
            </div>
        </div>

        <div class="row g-3" id="productList">
            {% for item in catalogo %}
            <div class="col-6 col-md-4 col-lg-3 product-item" data-search="{{ item.marca.lower() }} {{ item.producto.lower() }}">
                <div class="card card-perfume h-100 p-3 shadow-sm d-flex flex-column justify-content-between">
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
                        
                        <!-- BOTÓN DE WHATSAPP -->
                        <a href="https://wa.me/584228490047?text=Hola,%20estoy%20interesado%20en%20el%20perfume:%20{{ item.producto | urlencode }}%20-%20Marca:%20{{ item.marca | urlencode }}.%20Precio%20Detal:%20${{ '%.2f'|format(item.detal) }}" 
                           target="_blank" 
                           class="btn btn-whatsapp btn-sm w-100">
                           💬 Pedir por WhatsApp
                        </a>
                        
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>

    <script>
    function filterProducts() {
        let input = document.getElementById('searchInput').value.toLowerCase();
        let items = document.getElementsByClassName('product-item');

        for (let i = 0; i < items.length; i++) {
            let searchData = items[i].getAttribute('data-search');
            if (searchData.includes(input)) {
                items[i].style.display = "";
            } else {
                items[i].style.display = "none";
            }
        }
    }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    catalogo = cargar_catalogo()
    return render_template_string(HTML_TEMPLATE, catalogo=catalogo)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
