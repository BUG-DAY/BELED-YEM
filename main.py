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
        <title>Belediyem Pro Terminal 🛸</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <style>
            :root {{ --tr-mavi: #1e3a8a; --tr-altin: #c5a059; --tr-kirmizi: #e11d48; }}
            * {{ box-sizing: border-box; font-family: 'Inter', sans-serif; }}
            
            body {{ 
                margin: 0; height: 100vh; display: flex; align-items: center; justify-content: center;
                background: #cbd5e1; background-image: url('https://www.transparenttextures.com/patterns/az-subtle.png');
            }}

            .terminal-square {{
                width: 95vw; height: 95vw; max-width: 500px; max-height: 500px;
                background: white; border-radius: 40px; overflow: hidden;
                position: relative; display: flex; flex-direction: column;
                box-shadow: 0 30px 60px rgba(0,0,0,0.3); border: 6px solid #334155;
            }}

            .tv-strip {{ background: #000; padding: 10px; border-bottom: 3px solid var(--tr-mavi); z-index: 1000; }}
            .scroll {{ color: var(--tr-kirmizi); font-weight: 900; white-space: nowrap; animation: scroll 12s linear infinite; font-family: monospace; font-size: 13px; }}

            .content {{ flex: 1; position: relative; display: flex; overflow: hidden; }}
            #map {{ flex: 1; z-index: 1; }}

            /* SOL PANEL - SADECE AYARLAR */
            .left-dock {{
                position: absolute; left: 0; top: 0; bottom: 0; width: 45px;
                background: rgba(30, 58, 138, 0.9); backdrop-filter: blur(8px);
                z-index: 100; display: flex; flex-direction: column; align-items: center; gap: 25px; padding-top: 20px;
                transition: width 0.3s; overflow: hidden;
            }}
            .left-dock:hover {{ width: 120px; }}
            .icon {{ color: white; font-size: 22px; cursor: pointer; display: flex; align-items: center; gap: 10px; }}
            .label {{ display: none; font-size: 10px; font-weight: bold; white-space: nowrap; }}
            .left-dock:hover .label {{ display: block; }}

            /* SAĞ PANEL - CANLI DURAK TAKİBİ */
            .right-track {{
                width: 80px; background: rgba(255,255,255,0.95); border-left: 2px solid var(--tr-mavi);
                z-index: 50; display: flex; flex-direction: column; align-items: center; padding: 12px 5px; gap: 10px;
            }}
            .search-mini {{ width: 100%; padding: 5px; border-radius: 5px; border: 1px solid #ccc; font-size: 9px; }}
            .bus-tag {{ background: var(--tr-mavi); color: white; font-size: 9px; padding: 10px 2px; border-radius: 8px; width: 100%; text-align: center; font-weight: bold; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}

            .footer-bar {{ background: white; padding: 8px; text-align: center; border-top: 1.5px solid #eee; }}
            .clock {{ font-size: 18px; font-weight: 900; color: var(--tr-mavi); letter-spacing: 1px; }}

            @keyframes scroll {{ from {{ transform: translateX(100%); }} to {{ transform: translateX(-100%); }} }}
        </style>
    </head>
    <body>
        <div class="terminal-square">
            <div class="tv-strip">
                <div class="scroll">📡 BELEDİYEM SMART: SİSTEM AKTİF | 154 HATTI YAKLAŞIYOR | MEHMET TAHİR SUNAR...</div>
            </div>

            <div class="content">
                <div class="left-dock">
                    <div class="icon" onclick="alert('Ayarlar yakında eklenecek!')">⚙️ <span class="label">AYARLAR</span></div>
                    <div class="icon" onclick="alert('Rota bilgisi yükleniyor...')">🛰️ <span class="label">RADAR</span></div>
                </div>

                <div id="map"></div>

                <div class="right-track">
                    <input type="text" class="search-mini" placeholder="Hat Ara">
                    <div style="font-size:9px; font-weight:900; color:var(--tr-altin);">CANLI</div>
                    <div class="bus-tag" id="bus1">154: 3dk</div>
                    <div class="bus-tag" style="background:#c5a059" id="bus2">İTİMAT</div>
                    <div class="bus-tag" style="background:var(--tr-kirmizi)" id="bus3">172: YAKIN</div>
                </div>
            </div>

            <div class="footer-bar">
                <div class="clock" id="clock">{simdi}</div>
            </div>
        </div>

        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <script>
            // Saat Güncelleme
            setInterval(() => {{ 
                document.getElementById('clock').textContent = new Date().toLocaleTimeString('tr-TR', {{hour:'2-digit', minute:'2-digit'}}); 
            }}, 1000);

            // Durak Simülasyonu
            let counts = [4, 3, 2, 1, 0];
            let step = 0;
            setInterval(() => {{
                step = (step + 1) % counts.length;
                let val = counts[step];
                document.getElementById('bus1').textContent = val === 0 ? "154: DURAKTA" : "154: " + val + "dk";
            }}, 5000);

            // Harita Kurulum (Adana)
            var map = L.map('map', {{zoomControl: false}}).setView([36.9914, 35.3308], 14);
            L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png').addTo(map);

            // Hareketli Otobüs
            var busIcon = L.divIcon({{
                html: '<div style="background: #1e3a8a; border: 2px solid white; border-radius: 50%; width: 22px; height: 22px; display: flex; align-items:center; justify-content:center; color:white; font-size:11px;">🚌</div>',
                className: 'dummy-bus'
            }});
            var busMarker = L.marker([36.9914, 35.3308], {{icon: busIcon}}).addTo(map);

            let angle = 0;
            setInterval(() => {{
                angle += 0.005;
                let newLat = 36.9914 + Math.sin(angle) * 0.004;
                let newLon = 35.3308 + Math.cos(angle) * 0.004;
                busMarker.setLatLng([newLat, newLon]);
            }}, 100);
        </script>
    </body>
    </html>
    """
