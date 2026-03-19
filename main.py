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
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Belediyem - Akıllı Terminal 🛸</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <style>
            * {{ box-sizing: border-box; }}
            body {{
                background: linear-gradient(135deg, #1e3a8a, #3b82f6);
                color: white; font-family: 'Segoe UI', Tahoma, sans-serif;
                margin: 0; display: flex; flex-direction: column; height: 100vh; width: 100vw; overflow: hidden;
            }}
            .tv-frame {{ padding: 10px 15px; width: 100%; z-index: 10; }}
            .tv-screen {{
                height: 60px; background: #000; border: 3px solid #334155;
                border-radius: 12px; display: flex; align-items: center;
                overflow: hidden; box-shadow: 0 5px 15px rgba(0,0,0,0.5);
            }}
            .reklam-bandi {{
                font-size: 1.2rem; font-weight: bold; color: #facc15;
                animation: kayanYazi 20s linear infinite; white-space: nowrap;
            }}
            .wrapper {{ display: flex; flex: 1; min-height: 0; }}
            .sidebar {{
                width: 260px; min-width: 260px; background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px); padding: 20px;
                display: flex; flex-direction: column; gap: 15px;
                border-right: 1px solid rgba(255, 255, 255, 0.2);
            }}
            .main-content {{ flex: 1; display: flex; flex-direction: column; min-width: 0; padding: 15px; }}
            .content-row {{ flex: 1; display: flex; gap: 15px; min-height: 0; }}
            #map {{
                flex: 3; background: rgba(255,255,255,0.08); border-radius: 20px;
                border: 2px solid rgba(255,255,255,0.15); 
            }}
            .bus-list {{
                width: 260px; min-width: 260px;
                background: rgba(255, 255, 255, 0.1); border-radius: 20px;
                padding: 15px; border: 1px solid rgba(255,255,255,0.2);
                overflow-y: auto;
            }}
            ul {{ list-style: none; padding: 0; }}
            li {{ 
                background: white; color: #1e3a8a; margin-bottom: 10px; 
                padding: 12px; border-radius: 12px; font-weight: bold;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1); font-size: 0.85rem;
            }}
            select, button {{
                width: 100%; padding: 10px; border-radius: 10px; border: none; 
                background: white; color: #1e3a8a; font-weight: bold; cursor: pointer;
            }}
            .icon-display {{ font-size: 50px; text-align: center; margin: 5px 0; animation: bounce 2s infinite; }}
            @keyframes bounce {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-10px); }} }}
            @keyframes kayanYazi {{ from {{ transform: translateX(100%); }} to {{ transform: translateX(-100%); }} }}
        </style>
    </head>
    <body>
        <div class="tv-frame">
            <div class="tv-screen">
                <div class="reklam-bandi">📢 BELEDİYEM DUYURU: Akıllı Terminal Sistemi Yayında! | 🚍 Mehmet Tahir Sundu! | ☀️ Hava: {sehir} Açık | 🛸 Yarın UFO Seferleri Başlıyor!</div>
            </div>
        </div>

        <div class="wrapper">
            <div class="sidebar">
                <h2 style="color: #facc15; margin:0; font-size: 1.2rem;">⚙️ KONTROL</h2>
                <select onchange="location.href='/?sehir=' + this.value">
                    <option value="Adana" {"selected" if sehir=="Adana" else ""}>Adana</option>
                    <option value="İstanbul" {"selected" if sehir=="İstanbul" else ""}>İstanbul</option>
                    <option value="Ankara" {"selected" if sehir=="Ankara" else ""}>Ankara</option>
                </select>
                <button onclick="alert('GPS Aranıyor...')">📍 Konum Bul</button>
                <div id="user-icon" class="icon-display">🛸</div>
                <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 5px;">
                    <button onclick="document.getElementById('user-icon').textContent='🐰'">🐰</button>
                    <button onclick="document.getElementById('user-icon').textContent='🏎️'">🏎️</button>
                </div>
                <div style="text-align: center; font-weight: bold; color: #facc15; margin-top: auto; font-size: 1.1rem;">
                    🕒 <span id="clock">{simdi}</span>
                </div>
            </div>

            <div class="main-content">
                <div class="content-row">
                    <div id="map"></div>
                    <div class="bus-list">
                        <h3 style="color: #facc15; border-bottom: 2px solid #facc15; padding-bottom: 5px; margin-top:0; font-size: 1rem;">⏳ Canlı Durak</h3>
                        <ul>{otobus_listesi_html}</ul>
                    </div>
                </div>
            </div>
        </div>

        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <script>
            setInterval(() => {{
                document.getElementById('clock').textContent = new Date().toLocaleTimeString('tr-TR');
            }}, 1000);

            var map = L.map('map').setView([39.9334, 32.8597], 12);
            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png').addTo(map);
            L.marker([39.9334, 32.8597]).addTo(map).bindPopup("<b>Ana Terminal</b>").openPopup();
        </script>
    </body>
    </html>
    """
