from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import datetime

app = FastAPI()

sehir_detaylari = {
    "Adana": {"duraklar": ["🚌 154 - 2 dk", "🚌 172 - Yakın", "🚌 İtimat 1 - 15 dk"], "koordinat": [36.9914, 35.3308], "zoom": 14},
    "İstanbul": {"duraklar": ["🚇 Metro - 1 dk", "🚢 Vapur - 5 dk", "🚌 500T - Durakta"], "koordinat": [41.0082, 28.9784], "zoom": 12},
    "Ankara": {"duraklar": ["🚇 Ankaray - 3 dk", "🚌 EGO 413 - 10 dk"], "koordinat": [39.9334, 32.8597], "zoom": 13}
}

@app.get("/", response_class=HTMLResponse)
async def read_root(sehir: str = "Adana"):
    simdi = datetime.datetime.now().strftime("%H:%M")
    detay = sehir_detaylari.get(sehir, sehir_detaylari["Adana"])
    otobus_listesi_html = "".join([f"<li>{hat}</li>" for hat in detay["duraklar"]])
    lat, lon, zoom = detay["koordinat"][0], detay["koordinat"][1], detay["zoom"]

    return f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Belediyem Smart 🛸</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <style>
            :root {{ --ana-mavi: #3b82f6; --koyu-mavi: #1e3a8a; --acik-mavi: #eff6ff; }}
            * {{ box-sizing: border-box; font-family: 'Segoe UI', sans-serif; }}
            body {{ background: var(--acik-mavi); margin: 0; overflow: hidden; height: 100vh; display: flex; flex-direction: column; }}

            /* REKLAM BANDI */
            .header-ads {{ background: var(--koyu-mavi); color: #fbbf24; padding: 8px; overflow: hidden; white-space: nowrap; border-bottom: 3px solid #fbbf24; }}
            .scroll {{ display: inline-block; animation: scroll 20s linear infinite; font-weight: bold; }}

            /* ANA ALAN */
            .main-content {{ flex: 1; display: flex; position: relative; }}

            /* HARİTA (TAM EKRAN) */
            #map {{ flex: 1; z-index: 1; }}

            /* SAĞ DURAK PANELİ (İNCE UZUN) */
            .right-panel {{
                width: 120px; background: rgba(255,255,255,0.9); backdrop-filter: blur(10px);
                z-index: 10; border-left: 2px solid var(--ana-mavi); padding: 10px;
                display: flex; flex-direction: column; align-items: center;
            }}
            .right-panel h4 {{ color: var(--koyu-mavi); font-size: 12px; margin: 5px 0; text-align: center; }}
            .right-panel ul {{ list-style: none; padding: 0; width: 100%; }}
            .right-panel li {{ 
                background: var(--ana-mavi); color: white; font-size: 10px; 
                padding: 8px 4px; margin-bottom: 8px; border-radius: 6px; 
                text-align: center; font-weight: bold; box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}

            /* SOL YÜZEN MENÜ BUTONLARI */
            .left-menu {{ position: absolute; left: 15px; top: 15px; z-index: 20; display: flex; flex-direction: column; gap: 10px; }}
            .menu-btn {{ 
                width: 50px; height: 50px; background: var(--koyu-mavi); color: white; 
                border-radius: 50%; display: flex; align-items: center; justify-content: center; 
                cursor: pointer; font-size: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); border: 2px solid white;
            }}

            /* AÇILIR PENCERE (MODAL) */
            .modal {{ 
                display: none; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
                width: 300px; background: white; border-radius: 20px; padding: 20px;
                z-index: 100; box-shadow: 0 0 30px rgba(0,0,0,0.5); border: 3px solid var(--ana-mavi);
            }}
            .modal-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; color: var(--koyu-mavi); }}
            .close-btn {{ cursor: pointer; font-size: 24px; font-weight: bold; }}

            .clock {{ font-weight: bold; color: var(--koyu-mavi); margin-top: auto; font-size: 14px; padding-bottom: 10px; }}

            @keyframes scroll {{ from {{ transform: translateX(100%); }} to {{ transform: translateX(-100%); }} }}
        </style>
    </head>
    <body>
        <div class="header-ads">
            <div class="scroll">📢 BELEDİYEM SMART: Adana Hatları saniyeler içinde cebinizde! | İyi yolculuklar dileriz...</div>
        </div>

        <div class="main-content">
            <!-- Sol Menü -->
            <div class="left-menu">
                <div class="menu-btn" onclick="toggleModal('settings-modal')">⚙️</div>
                <div class="menu-btn" onclick="toggleModal('game-modal')">🎮</div>
            </div>

            <!-- Harita -->
            <div id="map"></div>

            <!-- Sağ Panel -->
            <div class="right-panel">
                <h4>OTOBÜS</h4>
                <ul>{otobus_listesi_html}</ul>
                <div class="clock" id="clock">{simdi}</div>
            </div>
        </div>

        <!-- Ayarlar Penceresi -->
        <div id="settings-modal" class="modal">
            <div class="modal-header"><h3>⚙️ Ayarlar</h3> <span class="close-btn" onclick="toggleModal('settings-modal')">&times;</span></div>
            <label>Şehir Değiştir:</label>
            <select style="width:100%; padding:10px; margin-top:10px; border-radius:10px;" onchange="location.href='/?sehir=' + this.value">
                <option value="Adana" {"selected" if sehir=="Adana" else ""}>Adana</option>
                <option value="İstanbul" {"selected" if sehir=="İstanbul" else ""}>İstanbul</option>
                <option value="Ankara" {"selected" if sehir=="Ankara" else ""}>Ankara</option>
            </select>
        </div>

        <!-- Oyun Penceresi -->
        <div id="game-modal" class="modal">
            <div class="modal-header"><h3>🎮 Mola</h3> <span class="close-btn" onclick="toggleModal('game-modal')">&times;</span></div>
            <p style="color: #666; text-align:center;">XOX buraya daha şık gelecek!</p>
            <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:5px; width:150px; margin:auto;" id="xox-mini">
                <!-- XOX alanını buraya çok daha küçük ekleyebiliriz -->
            </div>
        </div>

        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <script>
            // Pencere Aç/Kapat
            function toggleModal(id) {{
                const m = document.getElementById(id);
                m.style.display = (m.style.display === 'block') ? 'none' : 'block';
            }}

            // Saat
            setInterval(() => {{ document.getElementById('clock').textContent = new Date().toLocaleTimeString('tr-TR', {{hour:'2-digit', minute:'2-digit'}}); }}, 1000);

            // Harita
            var map = L.map('map', {{zoomControl: false}}).setView([{lat}, {lon}], {zoom});
            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png').addTo(map);
            L.marker([{lat}, {lon}]).addTo(map).bindPopup("<b>{sehir} Terminal</b>");
        </script>
    </body>
    </html>
    """
