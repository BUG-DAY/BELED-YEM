from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import datetime

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root(sehir: str = "Adana"):
    simdi = datetime.datetime.now().strftime("%H:%M")
    
    return f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Belediyem Radar 🛸</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <style>
            :root {{ --neon-blue: #00d2ff; --glass: rgba(255, 255, 255, 0.9); }}
            * {{ box-sizing: border-box; font-family: 'Orbitron', sans-serif; }}
            body {{ 
                background: #e0e5ec; margin: 0; padding: 15px; 
                display: flex; flex-direction: column; height: 100vh; gap: 20px;
                align-items: center; justify-content: center;
            }}

            /* TELEVİZYON REKLAM PANOSU */
            .tv-frame {{ 
                width: 100%; max-width: 400px; background: #333; padding: 5px; 
                border-radius: 10px; border: 4px solid #111; box-shadow: 0 10px 20px rgba(0,0,0,0.3);
            }}
            .tv-screen {{ 
                background: #000; height: 30px; overflow: hidden; position: relative; 
                display: flex; align-items: center;
            }}
            .scroll {{ color: #00ff00; white-space: nowrap; animation: scroll 12s linear infinite; font-family: monospace; font-size: 14px; }}

            /* YUVARLAK RADAR HARİTA (TAM ORTADA) */
            .map-container {{
                position: relative; width: 300px; height: 300px;
                border-radius: 50%; border: 8px solid white;
                box-shadow: 20px 20px 60px #bebebe, -20px -20px 60px #ffffff;
                overflow: hidden; z-index: 10;
            }}
            #map {{ width: 100%; height: 100%; }}

            /* SOL AYARLAR VE OYUN (YÜZEN) */
            .left-actions {{ position: absolute; left: 20px; top: 50%; transform: translateY(-50%); display: flex; flex-direction: column; gap: 20px; }}
            .action-btn {{ 
                width: 50px; height: 50px; background: #e0e5ec; border-radius: 12px;
                display: flex; align-items: center; justify-content: center; font-size: 22px;
                box-shadow: 6px 6px 12px #bebebe, -6px -6px 12px #ffffff; cursor: pointer;
            }}

            /* SAĞ CANLI DURAK VERİSİ */
            .live-data {{
                position: absolute; right: 15px; top: 50%; transform: translateY(-50%);
                width: 100px; display: flex; flex-direction: column; gap: 10px;
            }}
            .bus-card {{
                background: #e0e5ec; padding: 10px; border-radius: 12px; text-align: center;
                box-shadow: 4px 4px 8px #bebebe, -4px -4px 8px #ffffff;
            }}
            .bus-id {{ font-size: 10px; font-weight: bold; color: #555; }}
            .bus-dist {{ font-size: 12px; color: var(--neon-blue); font-weight: 900; }}

            /* ALT SAAT */
            .bottom-info {{ margin-top: 10px; font-weight: 900; font-size: 20px; color: #333; }}

            @keyframes scroll {{ from {{ transform: translateX(100%); }} to {{ transform: translateX(-100%); }} }}
        </style>
    </head>
    <body>
        <!-- TV Reklam Panosu -->
        <div class="tv-frame">
            <div class="tv-screen">
                <div class="scroll">>>> BELEDİYE TV: {sehir.upper()} HATLARINDA CANLI TAKİP BAŞLADI... MEHMET TAHİR SUNAR...</div>
            </div>
        </div>

        <!-- Sol Tuşlar -->
        <div class="left-actions">
            <div class="action-btn" onclick="alert('Ayarlar Açıldı')">⚙️</div>
            <div class="action-btn" onclick="alert('Oyun Başladı')">🎮</div>
        </div>

        <!-- Yuvarlak Harita (Radar) -->
        <div class="map-container">
            <div id="map"></div>
        </div>

        <!-- Sağ Canlı Durak Değişen Veriler -->
        <div class="live-data">
            <div class="bus-card">
                <div class="bus-id">HAT 154</div>
                <div class="bus-dist" id="bus1">3 Durak</div>
            </div>
            <div class="bus-card">
                <div class="bus-id">İTİMAT 1</div>
                <div class="bus-dist" id="bus2">1 Durak</div>
            </div>
            <div class="bus-card">
                <div class="bus-id">HAT 172</div>
                <div class="bus-dist" id="bus3">Yakın</div>
            </div>
        </div>

        <div class="bottom-info" id="clock">{simdi}</div>

        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <script>
            // Saat Güncelleme
            setInterval(() => {{ document.getElementById('clock').textContent = new Date().toLocaleTimeString('tr-TR', {{hour:'2-digit', minute:'2-digit'}}); }}, 1000);

            // Durak Değiştirme Simülasyonu (Canlı Değişen Veri)
            let duraklar = ["5 Durak", "4 Durak", "3 Durak", "2 Durak", "1 Durak", "DURAKTA"];
            let i = 0;
            setInterval(() => {{
                i = (i + 1) % duraklar.length;
                document.getElementById('bus1').textContent = duraklar[i];
                document.getElementById('bus2').textContent = duraklar[(i+2)%duraklar.length];
            }}, 5000); // Her 5 saniyede bir durak değişir

            // Harita Kurulum (Adana Odaklı)
            var map = L.map('map', {{zoomControl: false}}).setView([36.9914, 35.3308], 14);
            L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png').addTo(map);
            L.circle([36.9914, 35.3308], {{color: 'red', fillColor: '#f03', fillOpacity: 0.5, radius: 200}}).addTo(map);
        </script>
    </body>
    </html>
    """
