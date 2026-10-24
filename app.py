from flask import Flask, render_template_string, request

app = Flask(__name__)

# Base de datos organizada por Marca / Casa de Perfume
# Nota: Puedes actualizar los precios directamente en este diccionario
CATALOGO = [
    {"marca": "AFNAN", "producto": "9PM Elixir", "precio": 0, "genero": "Unisex"},
    {"marca": "AFNAN", "producto": "9PM Night Out", "precio": 0, "genero": "Hombre"},
    {"marca": "AFNAN", "producto": "9AM Unisex (100ml)", "precio": 0, "genero": "Unisex"},
    {"marca": "AFNAN", "producto": "9AM Unisex (50ml)", "precio": 0, "genero": "Unisex"},
    {"marca": "AFNAN", "producto": "9AM Dive (100ml)", "precio": 0, "genero": "Unisex"},
    {"marca": "AFNAN", "producto": "9AM Dive (50ml)", "precio": 0, "genero": "Unisex"},
    {"marca": "AFNAN", "producto": "9PM Rebel (50ml)", "precio": 0, "genero": "Hombre"},
    
    {"marca": "AL HARAMAIN", "producto": "Amber Oud Exclusif Emerald Unisex", "precio": 0, "genero": "Unisex"},
    {"marca": "AL HARAMAIN", "producto": "Amber Oud Gold Edition Unisex", "precio": 0, "genero": "Unisex"},
    {"marca": "AL HARAMAIN", "producto": "Amber Oud Ultra Violet Fem", "precio": 0, "genero": "Mujer"},
    
    {"marca": "AMOUAGE", "producto": "Interlude Men", "precio": 0, "genero": "Hombre"},
    
    {"marca": "ARIANA GRANDE", "producto": "Cloud 2.0", "precio": 0, "genero": "Mujer"},
    {"marca": "ARIANA GRANDE", "producto": "Cloud Fem", "precio": 0, "genero": "Mujer"},
    {"marca": "ARIANA GRANDE", "producto": "Mod Blush Fem", "precio": 0, "genero": "Mujer"},
    {"marca": "ARIANA GRANDE", "producto": "Mod Vanilla Fem", "precio": 0, "genero": "Mujer"},
    {"marca": "ARIANA GRANDE", "producto": "R.E.M. Fem", "precio": 0, "genero": "Mujer"},
    {"marca": "ARIANA GRANDE", "producto": "Thank U Next Fem", "precio": 0, "genero": "Mujer"},
    
    {"marca": "ARMAF", "producto": "Silver Infinity", "precio": 0, "genero": "Unisex"},
    {"marca": "ARMAF", "producto": "Gold Infinity", "precio": 0, "genero": "Unisex"},
    {"marca": "ARMAF", "producto": "Club de Nuit Lionheart Woman Fem", "precio": 0, "genero": "Mujer"},
    {"marca": "ARMAF", "producto": "Club de Nuit X3 30ml Set Lujo (Intense Man, Milestone, Sillage)", "precio": 0, "genero": "Unisex"},
    {"marca": "ARMAF", "producto": "Club de Nuit Parfum A Collector’s Pride X3 30ml Set Lujo", "precio": 0, "genero": "Unisex"},
    {"marca": "ARMAF", "producto": "Club de Nuit Untold", "precio": 0, "genero": "Unisex"},
    {"marca": "ARMAF", "producto": "Club de Nuit Milestone Unisex", "precio": 0, "genero": "Unisex"},
    {"marca": "ARMAF", "producto": "Club de Nuit Oud Unisex", "precio": 0, "genero": "Unisex"},
    {"marca": "ARMAF", "producto": "Beach Party", "precio": 0, "genero": "Unisex"},
    {"marca": "ARMAF", "producto": "Odyssey Mandarin Sky", "precio": 0, "genero": "Hombre"},
    {"marca": "ARMAF", "producto": "Odyssey Mandarin Sky Elixir Unisex", "precio": 0, "genero": "Unisex"},
    {"marca": "ARMAF", "producto": "Odyssey Mandarin Sky Vintage", "precio": 0, "genero": "Hombre"},
    {"marca": "ARMAF", "producto": "Odyssey Aoud Men", "precio": 0, "genero": "Hombre"},
    {"marca": "ARMAF", "producto": "Odyssey Set Lujo X3 (Candee, Mandarin Sky, Dubai Chocolat)", "precio": 0, "genero": "Unisex"},
    {"marca": "ARMAF", "producto": "Odyssey Homme Men", "precio": 0, "genero": "Hombre"},
    {"marca": "ARMAF", "producto": "Odyssey Mega Men", "precio": 0, "genero": "Hombre"},
    {"marca": "ARMAF", "producto": "Odyssey Tyrant Men", "precio": 0, "genero": "Hombre"},
    {"marca": "ARMAF", "producto": "Odyssey Wild One Gold Edition Men", "precio": 0, "genero": "Hombre"},
    {"marca": "ARMAF", "producto": "Island Breeze Unisex Lujo Premium", "precio": 0, "genero": "Unisex"},
    {"marca": "ARMAF", "producto": "Bon Bon", "precio": 0, "genero": "Mujer"},
    {"marca": "ARMAF", "producto": "Island Bliss Fem", "precio": 0, "genero": "Mujer"},
    {"marca": "ARMAF", "producto": "Yum Yum Fem", "precio": 0, "genero": "Mujer"},
    
    {"marca": "BHARARA", "producto": "King Soleil Unisex Lujo Premium", "precio": 0, "genero": "Unisex"},
    {"marca": "BHARARA", "producto": "Queen Fem", "precio": 0, "genero": "Mujer"},
    {"marca": "BHARARA", "producto": "Rose Fem", "precio": 0, "genero": "Mujer"},
    {"marca": "BHARARA", "producto": "Viking Dubai", "precio": 0, "genero": "Unisex"},
    {"marca": "BHARARA", "producto": "Viking Beirut", "precio": 0, "genero": "Unisex"},
    {"marca": "BHARARA", "producto": "Viking Cairo", "precio": 0, "genero": "Unisex"},
    {"marca": "BHARARA", "producto": "Viking Kashmir", "precio": 0, "genero": "Unisex"},
    {"marca": "BHARARA", "producto": "Scarlet Fem", "precio": 0, "genero": "Mujer"},
    
    {"marca": "BRITNEY SPEARS", "producto": "Fantasy Midnight", "precio": 0, "genero": "Mujer"},
    {"marca": "BRITNEY SPEARS", "producto": "Fantasy Circus", "precio": 0, "genero": "Mujer"},
    
    {"marca": "BVLGARI", "producto": "Man Extreme Men", "precio": 0, "genero": "Hombre"},
    {"marca": "BVLGARI", "producto": "Man In Black Men", "precio": 0, "genero": "Hombre"},
    {"marca": "BVLGARI", "producto": "Omnia Coral Fem", "precio": 0, "genero": "Mujer"},
    {"marca": "BVLGARI", "producto": "Man Wood Essence Men", "precio": 0, "genero": "Hombre"},
    {"marca": "BVLGARI", "producto": "Aqva Pour Homme Men", "precio": 0, "genero": "Hombre"},
    
    {"marca": "CAROLINA HERRERA", "producto": "212 Fem", "precio": 0, "genero": "Mujer"},
    {"marca": "CAROLINA HERRERA", "producto": "212 Men NYC", "precio": 0, "genero": "Hombre"},
    {"marca": "CAROLINA HERRERA", "producto": "212 VIP Black Men", "precio": 0, "genero": "Hombre"},
    {"marca": "CAROLINA HERRERA", "producto": "212 VIP Wins Men", "precio": 0, "genero": "Hombre"},
    {"marca": "CAROLINA HERRERA", "producto": "212 VIP Rosé Fem", "precio": 0, "genero": "Mujer"},
    
    {"marca": "CHANEL", "producto": "Allure Homme Sport Men", "precio": 0, "genero": "Hombre"},
    {"marca": "CHANEL", "producto": "No 5 Eau de Parfum Fem", "precio": 0, "genero": "Mujer"},
    
    {"marca": "DEVIER", "producto": "Oud Silence Unisex", "precio": 0, "genero": "Unisex"},
    {"marca": "DEVIER", "producto": "D' Christian Unisex", "precio": 0, "genero": "Unisex"},
    {"marca": "DEVIER", "producto": "Fresh Orient Unisex", "precio": 0, "genero": "Unisex"},
    {"marca": "DEVIER", "producto": "Silver Danger Unisex", "precio": 0, "genero": "Unisex"},
    {"marca": "DEVIER", "producto": "D' Narcoide Unisex", "precio": 0, "genero": "Unisex"},
    
    {"marca": "DIOR", "producto": "Sauvage Parfum Men", "precio": 0, "genero": "Hombre"},
    
    {"marca": "DOLCE & GABBANA", "producto": "Devotion Fem", "precio": 0, "genero": "Mujer"},
    {"marca": "DOLCE & GABBANA", "producto": "Light Blue Fem", "precio": 0, "genero": "Mujer"},
    
    {"marca": "ESCADA", "producto": "Rockin' Rio Fem", "precio": 0, "genero": "Mujer"},
    
    {"marca": "FRENCH AVENUE", "producto": "Vulcan Feu", "precio": 0, "genero": "Unisex"},
    {"marca": "FRENCH AVENUE", "producto": "Vulcan Sable Unisex Lujo Premium", "precio": 0, "genero": "Unisex"},
    
    {"marca": "GIVENCHY", "producto": "Ange Ou Demon Fem", "precio": 0, "genero": "Mujer"},
    
    {"marca": "HUGO BOSS", "producto": "Bottled Men", "precio": 0, "genero": "Hombre"},
    {"marca": "HUGO BOSS", "producto": "Bottled Night Men", "precio": 0, "genero": "Hombre"},
    
    {"marca": "INITIO", "producto": "Oud For Greatness Unisex", "precio": 0, "genero": "Unisex"},
    
    {"marca": "INVICTUS", "producto": "Parfum Men", "precio": 0, "genero": "Hombre"},
    
    {"marca": "JUICY COUTURE", "producto": "Viva La Juicy", "precio": 0, "genero": "Mujer"},
    
    {"marca": "KATY PERRY", "producto": "Purr Fem", "precio": 0, "genero": "Mujer"},
    {"marca": "KATY PERRY", "producto": "Meow", "precio": 0, "genero": "Mujer"},
    
    {"marca": "LACOSTE", "producto": "Blue Men", "precio": 0, "genero": "Hombre"},
    {"marca": "LACOSTE", "producto": "Essential Men", "precio": 0, "genero": "Hombre"},
    {"marca": "LACOSTE", "producto": "Green Men", "precio": 0, "genero": "Hombre"},
    {"marca": "LACOSTE", "producto": "Natural Fem", "precio": 0, "genero": "Mujer"},
    {"marca": "LACOSTE", "producto": "Red Men", "precio": 0, "genero": "Hombre"},
    {"marca": "LACOSTE", "producto": "Rouge Energetic Men", "precio": 0, "genero": "Hombre"},
    {"marca": "LACOSTE", "producto": "White Men", "precio": 0, "genero": "Hombre"},
    
    {"marca": "LANCOME", "producto": "La Vie Est Belle Fem", "precio": 0, "genero": "Mujer"},
    
    {"marca": "LATTAFA", "producto": "Asad Men", "precio": 0, "genero": "Hombre"},
    {"marca": "LATTAFA", "producto": "Bade'e Al Oud Amethyst Unisex", "precio": 0, "genero": "Unisex"},
    {"marca": "LATTAFA", "producto": "Bade'e Al Oud Oud For Glory Unisex", "precio": 0, "genero": "Unisex"},
    {"marca": "LATTAFA", "producto": "Bade'e Al Oud Honor & Glory Unisex", "precio": 0, "genero": "Unisex"},
    {"marca": "LATTAFA", "producto": "Noble Blush Fem", "precio": 0, "genero": "Mujer"},
    {"marca": "LATTAFA", "producto": "Bade'e Al Oud 30ml Set Lujo", "precio": 0, "genero": "Unisex"},
    {"marca": "LATTAFA", "producto": "Choco Overdose Fem", "precio": 0, "genero": "Mujer"},
    {"marca": "LATTAFA", "producto": "Cookie Crave Fem", "precio": 0, "genero": "Mujer"},
    {"marca": "LATTAFA", "producto": "Mallow Madness Fem", "precio": 0, "genero": "Mujer"},
    {"marca": "LATTAFA", "producto": "Vanilla Freak - Give Me Gourmand", "precio": 0, "genero": "Unisex"},
    {"marca": "LATTAFA", "producto": "Whipped Pleasure - Give Me Gourmand", "precio": 0, "genero": "Unisex"},
    {"marca": "LATTAFA", "producto": "Sehr", "precio": 0, "genero": "Unisex"},
    {"marca": "LATTAFA", "producto": "Atheeri", "precio": 0, "genero": "Unisex"},
    {"marca": "LATTAFA", "producto": "Emeer", "precio": 0, "genero": "Unisex"},
    {"marca": "LATTAFA", "producto": "Fakhar Extrait Men", "precio": 0, "genero": "Hombre"},
    {"marca": "LATTAFA", "producto": "Her Confession Fem", "precio": 0, "genero": "Mujer"},
    {"marca": "LATTAFA", "producto": "His Confession Men", "precio": 0, "genero": "Hombre"},
    {"marca": "LATTAFA", "producto": "Khamrah Zangam Unisex", "precio": 0, "genero": "Unisex"},
    {"marca": "LATTAFA", "producto": "Khamrah Karaz Unisex", "precio": 0, "genero": "Unisex"},
    {"marca": "LATTAFA", "producto": "Set Khamrah 3x 35ml (Clásica, Dukhan, Qahwa)", "precio": 0, "genero": "Unisex"},
    {"marca": "LATTAFA", "producto": "Yara Candy Fem", "precio": 0, "genero": "Mujer"},
    {"marca": "LATTAFA", "producto": "Yara Fem", "precio": 0, "genero": "Mujer"},
    {"marca": "LATTAFA", "producto": "Yara Moi Fem", "precio": 0, "genero": "Mujer"},
    {"marca": "LATTAFA", "producto": "Yara Tous Fem", "precio": 0, "genero": "Mujer"},
    {"marca": "LATTAFA", "producto": "Yara X3 30ml Set Lujo", "precio": 0, "genero": "Mujer"},
    {"marca": "LATTAFA", "producto": "Yara X4 30ml Set Lujo", "precio": 0, "genero": "Mujer"},
    {"marca": "LATTAFA", "producto": "Mayar Natural Intense Fem", "precio": 0, "genero": "Mujer"},
    {"marca": "LATTAFA", "producto": "Mayar Fem", "precio": 0, "genero": "Mujer"},
    
    {"marca": "LOUIS VUITTON", "producto": "Ombre Nomade Unisex", "precio": 0, "genero": "Unisex"},
    {"marca": "MAISON FRANCIS KURKDJIAN", "producto": "Baccarat Rouge 540 Unisex", "precio": 0, "genero": "Unisex"},
    {"marca": "MONTBLANC", "producto": "Starwalker Men", "precio": 0, "genero": "Hombre"},
    
    {"marca": "MOSCHINO", "producto": "Funny Fem", "precio": 0, "genero": "Mujer"},
    {"marca": "MOSCHINO", "producto": "Toy 2 Pearl Unisex", "precio": 0, "genero": "Unisex"},
    {"marca": "MOSCHINO", "producto": "Toy 2 X4 Set Lujo", "precio": 0, "genero": "Unisex"},
    {"marca": "MOSCHINO", "producto": "Toy 2 X3 Set Lujo", "precio": 0, "genero": "Unisex"},
    {"marca": "MOSCHINO", "producto": "Toy Boy Men", "precio": 0, "genero": "Hombre"},
    
    {"marca": "MUNDUS", "producto": "Burj Khalifa Unisex", "precio": 0, "genero": "Unisex"},
    {"marca": "MUNDUS", "producto": "Chichen Itza Unisex", "precio": 0, "genero": "Unisex"},
    {"marca": "MUNDUS", "producto": "Empire State", "precio": 0, "genero": "Unisex"},
    {"marca": "MUNDUS", "producto": "Taj Mahal Unisex", "precio": 0, "genero": "Unisex"},
    {"marca": "MUNDUS", "producto": "Torre Eiffel", "precio": 0, "genero": "Unisex"},
    
    {"marca": "NAUTICA", "producto": "Voyage", "precio": 0, "genero": "Hombre"},
    
    {"marca": "ORIENTICA", "producto": "Premium - Royal Amber Unisex", "precio": 0, "genero": "Unisex"},
    {"marca": "ORIENTICA", "producto": "Premium - Velvet Gold Unisex", "precio": 0, "genero": "Unisex"},
    {"marca": "ORIENTICA", "producto": "Premium - Oud Saffron Unisex", "precio": 0, "genero": "Unisex"},
    {"marca": "ORIENTICA", "producto": "Premium - Noble Unisex", "precio": 0, "genero": "Unisex"},
    {"marca": "ORIENTICA", "producto": "Dania Fem", "precio": 0, "genero": "Mujer"},
    
    {"marca": "PARFUMS DE MARLY", "producto": "Delina Fem", "precio": 0, "genero": "Mujer"},
    
    {"marca": "PARIS HILTON", "producto": "Can Can Fem", "precio": 0, "genero": "Mujer"},
    {"marca": "PARIS HILTON", "producto": "Dazzle Fem", "precio": 0, "genero": "Mujer"},
    {"marca": "PARIS HILTON", "producto": "Heiress Fem", "precio": 0, "genero": "Mujer"},
    
    {"marca": "PERRY ELLIS", "producto": "360° Coral Fem", "precio": 0, "genero": "Mujer"},
    {"marca": "PERRY ELLIS", "producto": "360° Fem", "precio": 0, "genero": "Mujer"},
    {"marca": "PERRY ELLIS", "producto": "360° Men", "precio": 0, "genero": "Hombre"},
    
    {"marca": "PRADA", "producto": "Paradoxe", "precio": 0, "genero": "Mujer"},
    
    {"marca": "RABANNE", "producto": "Black XS Aphrodisiaque Men", "precio": 0, "genero": "Hombre"},
    {"marca": "RABANNE", "producto": "Black XS L'Exces Men", "precio": 0, "genero": "Hombre"},
    {"marca": "RABANNE", "producto": "Black XS Men", "precio": 0, "genero": "Hombre"},
    {"marca": "RABANNE", "producto": "Pure XS Men", "precio": 0, "genero": "Hombre"},
    {"marca": "RABANNE", "producto": "Fame Couture Fem", "precio": 0, "genero": "Mujer"},
    {"marca": "RABANNE", "producto": "Fame Fem", "precio": 0, "genero": "Mujer"},
    {"marca": "RABANNE", "producto": "Fame Parfum Fem", "precio": 0, "genero": "Mujer"},
    {"marca": "RABANNE", "producto": "Million Gold Fem", "precio": 0, "genero": "Mujer"},
    {"marca": "RABANNE", "producto": "Olympéa Fem", "precio": 0, "genero": "Mujer"},
    {"marca": "RABANNE", "producto": "One Million Lucky Men", "precio": 0, "genero": "Hombre"},
    {"marca": "RABANNE", "producto": "One Million Prive Men", "precio": 0, "genero": "Hombre"},
    {"marca": "RABANNE", "producto": "One Million Royal Men", "precio": 0, "genero": "Hombre"},
    
    {"marca": "RALPH LAUREN", "producto": "Ralph Fem", "precio": 0, "genero": "Mujer"},
    {"marca": "RALPH LAUREN", "producto": "Love Fem", "precio": 0, "genero": "Mujer"},
    
    {"marca": "TOMMY HILFIGER", "producto": "Men", "precio": 0, "genero": "Hombre"},
    {"marca": "VALENTINO", "producto": "Donna", "precio": 0, "genero": "Mujer"},
    {"marca": "VERSACE", "producto": "Eros Energy Men", "precio": 0, "genero": "Hombre"},
    {"marca": "VERSACE", "producto": "Yellow Diamond Fem", "precio": 0, "genero": "Mujer"},
    {"marca": "XERJOFF", "producto": "Erba Pura", "precio": 0, "genero": "Unisex"}
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Catálogo de Fragancias</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f8f9fa; font-family: 'Segoe UI', sans-serif; }
        .header-bg { background: linear-gradient(135deg, #111827, #1f2937); color: #fff; padding: 2rem 1rem; }
        .card-perfume { border: none; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); transition: transform 0.2s; }
        .card-perfume:hover { transform: translateY(-3px); }
        .badge-brand { background-color: #e5e7eb; color: #374151; font-size: 0.75rem; font-weight: 600; }
        .badge-gender { font-size: 0.7rem; }
    </style>
</head>
<body>

<div class="header-bg text-center mb-4">
    <h1 class="fw-bold">Catálogo de Fragancias</h1>
    <p class="mb-0 text-muted">Explora nuestra colección de perfumes disponibles</p>
</div>

<div class="container mb-5">
    <!-- Buscador en tiempo real -->
    <div class="row justify-content-center mb-4">
        <div class="col-md-6">
            <input type="text" id="searchInput" class="form-control form-control-lg shadow-sm" placeholder="Buscar por perfume, marca o género..." onkeyup="filterProducts()">
        </div>
    </div>

    <!-- Lista de Productos -->
    <div class="row g-3" id="productList">
        {% for item in catalogo %}
        <div class="col-6 col-md-4 col-lg-3 product-item" data-search="{{ item.marca.lower() }} {{ item.producto.lower() }} {{ item.genero.lower() }}">
            <div class="card card-perfume h-100 p-3">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <span class="badge badge-brand text-uppercase">{{ item.marca }}</span>
                    {% if item.genero == 'Mujer' %}
                        <span class="badge bg-danger-subtle text-danger badge-gender">Fem</span>
                    {% elif item.genero == 'Hombre' %}
                        <span class="badge bg-primary-subtle text-primary badge-gender">Men</span>
                    {% else %}
                        <span class="badge bg-warning-subtle text-warning badge-gender">Unisex</span>
                    {% endif %}
                </div>
                <h6 class="card-title fw-bold text-dark mb-2" style="font-size: 0.95rem;">{{ item.producto }}</h6>
                <div class="mt-auto pt-2 border-top d-flex justify-content-between align-items-center">
                    <span class="text-muted small">Precio:</span>
                    <span class="fw-bold text-success">${{ item.precio if item.precio > 0 else ' Consultar' }}</span>
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
    return render_template_string(HTML_TEMPLATE, catalogo=CATALOGO)

if __name__ == '__main__':
    app.run(debug=True)
