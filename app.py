import os
from flask import Flask, render_template_string

app = Flask(__name__)

# Catálogo completo con costos de proveedor y esquema de 3 niveles (Detal, Mayor, Gran Mayor)
CATALOGO = [
    {"marca": "Afnan", "producto": "9PM Elixir", "detal": 20.0, "mayor": 16.5, "gran_mayor": 14.5, "genero": "Hombre", "imagen": "/static/fotos/9pm-elixir.jpg"},
    {"marca": "Afnan", "producto": "9PM Night Out", "detal": 25.0, "mayor": 19.0, "gran_mayor": 16.5, "genero": "Hombre", "imagen": "/static/fotos/9pm-night-out.jpg"},
    {"marca": "Afnan", "producto": "9AM Unisex", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Unisex", "imagen": "/static/fotos/9am-unisex.jpg"},
    {"marca": "Afnan", "producto": "9AM Dive", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Unisex", "imagen": "/static/fotos/9am-dive.jpg"},
    {"marca": "Afnan", "producto": "9AM Dive Unisex 50ml", "detal": 12.0, "mayor": 9.0, "gran_mayor": 8.0, "genero": "Unisex", "imagen": "/static/fotos/9am-dive-50ml.jpg"},
    {"marca": "Afnan", "producto": "9AM Unisex 50ml", "detal": 12.0, "mayor": 9.0, "gran_mayor": 8.0, "genero": "Unisex", "imagen": "/static/fotos/9am-unisex-50ml.jpg"},
    {"marca": "Afnan", "producto": "9PM Rebel 50ml", "detal": 12.0, "mayor": 9.0, "gran_mayor": 8.0, "genero": "Hombre", "imagen": "/static/fotos/9pm-rebel-50ml.jpg"},
    {"marca": "Al Haramain", "producto": "Amber Oud Exclusif Emerald", "detal": 22.0, "mayor": 18.0, "gran_mayor": 16.5, "genero": "Unisex", "imagen": "/static/fotos/amber-oud-emerald.jpg"},
    {"marca": "Al Haramain", "producto": "Amber Oud Gold Edition", "detal": 22.0, "mayor": 18.0, "gran_mayor": 16.5, "genero": "Unisex", "imagen": "/static/fotos/amber-oud-gold.jpg"},
    {"marca": "Al Haramain", "producto": "Amber Oud Ultra Violet", "detal": 22.0, "mayor": 18.0, "gran_mayor": 16.5, "genero": "Unisex", "imagen": "/static/fotos/amber-oud-ultra-violet.jpg"},
    {"marca": "Amouage", "producto": "Interlude Men", "detal": 15.0, "mayor": 13.0, "gran_mayor": 11.5, "genero": "Hombre", "imagen": "/static/fotos/interlude-men.jpg"},
    {"marca": "Ariana Grande", "producto": "Cloud 2.0", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Mujer", "imagen": "/static/fotos/cloud-2.jpg"},
    {"marca": "Ariana Grande", "producto": "Cloud Fem", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Mujer", "imagen": "/static/fotos/cloud-fem.jpg"},
    {"marca": "Ariana Grande", "producto": "Mod Blush Fem", "detal": 15.0, "mayor": 13.0, "gran_mayor": 11.5, "genero": "Mujer", "imagen": "/static/fotos/mod-blush.jpg"},
    {"marca": "Ariana Grande", "producto": "Mod Vanilla Fem", "detal": 15.0, "mayor": 13.0, "gran_mayor": 11.5, "genero": "Mujer", "imagen": "/static/fotos/mod-vanilla.jpg"},
    {"marca": "Ariana Grande", "producto": "R.E.M. Fem", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Mujer", "imagen": "/static/fotos/rem-fem.jpg"},
    {"marca": "Ariana Grande", "producto": "Thank U Next Fem", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Mujer", "imagen": "/static/fotos/thank-u-next.jpg"},
    {"marca": "Armaf", "producto": "Silver Infinity", "detal": 35.0, "mayor": 28.0, "gran_mayor": 25.0, "genero": "Hombre", "imagen": "/static/fotos/silver-infinity.jpg"},
    {"marca": "Armaf", "producto": "Gold Infinity", "detal": 35.0, "mayor": 28.0, "gran_mayor": 25.0, "genero": "Unisex", "imagen": "/static/fotos/gold-infinity.jpg"},
    {"marca": "Armaf", "producto": "Club de Nuit Lionheart Woman", "detal": 22.0, "mayor": 18.0, "gran_mayor": 16.5, "genero": "Mujer", "imagen": "/static/fotos/cdn-lionheart-woman.jpg"},
    {"marca": "Armaf", "producto": "Club De Nuit Man Intense 105ml", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Hombre", "imagen": "/static/fotos/cdn-man-intense.jpg"},
    {"marca": "Armaf", "producto": "Club De Nuit Milestone", "detal": 22.0, "mayor": 18.0, "gran_mayor": 16.5, "genero": "Unisex", "imagen": "/static/fotos/cdn-milestone.jpg"},
    {"marca": "Armaf", "producto": "Club De Nuit Woman 105ml", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Mujer", "imagen": "/static/fotos/cdn-woman.jpg"},
    {"marca": "Armaf", "producto": "Odyssey Aqua Edition", "detal": 22.0, "mayor": 18.0, "gran_mayor": 16.5, "genero": "Hombre", "imagen": "/static/fotos/odyssey-aqua.jpg"},
    {"marca": "Armaf", "producto": "Odyssey Mandarin Sky", "detal": 22.0, "mayor": 18.0, "gran_mayor": 16.5, "genero": "Hombre", "imagen": "/static/fotos/odyssey-mandarin-sky.jpg"},
    {"marca": "Armaf", "producto": "Club de Nuit Lionheart Man", "detal": 22.0, "mayor": 18.0, "gran_mayor": 16.5, "genero": "Hombre", "imagen": "/static/fotos/cdn-lionheart-man.jpg"},
    {"marca": "Armaf", "producto": "Island Lush", "detal": 35.0, "mayor": 28.0, "gran_mayor": 25.0, "genero": "Unisex", "imagen": "/static/fotos/island-lush.jpg"},
    {"marca": "Armaf", "producto": "Odyssey Candyland", "detal": 22.0, "mayor": 18.0, "gran_mayor": 16.5, "genero": "Mujer", "imagen": "/static/fotos/odyssey-candyland.jpg"},
    {"marca": "Armaf", "producto": "Odyssey Homme White Edition", "detal": 22.0, "mayor": 18.0, "gran_mayor": 16.5, "genero": "Hombre", "imagen": "/static/fotos/odyssey-white.jpg"},
    {"marca": "Armaf", "producto": "Odyssey Limoni", "detal": 22.0, "mayor": 18.0, "gran_mayor": 16.5, "genero": "Unisex", "imagen": "/static/fotos/odyssey-limoni.jpg"},
    {"marca": "Armaf", "producto": "Odyssey Mega", "detal": 22.0, "mayor": 18.0, "gran_mayor": 16.5, "genero": "Hombre", "imagen": "/static/fotos/odyssey-mega.jpg"},
    {"marca": "Armaf", "producto": "Odyssey Tyrant Special Edition", "detal": 22.0, "mayor": 18.0, "gran_mayor": 16.5, "genero": "Hombre", "imagen": "/static/fotos/odyssey-tyrant.jpg"},
    {"marca": "Armaf", "producto": "Odissey Wild One", "detal": 22.0, "mayor": 18.0, "gran_mayor": 16.5, "genero": "Hombre", "imagen": "/static/fotos/odyssey-wild-one.jpg"},
    {"marca": "Bharara", "producto": "Bharara King", "detal": 22.0, "mayor": 18.0, "gran_mayor": 16.5, "genero": "Hombre", "imagen": "/static/fotos/bharara-king.jpg"},
    {"marca": "Bharara", "producto": "King Fast Black", "detal": 22.0, "mayor": 18.0, "gran_mayor": 16.5, "genero": "Hombre", "imagen": "/static/fotos/king-fast-black.jpg"},
    {"marca": "Bharara", "producto": "Onyx Unisex", "detal": 22.0, "mayor": 18.0, "gran_mayor": 16.5, "genero": "Unisex", "imagen": "/static/fotos/onyx-unisex.jpg"},
    {"marca": "Bharara", "producto": "Viking Beirut", "detal": 22.0, "mayor": 18.0, "gran_mayor": 16.5, "genero": "Hombre", "imagen": "/static/fotos/viking-beirut.jpg"},
    {"marca": "Bharara", "producto": "Viking Cayman", "detal": 22.0, "mayor": 18.0, "gran_mayor": 16.5, "genero": "Hombre", "imagen": "/static/fotos/viking-cayman.jpg"},
    {"marca": "Bharara", "producto": "Viking Desert", "detal": 22.0, "mayor": 18.0, "gran_mayor": 16.5, "genero": "Hombre", "imagen": "/static/fotos/viking-desert.jpg"},
    {"marca": "Bharara", "producto": "Viking Double Black", "detal": 22.0, "mayor": 18.0, "gran_mayor": 16.5, "genero": "Hombre", "imagen": "/static/fotos/viking-double-black.jpg"},
    {"marca": "Bharara", "producto": "Viking Kashmir", "detal": 22.0, "mayor": 18.0, "gran_mayor": 16.5, "genero": "Hombre", "imagen": "/static/fotos/viking-kashmir.jpg"},
    {"marca": "Bharara", "producto": "Viking Rio", "detal": 22.0, "mayor": 18.0, "gran_mayor": 16.5, "genero": "Hombre", "imagen": "/static/fotos/viking-rio.jpg"},
    {"marca": "Carolina Herrera", "producto": "212 VIP Black Men", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Hombre", "imagen": "/static/fotos/212-vip-black.jpg"},
    {"marca": "Carolina Herrera", "producto": "212 VIP Rose Fem", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Mujer", "imagen": "/static/fotos/212-vip-rose.jpg"},
    {"marca": "Carolina Herrera", "producto": "212 Sexy Fem", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Mujer", "imagen": "/static/fotos/212-sexy-fem.jpg"},
    {"marca": "Carolina Herrera", "producto": "212 VIP Fem", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Mujer", "imagen": "/static/fotos/212-vip-fem.jpg"},
    {"marca": "Carolina Herrera", "producto": "212 VIP Men", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Hombre", "imagen": "/static/fotos/212-vip-men.jpg"},
    {"marca": "Carolina Herrera", "producto": "Bad Boy Cobalt Men", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Hombre", "imagen": "/static/fotos/bad-boy-cobalt.jpg"},
    {"marca": "Carolina Herrera", "producto": "Bad Boy Extreme Men", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Hombre", "imagen": "/static/fotos/bad-boy-extreme.jpg"},
    {"marca": "Carolina Herrera", "producto": "Bad Boy Men", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Hombre", "imagen": "/static/fotos/bad-boy-men.jpg"},
    {"marca": "Carolina Herrera", "producto": "CH Men", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Hombre", "imagen": "/static/fotos/ch-men.jpg"},
    {"marca": "Carolina Herrera", "producto": "CH Pasión Men", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Hombre", "imagen": "/static/fotos/ch-pasion-men.jpg"},
    {"marca": "Carolina Herrera", "producto": "Good Girl Blush Fem", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Mujer", "imagen": "/static/fotos/good-girl-blush.jpg"},
    {"marca": "Carolina Herrera", "producto": "Good Girl Dazzling Garden", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Mujer", "imagen": "/static/fotos/good-girl-dazzling.jpg"},
    {"marca": "Carolina Herrera", "producto": "Good Girl Fem", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Mujer", "imagen": "/static/fotos/good-girl-fem.jpg"},
    {"marca": "Carolina Herrera", "producto": "Good Girl Midnight Fem", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Mujer", "imagen": "/static/fotos/good-girl-midnight.jpg"},
    {"marca": "Carolina Herrera", "producto": "Good Girl Supreme Fem", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Mujer", "imagen": "/static/fotos/good-girl-supreme.jpg"},
    {"marca": "Carolina Herrera", "producto": "Very Good Girl Fem", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Mujer", "imagen": "/static/fotos/very-good-girl.jpg"},
    {"marca": "Carolina Herrera", "producto": "Very Good Girl Glam Fem", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Mujer", "imagen": "/static/fotos/very-good-girl-glam.jpg"},
    {"marca": "Chanel", "producto": "Bleu De Chanel Men", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Hombre", "imagen": "/static/fotos/bleu-de-chanel.jpg"},
    {"marca": "Chanel", "producto": "Coco Mademoiselle Fem", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Mujer", "imagen": "/static/fotos/coco-mademoiselle.jpg"},
    {"marca": "Creed", "producto": "Aventus 100ml", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Hombre", "imagen": "/static/fotos/creed-aventus.jpg"},
    {"marca": "Christian Dior", "producto": "Fahrenheit Men", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Hombre", "imagen": "/static/fotos/fahrenheit-men.jpg"},
    {"marca": "Christian Dior", "producto": "Sauvage Elixir Men", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Hombre", "imagen": "/static/fotos/sauvage-elixir.jpg"},
    {"marca": "Christian Dior", "producto": "Sauvage Men", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Hombre", "imagen": "/static/fotos/sauvage-men.jpg"},
    {"marca": "Dolce & Gabbana", "producto": "Light Blue Men", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Hombre", "imagen": "/static/fotos/light-blue-men.jpg"},
    {"marca": "Giorgio Armani", "producto": "Acqua Di Gio Men", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Hombre", "imagen": "/static/fotos/acqua-di-gio.jpg"},
    {"marca": "Giorgio Armani", "producto": "Acqua Di Gio Profumo Men", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Hombre", "imagen": "/static/fotos/acqua-di-gio-profumo.jpg"},
    {"marca": "Giorgio Armani", "producto": "My Way Fem", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Mujer", "imagen": "/static/fotos/my-way-fem.jpg"},
    {"marca": "Giorgio Armani", "producto": "Si Passione Fem", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Mujer", "imagen": "/static/fotos/si-passione.jpg"},
    {"marca": "Jean Paul Gaultier", "producto": "Divine Fem", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Mujer", "imagen": "/static/fotos/divine-fem.jpg"},
    {"marca": "Jean Paul Gaultier", "producto": "Le Beau Paradise Garden", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Hombre", "imagen": "/static/fotos/le-beau-paradise.jpg"},
    {"marca": "Jean Paul Gaultier", "producto": "Le Male Elixir Men", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Hombre", "imagen": "/static/fotos/le-male-elixir.jpg"},
    {"marca": "Jean Paul Gaultier", "producto": "La Belle Le Parfum Intense", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Mujer", "imagen": "/static/fotos/la-belle-intense.jpg"},
    {"marca": "Jean Paul Gaultier", "producto": "Le Beau Le Parfum Men", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Hombre", "imagen": "/static/fotos/le-beau-le-parfum.jpg"},
    {"marca": "Jean Paul Gaultier", "producto": "Scandal Absolu Fem", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Mujer", "imagen": "/static/fotos/scandal-absolu-fem.jpg"},
    {"marca": "Jean Paul Gaultier", "producto": "Scandal Absolu Men", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Hombre", "imagen": "/static/fotos/scandal-absolu-men.jpg"},
    {"marca": "Jean Paul Gaultier", "producto": "Scandal Fem", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Mujer", "imagen": "/static/fotos/scandal-fem.jpg"},
    {"marca": "Jean Paul Gaultier", "producto": "Scandal Le Parfum Fem", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Mujer", "imagen": "/static/fotos/scandal-le-parfum-fem.jpg"},
    {"marca": "Jean Paul Gaultier", "producto": "Scandal Le Parfum Men", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Hombre", "imagen": "/static/fotos/scandal-le-parfum-men.jpg"},
    {"marca": "Jean Paul Gaultier", "producto": "Scandal Men", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Hombre", "imagen": "/static/fotos/scandal-men.jpg"},
    {"marca": "Lattafa", "producto": "Al Nashama Caprice", "detal": 25.0, "mayor": 21.0, "gran_mayor": 19.5, "genero": "Unisex", "imagen": "/static/fotos/al-nashama-caprice.jpg"},
    {"marca": "Lattafa", "producto": "Affection Unisex", "detal": 25.0, "mayor": 21.0, "gran_mayor": 19.5, "genero": "Unisex", "imagen": "/static/fotos/affection-unisex.jpg"},
    {"marca": "Lattafa", "producto": "Ajwad Pink to Pink Unisex", "detal": 25.0, "mayor": 21.0, "gran_mayor": 19.5, "genero": "Unisex", "imagen": "/static/fotos/ajwad-pink-to-pink.jpg"},
    {"marca": "Lattafa", "producto": "Ajwad Unisex", "detal": 25.0, "mayor": 21.0, "gran_mayor": 19.5, "genero": "Unisex", "imagen": "/static/fotos/ajwad-unisex.jpg"},
    {"marca": "Lattafa", "producto": "Asad Men", "detal": 25.0, "mayor": 21.0, "gran_mayor": 19.5, "genero": "Hombre", "imagen": "/static/fotos/asad-men.jpg"},
    {"marca": "Lattafa", "producto": "Asad Zanzibar Men", "detal": 25.0, "mayor": 21.0, "gran_mayor": 19.5, "genero": "Hombre", "imagen": "/static/fotos/asad-zanzibar.jpg"},
    {"marca": "Lattafa", "producto": "Bade'e Al Oud Honor & Glory", "detal": 25.0, "mayor": 21.0, "gran_mayor": 19.5, "genero": "Unisex", "imagen": "/static/fotos/badee-honor-glory.jpg"},
    {"marca": "Lattafa", "producto": "Bade'e Al Oud Sublime Unisex", "detal": 25.0, "mayor": 21.0, "gran_mayor": 19.5, "genero": "Unisex", "imagen": "/static/fotos/badee-sublime.jpg"},
    {"marca": "Lattafa", "producto": "Eclaire Fem", "detal": 25.0, "mayor": 21.0, "gran_mayor": 19.5, "genero": "Mujer", "imagen": "/static/fotos/eclaire-fem.jpg"},
    {"marca": "Lattafa", "producto": "Fakhar Black Men", "detal": 25.0, "mayor": 21.0, "gran_mayor": 19.5, "genero": "Hombre", "imagen": "/static/fotos/fakhar-black.jpg"},
    {"marca": "Lattafa", "producto": "Fakhar Extrait Gold Unisex", "detal": 25.0, "mayor": 21.0, "gran_mayor": 19.5, "genero": "Unisex", "imagen": "/static/fotos/fakhar-gold.jpg"},
    {"marca": "Lattafa", "producto": "Fakhar Rose Fem", "detal": 25.0, "mayor": 21.0, "gran_mayor": 19.5, "genero": "Mujer", "imagen": "/static/fotos/fakhar-rose.jpg"},
    {"marca": "Lattafa", "producto": "Hayaati Gold Elixir Unisex", "detal": 25.0, "mayor": 21.0, "gran_mayor": 19.5, "genero": "Unisex", "imagen": "/static/fotos/hayaati-gold.jpg"},
    {"marca": "Lattafa", "producto": "Hayaati Men", "detal": 25.0, "mayor": 21.0, "gran_mayor": 19.5, "genero": "Hombre", "imagen": "/static/fotos/hayaati-men.jpg"},
    {"marca": "Lattafa", "producto": "Khamrah Qahwa Unisex", "detal": 25.0, "mayor": 21.0, "gran_mayor": 19.5, "genero": "Unisex", "imagen": "/static/fotos/khamrah-qahwa.jpg"},
    {"marca": "Lattafa", "producto": "Khamrah Unisex", "detal": 25.0, "mayor": 21.0, "gran_mayor": 19.5, "genero": "Unisex", "imagen": "/static/fotos/khamrah-unisex.jpg"},
    {"marca": "Lattafa", "producto": "Liam Grey Unisex", "detal": 25.0, "mayor": 21.0, "gran_mayor": 19.5, "genero": "Unisex", "imagen": "/static/fotos/liam-grey.jpg"},
    {"marca": "Lattafa", "producto": "Mayar Natural Intense Fem", "detal": 25.0, "mayor": 21.0, "gran_mayor": 19.5, "genero": "Mujer", "imagen": "/static/fotos/mayar-natural-intense.jpg"},
    {"marca": "Lattafa", "producto": "Mayar Fem", "detal": 25.0, "mayor": 21.0, "gran_mayor": 19.5, "genero": "Mujer", "imagen": "/static/fotos/mayar-fem.jpg"},
    {"marca": "Lattafa", "producto": "Musamam White Intense", "detal": 25.0, "mayor": 21.0, "gran_mayor": 19.5, "genero": "Unisex", "imagen": "/static/fotos/musamam-white.jpg"},
    {"marca": "Lattafa", "producto": "Yara Tous Fem", "detal": 25.0, "mayor": 21.0, "gran_mayor": 19.5, "genero": "Mujer", "imagen": "/static/fotos/yara-tous.jpg"},
    {"marca": "Lattafa", "producto": "Yara Moi Fem", "detal": 25.0, "mayor": 21.0, "gran_mayor": 19.5, "genero": "Mujer", "imagen": "/static/fotos/yara-moi.jpg"},
    {"marca": "Lattafa", "producto": "Yara Candy Fem", "detal": 25.0, "mayor": 21.0, "gran_mayor": 19.5, "genero": "Mujer", "imagen": "/static/fotos/yara-candy.jpg"},
    {"marca": "Lattafa", "producto": "Yara Pink Fem", "detal": 25.0, "mayor": 21.0, "gran_mayor": 19.5, "genero": "Mujer", "imagen": "/static/fotos/yara-pink.jpg"},
    {"marca": "Lattafa", "producto": "Yara X3 30ml Set Lujo", "detal": 22.0, "mayor": 18.5, "gran_mayor": 17.5, "genero": "Mujer", "imagen": "/static/fotos/yara-x3-set.jpg"},
    {"marca": "Lattafa", "producto": "Yara X4 30ml Set Lujo", "detal": 35.0, "mayor": 28.0, "gran_mayor": 25.0, "genero": "Mujer", "imagen": "/static/fotos/yara-x4-set.jpg"},
    {"marca": "Louis Vuitton", "producto": "Ombre Nomade Unisex", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Unisex", "imagen": "/static/fotos/ombre-nomade.jpg"},
    {"marca": "Maison Francis Kurkdjian", "producto": "Baccarat Rouge 540 Unisex", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Unisex", "imagen": "/static/fotos/baccarat-rouge-540.jpg"},
    {"marca": "Montblanc", "producto": "Starwalker Men", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Hombre", "imagen": "/static/fotos/starwalker-men.jpg"},
    {"marca": "Moschino", "producto": "Funny Fem", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Mujer", "imagen": "/static/fotos/funny-fem.jpg"},
    {"marca": "Moschino", "producto": "Toy 2 Pearl Unisex", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Unisex", "imagen": "/static/fotos/toy-2-pearl.jpg"},
    {"marca": "Moschino", "producto": "Toy 2 X4 Set Lujo", "detal": 35.0, "mayor": 28.0, "gran_mayor": 25.0, "genero": "Unisex", "imagen": "/static/fotos/toy-2-x4-set.jpg"},
    {"marca": "Moschino", "producto": "Toy 2 X3 Set Lujo", "detal": 22.0, "mayor": 18.5, "gran_mayor": 17.5, "genero": "Unisex", "imagen": "/static/fotos/toy-2-x3-set.jpg"},
    {"marca": "Moschino", "producto": "Toy Boy Men", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Hombre", "imagen": "/static/fotos/toy-boy-men.jpg"},
    {"marca": "Mundus", "producto": "Burj Khalifa Unisex", "detal": 35.0, "mayor": 28.0, "gran_mayor": 25.0, "genero": "Unisex", "imagen": "/static/fotos/burj-khalifa.jpg"},
    {"marca": "Mundus", "producto": "Chichen Itza Unisex", "detal": 35.0, "mayor": 28.0, "gran_mayor": 25.0, "genero": "Unisex", "imagen": "/static/fotos/chichen-itza.jpg"},
    {"marca": "Mundus", "producto": "Empire State", "detal": 35.0, "mayor": 28.0, "gran_mayor": 25.0, "genero": "Unisex", "imagen": "/static/fotos/empire-state.jpg"},
    {"marca": "Mundus", "producto": "Taj Mahal Unisex", "detal": 35.0, "mayor": 28.0, "gran_mayor": 25.0, "genero": "Unisex", "imagen": "/static/fotos/taj-mahal.jpg"},
    {"marca": "Mundus", "producto": "Torre Eiffel", "detal": 35.0, "mayor": 28.0, "gran_mayor": 25.0, "genero": "Unisex", "imagen": "/static/fotos/torre-eiffel.jpg"},
    {"marca": "Nautica", "producto": "Voyage", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Hombre", "imagen": "/static/fotos/nautica-voyage.jpg"},
    {"marca": "Orientica", "producto": "Amber Rouge Unisex", "detal": 22.0, "mayor": 18.0, "gran_mayor": 16.5, "genero": "Unisex", "imagen": "/static/fotos/orientica-amber-rouge.jpg"},
    {"marca": "Orientica", "producto": "Royal Amber Unisex", "detal": 22.0, "mayor": 18.0, "gran_mayor": 16.5, "genero": "Unisex", "imagen": "/static/fotos/orientica-royal-amber.jpg"},
    {"marca": "Orientica", "producto": "Velvet Gold Unisex", "detal": 22.0, "mayor": 18.0, "gran_mayor": 16.5, "genero": "Unisex", "imagen": "/static/fotos/orientica-velvet-gold.jpg"},
    {"marca": "Orientica", "producto": "Arte Bellissimo Romantic Unisex", "detal": 22.0, "mayor": 18.0, "gran_mayor": 16.5, "genero": "Unisex", "imagen": "/static/fotos/arte-bellissimo-romantic.jpg"},
    {"marca": "Parfums de Marly", "producto": "Delina Exclusif Fem", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Mujer", "imagen": "/static/fotos/delina-exclusif.jpg"},
    {"marca": "Paris Hilton", "producto": "Can Can Fem", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Mujer", "imagen": "/static/fotos/can-can-fem.jpg"},
    {"marca": "Paris Hilton", "producto": "Heirness Fem", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Mujer", "imagen": "/static/fotos/heiress-fem.jpg"},
    {"marca": "Paris Hilton", "producto": "Paris Hilton Fem", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Mujer", "imagen": "/static/fotos/paris-hilton-fem.jpg"},
    {"marca": "Perry Ellis", "producto": "360 Red Men", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Hombre", "imagen": "/static/fotos/360-red-men.jpg"},
    {"marca": "Perry Ellis", "producto": "360 Red Fem", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Mujer", "imagen": "/static/fotos/360-red-fem.jpg"},
    {"marca": "Perry Ellis", "producto": "360 Very Blue Men", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Hombre", "imagen": "/static/fotos/360-very-blue.jpg"},
    {"marca": "Prada", "producto": "Paradoxe Intense Fem", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Mujer", "imagen": "/static/fotos/paradoxe-intense.jpg"},
    {"marca": "Rabanne", "producto": "Invictus Victory Elixir Men", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Hombre", "imagen": "/static/fotos/invictus-victory-elixir.jpg"},
    {"marca": "Rabanne", "producto": "Phantom Men", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Hombre", "imagen": "/static/fotos/phantom-men.jpg"},
    {"marca": "Rabanne", "producto": "Pure XS Men", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Hombre", "imagen": "/static/fotos/pure-xs-men.jpg"},
    {"marca": "Rabanne", "producto": "Fame Couture Fem", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Mujer", "imagen": "/static/fotos/fame-couture.jpg"},
    {"marca": "Rabanne", "producto": "Fame Fem", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Mujer", "imagen": "/static/fotos/fame-fem.jpg"},
    {"marca": "Rabanne", "producto": "Fame Parfum Fem", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Mujer", "imagen": "/static/fotos/fame-parfum.jpg"},
    {"marca": "Rabanne", "producto": "Million Gold Fem", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Mujer", "imagen": "/static/fotos/million-gold-fem.jpg"},
    {"marca": "Rabanne", "producto": "Olympéa Fem", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Mujer", "imagen": "/static/fotos/olympea-fem.jpg"},
    {"marca": "Rabanne", "producto": "One Million Lucky Men", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Hombre", "imagen": "/static/fotos/one-million-lucky.jpg"},
    {"marca": "Rabanne", "producto": "One Million Prive Men", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Hombre", "imagen": "/static/fotos/one-million-prive.jpg"},
    {"marca": "Rabanne", "producto": "One Million Royal Men", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Hombre", "imagen": "/static/fotos/one-million-royal.jpg"},
    {"marca": "Ralph Lauren", "producto": "Ralph Fem", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Mujer", "imagen": "/static/fotos/ralph-fem.jpg"},
    {"marca": "Ralph Lauren", "producto": "Love Fem", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Mujer", "imagen": "/static/fotos/love-fem.jpg"},
    {"marca": "Swiss Arabian", "producto": "Shaghaf Oud Tonka Unisex", "detal": 22.0, "mayor": 18.0, "gran_mayor": 16.5, "genero": "Unisex", "imagen": "/static/fotos/shaghaf-oud-tonka.jpg"},
    {"marca": "Swiss Arabian", "producto": "Shaghaf Oud Unisex", "detal": 22.0, "mayor": 18.0, "gran_mayor": 16.5, "genero": "Unisex", "imagen": "/static/fotos/shaghaf-oud.jpg"},
    {"marca": "Tom Ford", "producto": "Black Orchid Unisex", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Unisex", "imagen": "/static/fotos/black-orchid.jpg"},
    {"marca": "Tom Ford", "producto": "Lost Cherry Unisex", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Unisex", "imagen": "/static/fotos/lost-cherry.jpg"},
    {"marca": "Tom Ford", "producto": "Ombre Leather Men", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Hombre", "imagen": "/static/fotos/ombre-leather.jpg"},
    {"marca": "Tom Ford", "producto": "Tobacco Vanille Unisex", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Unisex", "imagen": "/static/fotos/tobacco-vanille.jpg"},
    {"marca": "Tommy Hilfiger", "producto": "Tommy Girl Fem", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Mujer", "imagen": "/static/fotos/tommy-girl.jpg"},
    {"marca": "Tommy Hilfiger", "producto": "Tommy Men", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Hombre", "imagen": "/static/fotos/tommy-men.jpg"},
    {"marca": "Versace", "producto": "Eros Flame Men", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Hombre", "imagen": "/static/fotos/eros-flame.jpg"},
    {"marca": "Versace", "producto": "Eros Men", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Hombre", "imagen": "/static/fotos/eros-men.jpg"},
    {"marca": "Versace", "producto": "Eros Pour Femme", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Mujer", "imagen": "/static/fotos/eros-pour-femme.jpg"},
    {"marca": "Versace", "producto": "Yellow Diamond Fem", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Mujer", "imagen": "/static/fotos/yellow-diamond.jpg"},
    {"marca": "Versace", "producto": "Bright Crystal Fem", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Mujer", "imagen": "/static/fotos/bright-crystal.jpg"},
    {"marca": "Victoria's Secret", "producto": "Bombshell Fem", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Mujer", "imagen": "/static/fotos/bombshell-fem.jpg"},
    {"marca": "Viktor & Rolf", "producto": "Flowerbomb Fem", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Mujer", "imagen": "/static/fotos/flowerbomb-fem.jpg"},
    {"marca": "Viktor & Rolf", "producto": "Spicebomb Night Vision Men", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Hombre", "imagen": "/static/fotos/spicebomb-night-vision.jpg"},
    {"marca": "Xerjoff", "producto": "Erba Pura Unisex", "detal": 35.0, "mayor": 28.0, "gran_mayor": 25.0, "genero": "Unisex", "imagen": "/static/fotos/erba-pura.jpg"},
    {"marca": "Yves Saint Laurent", "producto": "Black Opium Fem", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Mujer", "imagen": "/static/fotos/black-opium.jpg"},
    {"marca": "Yves Saint Laurent", "producto": "Y Men", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Hombre", "imagen": "/static/fotos/y-men.jpg"},
    {"marca": "Yves Saint Laurent", "producto": "Y Elixir Men", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Hombre", "imagen": "/static/fotos/y-elixir.jpg"},
    {"marca": "Yves Saint Laurent", "producto": "Libre Fem", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Mujer", "imagen": "/static/fotos/libre-fem.jpg"},
    {"marca": "Yves Saint Laurent", "producto": "Myslf Men", "detal": 20.0, "mayor": 16.0, "gran_mayor": 14.0, "genero": "Hombre", "imagen": "/static/fotos/myslf-men.jpg"}
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Catálogo Digital de Perfumes</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f4f6f8; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .header-bg { background: linear-gradient(135deg, #111827 0%, #1f2937 100%); color: white; padding: 2.5rem 1rem; text-align: center; border-bottom: 4px solid #d97706; }
        .card-perfume { border: none; border-radius: 12px; transition: transform 0.2s, box-shadow 0.2s; background: #ffffff; }
        .card-perfume:hover { transform: translateY(-3px); box-shadow: 0 10px 20px rgba(0,0,0,0.08); }
        .badge-brand { background-color: #f3f4f6; color: #374151; font-weight: 600; font-size: 0.75rem; padding: 0.35em 0.65em; border-radius: 6px; }
        .price-box { background-color: #f9fafb; border-radius: 8px; padding: 8px; font-size: 0.85rem; border: 1px solid #e5e7eb; }
        .price-detal { font-weight: bold; color: #059669; font-size: 1.05rem; }
        .price-label { color: #6b7280; font-size: 0.75rem; display: block; }
        .img-container { height: 140px; display: flex; align-items: center; justify-content: center; background-color: #fafafa; border-radius: 8px; overflow: hidden; margin-bottom: 10px; }
        .img-container img { max-height: 100%; max-width: 100%; object-fit: contain; }
    </style>
</head>
<body>

    <div class="header-bg shadow-sm mb-4">
        <h1 class="fw-bold m-0">✨ Catálogo de Perfumes</h1>
        <p class="text-light opacity-75 mt-1 small">Precios al Detal, Mayor y Gran Mayor</p>
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

                        <!-- Tarjeta de Imagen -->
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
                            <span class="price-label">Al Mayor:</span>
                            <span class="fw-bold text-dark">${{ "%.2f"|format(item.mayor) }}</span>
                        </div>
                        <div class="d-flex justify-content-between align-items-center">
                            <span class="price-label">Gran Mayor:</span>
                            <span class="fw-bold text-primary">${{ "%.2f"|format(item.gran_mayor) }}</span>
                        </div>
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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
