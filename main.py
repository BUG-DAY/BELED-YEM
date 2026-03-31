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
        <title>T.C. Akıllı Ulaşım Ağları 🛸</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <style>
            :root {{ --tr-mavi: #1e3a8a; --tr-kirmizi: #e11d48; --gold: #c5a059; }}
            * {{ box-sizing: border-box; font-family: 'Segoe UI', sans-serif; }}
            
            body {{ 
                margin: 0; height: 100vh; display: flex; align-items: center; justify-content: center;
                background: #cbd5e1; background-image: url('https://www.transparenttextures.com/patterns/az-subtle.png');
            }}

            .app-frame {{
                width: 95vw; height: 95vw; max-width: 500px; max-height: 500px;
                background: white; border-radius: 40px; overflow: hidden;
                position: relative; display: flex; flex-direction: column;
                box-shadow: 0 30px 60px rgba(0,0,0,0.4); border: 8px solid #334155;
            }}

            /* TV REKLAM BANDI */
            .tv-strip {{ background: #000; padding: 12px; border-bottom: 3px solid var(--tr-mavi); z-index: 1000; }}
            .scroll {{ color: var(--tr-kirmizi); font-weight: 900; white-space: nowrap; animation: scroll 15s linear infinite; font-family: monospace; font-size: 13px; }}

            .content {{ flex: 1; position: relative; display: flex; overflow: hidden; }}
            #map {{ flex: 1; z-index: 1; }}

            /* SOL TEKNOLOJİK MENÜ */
            .left-dock {{
                position: absolute; left: 0; top: 0; bottom: 0; width: 45px;
                background: rgba(30, 58, 138, 0.9); backdrop-filter: blur(8px);
                z-index: 100; display: flex; flex-direction: column; align-items: center; gap: 25px; padding-top: 20px;
                transition: width 0.3s; overflow: hidden;
            }}
            .left-dock:hover {{ width: 130px; }}
            .icon {{ color: white; font-size: 22px; cursor: pointer; display: flex; align-items: center; gap: 12px; }}
            .label {{ display: none; font-size: 10px; font-weight: 900; color: white; }}
            .left-dock:hover .label {{ display: block; }}

            /* SAĞ VERİ ŞERİDİ */
            .right-data {{
                width: 85px; background: rgba(255,255,255,0.95); border-left: 2px solid var(--tr-mavi);
                z-index: 50; display: flex; flex-direction: column; align-items: center; padding: 12px 5px; gap: 10px;
            }}
            .city-tag {{ background: var(--tr-mavi); color: white; font-size: 9px; padding: 10px 2px; border-radius: 10px; width: 100%; text-align: center; font-weight: 900; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}

            /* ALT SAAT VE LOGO */
            .footer {{ background: white; padding: 10px; text-align: center; border-top: 1.5px solid #eee; display: flex; justify-content: space-around; }}
            .clock {{ font-size: 18px; font-weight: 900; color: var(--tr-mavi); }}

            @keyframes scroll {{ from {{ transform: translateX(100%); }} to {{ transform: translateX(-100%); }} }}
        </style>
    </head>
    <body>

        <div class="app-frame">
            <div class="tv-strip">
                <div class="scroll">🇹🇷 T.C. AKILLI ULAŞIM AĞLARI | TÜRKİYE GENELİ CANLI TAKİP SİSTEMİ | PROJE: MEHMET TAHİR</div>
            </div>

            <div class="content">
                <div class="left-dock">
                    <div class="icon" onclick="location.href='/?sehir=Adana'">📍 <span class="label">ADANA</span></div>
                    <div class="icon" onclick="location.href='/?sehir=İstanbul'">📍 <span class="label">İSTANBUL</span></div>
                    <div class="icon" onclick="location.href='/?sehir=Ankara'">📍 <span class="label">ANKARA</span></div>
                </div>

                <div id="map"></div>

                <div class="right-data">
                    <div style="font-size:9px; font-weight:900; color:var(--tr-mavi); margin-bottom:5px;">HATLAR</div>
                    <div class="city-tag" id="bus1">ANA HAT: 2dk</div>
                    <div class="city-tag" style="background:#c5a059" id="bus2">EKSPRES</div>
                    <div class="city-tag" style="background:var(--tr-kirmizi)" id="bus3">METRO</div>
                </div>
            </div>

            <div class="footer">
                <div style="font-size:10px; font-weight:bold; color:#888;">TÜRKİYE AKILLI TERMİNAL</div>
                <div class="clock" id="clock">{simdi}</div>
            </div>
        </div>

        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <script>
            // Saat
            setInterval(() => {{ 
                document.getElementById('clock').textContent = new Date().toLocaleTimeString('tr-TR', {{hour:'2-digit', minute:'2-digit'}}); 
            }}, 1000);

            // Şehir Koordinatları
            const coords = {{
                "Adana": [36.9914, 35.3308],
                "İstanbul": [41.0082, 28.9784],
                "Ankara": [39.9334, 32.8597]
            }};
            const currentSehir = "{sehir}";
            const center = coords[currentSehir] || coords["Adana"];

            // Harita
            var map = L.map('map', {{zoomControl: false}}).setView(center, 13);
            L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png').addTo(map);

            // Hareketli Otobüs (Şehre Göre)
            var busIcon = L.divIcon({{
                html: '<div style="background: #1e3a8a; border: 2px solid white; border-radius: 50%; width: 22px; height: 22px; display: flex; align-items:center; justify-content:center; color:white; font-size:11px;">🚌</div>',
                className: 'dummy-bus'
            }});
            var busMarker = L.marker(center, {{icon: busIcon}}).addTo(map);

            let angle = 0;
            setInterval(() => {{
                angle += 0.005;
                let newLat = center[0] + Math.sin(angle) * 0.005;
                let newLon = center[1] + Math.cos(angle) * 0.005;
                busMarker.setLatLng([newLat, newLon]);
                
                // Canlı Dakika Simülasyonu
                let min = Math.abs(Math.floor(Math.sin(angle)*5 + 3));
                document.getElementById('bus1').textContent = min === 0 ? "DURAKTA" : "HAT: " + min + "dk";
            }}, 100);
        </script>
    </body>
    </html>
    """
