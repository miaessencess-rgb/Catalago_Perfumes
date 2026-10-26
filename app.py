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
            descripcion_original = str(row.get('descripcion', '')).strip()
            
            if descripcion_original == 'nan' or not descripcion_original:
                descripcion_original = ""
            
            if not nombre or nombre == 'nan':
                continue

            # --- LÓGICA DE LA ETIQUETA SECRETA ---
            genero = 'Unisex'
            descripcion_limpia = descripcion_original
            
            if descripcion_original.startswith('[H]'):
                genero = 'Hombre'
                descripcion_limpia = descripcion_original[3:].strip()
            elif descripcion_original.startswith('[M]'):
                genero = 'Mujer'
                descripcion_limpia = descripcion_original[3:].strip()
            elif descripcion_original.startswith('[U]'):
                genero = 'Unisex'
                descripcion_limpia = descripcion_original[3:].strip()
            else:
                nombre_lower = nombre.lower()
                if any(w in nombre_lower for w in ['men', 'man', 'hombre', 'sauvage', 'eros', 'bleu', 'one million', 'bad boy', 'elixir']):
                    genero = 'Hombre'
                elif any(w in nombre_lower for w in ['fem', 'woman', 'girl', 'yara', 'good girl', 'libre', 'black opium', 'oud gold']):
                    genero = 'Mujer'

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
                
            catalogo.append({
                "marca": marca,
                "producto": nombre,
                "descripcion": descripcion_limpia,
                "genero": genero,
                "detal": detal,
                "mayor": mayor,
                "gran_mayor": gran_mayor,
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
    <title>Catálogo Digital de Perfumes | Aroma2</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
    
    <style>
        body { background-color: #0a0a0a; font-family: 'Poppins', sans-serif; margin: 0; padding: 0; }
        
        .header-bg { 
            background: linear-gradient(rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.8)), url("{{ url_for('static', filename='fotos/banner.jpg') }}");
            background-size: cover;
            background-position: center;
            color: white; 
            text-align: center; 
            border-bottom: 4px solid #FFD700;
            padding: 3rem 1rem; 
        }

        .logo-header {
            width: 120px; height: 120px; object-fit: cover; 
            margin-bottom: 15px; border-radius: 50%; 
            box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
            border: 4px solid #FFD700; background-color: #000; 
        }

        .tiktok-btn {
            background-color: rgba(255, 255, 255, 0.1);
            color: #fff;
            text-decoration: none;
            padding: 8px 24px;
            border-radius: 30px;
            font-weight: 600;
            font-size: 0.9rem;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            border: 2px solid #FFD700;
            box-shadow: 0 4px 10px rgba(0,0,0,0.4);
            transition: all 0.3s ease;
            margin-top: 15px;
        }
        .tiktok-btn:hover { background-color: #FFD700; color: #000; transform: translateY(-2px); }

        .search-pill {
            border-radius: 50px !important;
            border: 1px solid #333;
            background-color: #1a1a1a;
            color: white;
            padding: 15px 25px;
            font-size: 1.1rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        }
        .search-pill::placeholder { color: #888; }
        .search-pill:focus { background-color: #222; color: white; box-shadow: 0 4px 20px rgba(255, 215, 0, 0.2); border-color: #FFD700; outline: none; }

        .card-perfume { 
            border: 1px solid rgba(255, 255, 255, 0.1); 
            border-radius: 15px; 
            transition: transform 0.3s, box-shadow 0.3s; 
            background-color: rgba(20, 20, 20, 0.85);
            backdrop-filter: blur(10px);
            color: white;
        }
        .card-perfume:hover { transform: translateY(-5px); box-shadow: 0 12px 25px rgba(255, 215, 0, 0.15); border-color: rgba(255, 215, 0, 0.3); }
        
        .badge-brand { background-color: #333; color: #FFD700; font-weight: 600; font-size: 0.75rem; padding: 0.35em 0.65em; border-radius: 6px; }
        
        .price-box { background-color: rgba(0, 0, 0, 0.5); border-radius: 10px; padding: 12px; border: 1px solid rgba(255, 255, 255, 0.05); }
        .price-detal { font-weight: 700; color: #4ade80; font-size: 1.1rem; }
        .price-label { color: #9ca3af; font-size: 0.75rem; display: block; }
        
        /* TRUCO PARA FUNDIR EL FONDO BLANCO CON EL NEGRO */
        .img-container { 
            height: 140px; 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            background-color: #1a1a1a; /* Fondo gris muy oscuro */
            border-radius: 8px; 
            overflow: hidden; 
            margin-bottom: 10px; 
        }
        .img-container img { 
            max-height: 100%; 
            max-width: 100%; 
            object-fit: contain; 
            mix-blend-mode: multiply; /* Hace que el blanco sea transparente */
            filter: contrast(1.1) brightness(0.9); /* Ajusta el brillo para que no se vea opaco */
        }
        
        .card-agotado { opacity: 0.5; filter: grayscale(100%); }
        .badge-agotado { position: absolute; top: 20px; right: 20px; background-color: #dc3545; color: white; font-weight: bold; font-size: 0.8rem; padding: 0.4em 0.7em; border-radius: 6px; z-index: 10; box-shadow: 0 2px 4px rgba(0,0,0,0.5); }

        .btn-whatsapp { background-color: #25D366; color: white; font-weight: 600; border: none; border-radius: 8px; transition: 0.2s; }
        .btn-whatsapp:hover { background-color: #1ebe57; color: white; transform: scale(1.02); box-shadow: 0 0 15px rgba(37, 211, 102, 0.4); }
        .btn-agotado { background-color: #333; color: #888; font-weight: 600; border: none; cursor: not-allowed; border-radius: 8px; }
        
        .descripcion-texto { font-size: 0.75rem; color: #9ca3af; font-weight: 300; line-height: 1.4; margin-bottom: 10px; }
    </style>
</head>
<body>

    <div class="header-bg shadow-sm mb-4">
        <img src="{{ url_for('static', filename='logo.jpg') }}" alt="Mi Logo" class="logo-header">
        <h1 class="fw-bold m-0" style="letter-spacing: 1px; color: white;">✨ Catálogo de Perfumes</h1>
        <p class="text-light opacity-75 mt-2 small" style="font-weight: 300; color: #FFD700 !important;">Detal, Mayor (6+ unds) y Gran Mayor (15+ unds)</p>
        
        <a href="https://www.tiktok.com/@aroma2s" target="_blank" class="tiktok-btn">
            <i class="fab fa-tiktok"></i> Síguenos en TikTok: @aroma2s
        </a>
    </div>

    <div class="container pb-5">
        {% if error_msg %}
        <div class="alert alert-danger text-center">
            <strong>Error al cargar los productos:</strong> {{ error_msg }}
        </div>
        {% endif %}

        <div class="row justify-content-center mb-5">
            <div class="col-12 col-md-8 col-lg-6">
                <input type="text" id="searchInput" class="form-control search-pill" placeholder="🔍 Buscar perfume o marca..." onkeyup="filterProducts()">
            </div>
        </div>

        <div class="row g-3" id="productList">
            {% for item in catalogo %}
            <div class="col-6 col-md-4 col-lg-3 product-item" data-search="{{ item.marca.lower() }} {{ item.producto.lower() }} {{ item.descripcion.lower() }}">
                
                <div class="card card-perfume h-100 p-3 shadow-sm d-flex flex-column justify-content-between position-relative {% if item.stock <= 0 %}card-agotado{% endif %}">
                    
                    {% if item.stock <= 0 %}
                        <div class="badge-agotado">AGOTADO</div>
                    {% endif %}

                    <div>
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <span class="badge badge-brand text-uppercase">{{ item.marca }}</span>
                            
                            {% if item.genero == 'Mujer' %}
                                <span class="badge bg-danger text-white" style="font-size:0.7rem;">Mujer</span>
                            {% elif item.genero == 'Hombre' %}
                                <span class="badge bg-primary text-white" style="font-size:0.7rem;">Hombre</span>
                            {% else %}
                                <span class="badge bg-warning text-dark" style="font-size:0.7rem;">Unisex</span>
                            {% endif %}
                            
                        </div>
                        <div class="img-container">
                            <img src="{{ item.imagen }}" onerror="this.onerror=null; this.parentElement.innerHTML='<span class=\'text-muted small\'>📷 Sin imagen</span>';" alt="{{ item.producto }}">
                        </div>
                        <h6 class="card-title fw-bold mb-1" style="font-size: 0.95rem; color: white;">{{ item.producto }}</h6>
                        
                        {% if item.descripcion %}
                            <p class="descripcion-texto">{{ item.descripcion }}</p>
                        {% endif %}
                        
                    </div>
                    
                    <div class="price-box mt-auto">
                        <div class="d-flex justify-content-between align-items-center mb-1 pb-1 border-bottom border-secondary">
                            <span class="price-label">Detal:</span>
                            <span class="price-detal">${{ "%.2f"|format(item.detal) }}</span>
                        </div>
                        <div class="d-flex justify-content-between align-items-center mb-1">
                            <span class="price-label">Mayor (6+):</span>
                            <span class="fw-bold text-white">${{ "%.2f"|format(item.mayor) }}</span>
                        </div>
                        <div class="d-flex justify-content-between align-items-center mb-3">
                            <span class="price-label">Gran Mayor (15+):</span>
                            <span class="fw-bold" style="color: #60a5fa;">${{ "%.2f"|format(item.gran_mayor) }}</span>
                        </div>
                        
                        {% if item.stock > 0 %}
                            <a href="https://wa.me/584228490047?text=Hola,%20estoy%20interesado%20en%20el%20perfume:%20{{ item.producto | urlencode }}%20-%20Marca:%20{{ item.marca | urlencode }}.%20Precio%20Detal:%20${{ '%.2f'|format(item.detal) }}" target="_blank" class="btn btn-whatsapp btn-sm w-100">
                               💬 Pedir por WhatsApp
                            </a>
                        {% else %}
                            <button class="btn btn-agotado btn-sm w-100" disabled>
                               ❌ Agotado
                            </button>
                        {% endif %}
                        
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
            if (searchData.includes(input)) { items[i].style.display = ""; } 
            else { items[i].style.display = "none"; }
        }
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
