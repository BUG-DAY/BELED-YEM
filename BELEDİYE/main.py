from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import datetime

app = FastAPI()

sehirler_verisi = {
    "Adana": ["🚌 154 Hattı - 2 dk", "🚌 172 Hattı - Yakın", "🚌 İtimat 1 - 15 dk"],
    "İstanbul": ["🚇 Metrobüs - 1 dk", "🚢 Vapur - Kalkıyor", "🚌 500T - Durakta"],
    "Ankara": ["🚇 Ankaray - 3 dk", "🚌 EGO 413 - 12 dk"]
}

@app.get("/", response_class=HTMLResponse)
async def read_root(sehir: str = "Adana"):
    simdi = datetime.datetime.now().strftime("%H:%M:%S")
    otobusler = sehirler_verisi.get(sehir, ["Veri yok"])
    otobus_listesi_html = "".join([f"<li>{hat}</li>" for hat in otobusler])

    return f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Belediyem Mobil 🛸</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <style>
            * {{ box-sizing: border-box; }}
            body {{
                background: linear-gradient(135deg, #1e3a8a, #3b82f6);
                color: white; font-family: -apple-system, sans-serif;
                margin: 0; padding: 10px; min-height: 100vh;
            }}
            
            /* ÜST DUYURU PANOSU */
            .tv-screen {{
                background: #000; border: 2px solid #444; border-radius: 10px;
                padding: 10px; margin-bottom: 15px; overflow: hidden;
            }}
            .reklam-bandi {{
                color: #facc15; font-weight: bold; white-space: nowrap;
                animation: kayanYazi 15s linear infinite;
            }}

            /* ANA KAPSAYICI - MOBİLDE ALT ALTA */
            .wrapper {{ display: flex; flex-direction: column; gap: 15px; }}

            /* KONTROL PANELİ */
            .sidebar {{
                background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px);
                padding: 15px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.2);
            }}
            
            /* HARİTA KUTUSU - MOBİLDE DAHA YÜKSEK */
            #map {{
                height: 250px; width: 100%; border-radius: 15px;
                border: 2px solid rgba(255,255,255,0.3);
            }}

            /* OTOBÜS LİSTESİ */
            .bus-list {{
                background: rgba(255, 255, 255, 0.1); padding: 15px;
                border-radius: 15px; border: 1px solid rgba(255,255,255,0.2);
            }}

            ul {{ list-style: none; padding: 0; margin: 0; }}
            li {{
                background: white; color: #1e3a8a; margin-bottom: 8px;
                padding: 15px; border-radius: 10px; font-weight: bold;
                display: flex; align-items: center; justify-content: center;
            }}

            select, button {{
                width: 100%; padding: 12px; border-radius: 10px; border: none;
                margin-top: 10px; font-weight: bold; font-size: 1rem;
            }}
            
            .icon-display {{ font-size: 40px; text-align: center; margin: 10px 0; }}
            .time-display {{ text-align: center; font-size: 1.2rem; color: #facc15; margin-top: 10px; }}

            @keyframes kayanYazi {{ from {{ transform: translateX(100%); }} to {{ transform: translateX(-100%); }} }}
        </style>
    </head>
    <body>
        <div class="tv-screen">
            <div class="reklam-bandi">📢 BELEDİYEM MOBİL: Hoş Geldiniz! | Şehir: {sehir} | Yarın Tüm Hatlar Ücretsiz!</div>
        </div>

        <div class="wrapper">
            <div class="sidebar">
                <h3 style="margin:0; color:#facc15;">⚙️ KONTROL</h3>
                <select onchange="location.href='/?sehir=' + this.value">
                    <option value="Adana" {"selected" if sehir=="Adana" else ""}>Adana</option>
                    <option value="İstanbul" {"selected" if sehir=="İstanbul" else ""}>İstanbul</option>
                    <option value="Ankara" {"selected" if sehir=="Ankara" else ""}>Ankara</option>
                </select>
                <div id="user-icon" class="icon-display">🛸</div>
                <div style="display:flex; gap:10px;">
                    <button onclick="document.getElementById('user-icon').textContent='🐰'">🐰</button>
                    <button onclick="document.getElementById('user-icon').textContent='🏎️'">🏎️</button>
                </div>
                <div class="time-display">🕒 <span id="clock">{simdi}</span></div>
            </div>

            <div id="map"></div>

            <div class="bus-list">
                <h3 style="margin:0 0 10px 0; color:#facc15; border-bottom:1px solid #facc15;">⏳ CANLI DURAK</h3>
                <ul>{otobus_listesi_html}</ul>
            </div>
        </div>

        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <script>
            setInterval(() => {{
                document.getElementById('clock').textContent = new Date().toLocaleTimeString('tr-TR');
            }}, 1000);

            var map = L.map('map').setView([39.9334, 32.8597], 12);
            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png').addTo(map);
            L.marker([39.9334, 32.8597]).addTo(map).bindPopup("<b>Ana Terminal</b>");
        </script>
    </body>
    </html>
    """
