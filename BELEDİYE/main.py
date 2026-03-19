from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import datetime

app = FastAPI()

# Şehir bazlı durak ve koordinat verileri
sehir_detaylari = {
    "Adana": {
        "duraklar": ["🚌 154 Hattı - 2 dk", "🚌 172 Hattı - Yakın", "🚌 İtimat 1 - 15 dk"],
        "koordinat": [36.9914, 35.3308], # Yüreğir/Adana civarı
        "zoom": 13
    },
    "İstanbul": {
        "duraklar": ["🚇 Metrobüs - 1 dk", "🚢 Vapur - Kalkıyor", "🚌 500T - Durakta"],
        "koordinat": [41.0082, 28.9784],
        "zoom": 11
    },
    "Ankara": {
        "duraklar": ["🚇 Ankaray - 3 dk", "🚌 EGO 413 - 12 dk"],
        "koordinat": [39.9334, 32.8597],
        "zoom": 12
    }
}

@app.get("/", response_class=HTMLResponse)
async def read_root(sehir: str = "Adana"):
    simdi = datetime.datetime.now().strftime("%H:%M:%S")
    
    # Seçilen şehrin verilerini çekelim
    detay = sehir_detaylari.get(sehir, sehir_detaylari["Adana"])
    otobus_listesi_html = "".join([f"<li>{hat}</li>" for hat in detay["duraklar"]])
    merkez_lat = detay["koordinat"][0]
    merkez_lon = detay["koordinat"][1]
    zoom_seviyesi = detay["zoom"]

    return f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Belediyem Akıllı Terminal 🛸</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <style>
            * {{ box-sizing: border-box; }}
            body {{
                background: linear-gradient(135deg, #0f172a, #1e3a8a);
                color: white; font-family: 'Segoe UI', sans-serif;
                margin: 0; padding: 10px; min-height: 100vh;
            }}
            .tv-screen {{
                background: #000; border: 2px solid #334155; border-radius: 12px;
                padding: 8px; margin-bottom: 12px; box-shadow: 0 0 20px rgba(0,0,0,0.5);
            }}
            .reklam-bandi {{
                color: #fbbf24; font-weight: bold; white-space: nowrap;
                animation: kayanYazi 12s linear infinite; font-size: 0.9rem;
            }}
            .wrapper {{ display: flex; flex-direction: column; gap: 12px; }}
            .sidebar {{
                background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(8px);
                padding: 15px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.1);
            }}
            #map {{
                height: 300px; width: 100%; border-radius: 15px;
                border: 2px solid #334155; box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            }}
            .bus-list {{
                background: rgba(15, 23, 42, 0.8); padding: 15px;
                border-radius: 15px; border: 1px solid rgba(255,255,255,0.1);
            }}
            ul {{ list-style: none; padding: 0; margin: 0; }}
            li {{
                background: #f8fafc; color: #1e3a8a; margin-bottom: 10px;
                padding: 15px; border-radius: 12px; font-weight: 800;
                box-shadow: 0 2px 5px rgba(0,0,0,0.2); border-left: 5px solid #fbbf24;
            }}
            select, button {{
                width: 100%; padding: 14px; border-radius: 10px; border: none;
                margin-top: 10px; font-weight: bold; background: #fbbf24; color: #000;
            }}
            .time-display {{ text-align: center; font-size: 1.4rem; color: #fbbf24; margin-top: 15px; text-shadow: 0 0 10px rgba(251,191,36,0.5); }}
            @keyframes kayanYazi {{ from {{ transform: translateX(100%); }} to {{ transform: translateX(-100%); }} }}
        </style>
    </head>
    <body>
        <div class="tv-screen">
            <div class="reklam-bandi">🛸 AKILLI TERMİNAL CANLI YAYINDA | ŞEHİR: {sehir.upper()} | TRAFİK YOĞUNLUĞU: DÜŞÜK</div>
        </div>

        <div class="wrapper">
            <div class="sidebar">
                <h3 style="margin:0; color:#fbbf24;">📍 ŞEHİR SEÇİN</h3>
                <select onchange="location.href='/?sehir=' + this.value">
                    <option value="Adana" {"selected" if sehir=="Adana" else ""}>Adana (Yüreğir)</option>
                    <option value="İstanbul" {"selected" if sehir=="İstanbul" else ""}>İstanbul</option>
                    <option value="Ankara" {"selected" if sehir=="Ankara" else ""}>Ankara</option>
                </select>
                <div id="user-icon" style="font-size:50px; text-align:center; margin:10px;">🛸</div>
                <div class="time-display">🕒 <span id="clock">{simdi}</span></div>
            </div>

            <div id="map"></div>

            <div class="bus-list">
                <h3 style="margin:0 0 10px 0; color:#fbbf24;">🚍 DURAKTAKİ OTOBÜSLER</h3>
                <ul>{otobus_listesi_html}</ul>
            </div>
        </div>

        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <script>
            // Canlı Saat Fonksiyonu
            setInterval(() => {{
                document.getElementById('clock').textContent = new Date().toLocaleTimeString('tr-TR');
            }}, 1000);

            // Dinamik Harita Ayarları
            var map = L.map('map').setView([{merkez_lat}, {merkez_lon}], {zoom_seviyesi});
            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png').addTo(map);

            // Şehre göre ana marker
            L.marker([{merkez_lat}, {merkez_lon}]).addTo(map)
                .bindPopup("<b>{sehir} Ana Terminal</b>")
                .openPopup();
        </script>
    </body>
    </html>
    """
