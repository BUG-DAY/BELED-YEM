from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import datetime

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root(sehir: str = "Adana"):
    simdi = datetime.datetime.now().strftime("%H:%M")
    
    # Şehir bazlı koordinat ve zum ayarları (Türkiye Vizyonu)
    coords = {
        "Adana": {"center": [36.9914, 35.3308], "zoom": 14},
        "İstanbul": {"center": [41.0082, 28.9784], "zoom": 13},
        "Ankara": {"center": [39.9334, 32.8597], "zoom": 13}
    }
    currentCoord = coords.get(sehir, coords["Adana"])
    
    return f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>T.C. Akıllı Ulaşım Komuta Merkezi 🛸</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <style>
            :root {{
                --neon-blue: #00d2ff; --neon-gold: #fbbf24; --deep-bg: #0f172a; --panel-bg: rgba(30,41,59,0.9);
                --tr-kirmizi: #e11d48;
            }}
            * {{ box-sizing: border-box; font-family: 'Inter', sans-serif; }}
            
            body {{ 
                margin: 0; padding: 15px; display: flex; align-items: center; justify-content: center; height: 100vh;
                background: #1e293b; background-image: url('https://www.transparenttextures.com/patterns/carbon-fibre.png');
            }}

            /* YENİ UZUNLAMASINA (DİKEY) ÇERÇEVE */
            .command-center-frame {{
                width: 90vw; height: 85vh; max-width: 500px; max-height: 800px; /* Boyu uzattık! */
                background: var(--deep-bg); border-radius: 35px; overflow: hidden;
                display: flex; flex-direction: column; position: relative;
                box-shadow: 0 40px 100px rgba(0,0,0,0.5); border: 3px solid #334155;
            }}

            /* TV PANELİ (YEŞİL AKAN YAZILAR) */
            .tv-strip {{ background: #000; padding: 10px; border-bottom: 3px solid var(--neon-gold); z-index: 1000; }}
            .scroll {{ color: #00ff41; font-weight: 900; white-space: nowrap; animation: scroll 12s linear infinite; font-family: monospace; font-size: 13px; }}

            .content-area {{ flex: 1; position: relative; display: flex; overflow: hidden; }}
            #map {{ flex: 1; z-index: 1; }}

            /* SOL TEKNOLOJİK PANEL */
            .left-dock {{
                position: absolute; left: 0; top: 0; bottom: 0; width: 45px;
                background: rgba(15, 23, 42, 0.95); backdrop-filter: blur(10px);
                z-index: 100; display: flex; flex-direction: column; align-items: center; gap: 20px; padding-top: 20px;
                transition: width 0.3s; overflow: hidden; border-right: 2px solid var(--neon-blue);
            }}
            .left-dock:hover {{ width: 140px; }}
            .icon {{ color: white; font-size: 22px; cursor: pointer; display: flex; align-items: center; gap: 12px; }}
            .label {{ display: none; font-size: 11px; font-weight: 900; color: white; }}
            .left-dock:hover .label {{ display: block; }}

            /* SAĞ VERİ ŞERİDİ */
            .right-data {{
                width: 90px; background: rgba(30, 41, 59, 0.9); border-left: 2px solid var(--neon-blue);
                z-index: 50; display: flex; flex-direction: column; align-items: center; padding: 12px 5px; gap: 10px;
            }}
            .bus-tag {{ background: white; color: var(--tr-mavi); font-size: 9px; padding: 10px 2px; border-radius: 10px; width: 100%; text-align: center; font-weight: 900; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}

            /* ALT BİLGİ VE SAAT */
            .footer {{ background: #fff; padding: 10px; text-align: center; border-top: 2px solid #ddd; display: flex; justify-content: space-around; }}
            .digital-clock {{ font-size: 20px; font-weight: 900; color: var(--tr-mavi); }}

            @keyframes scroll {{ from {{ transform: translateX(100%); }} to {{ transform: translateX(-100%); }} }}
        </style>
    </head>
    <body>

        <div class="command-center-frame">
            <div class="tv-strip">
                <div class="scroll">🇹🇷 T.C. AKILLI ULAŞIM KOMUTA MERKEZİ | SİSTEM AKTİF | ŞEHİR: {sehir.upper()} | PROJE: MEHMET TAHİR</div>
            </div>

            <div class="content-area">
                <div class="left-dock">
                    <div class="icon" onclick="location.href='/?sehir=Adana'">📍 <span class="label">ADANA</span></div>
                    <div class="icon" onclick="location.href='/?sehir=İstanbul'">📍 <span class="label">İSTANBUL</span></div>
                    <div class="icon" onclick="location.href='/?sehir=Ankara'">📍 <span class="label">ANKARA</span></div>
                </div>

                <div id="map"></div>

                <div class="right-data">
                    <div style="font-size:9px; font-weight:900; color:var(--neon-blue); margin-bottom:5px;">HATLAR</div>
                    <div class="bus-tag" style="background:var(--neon-blue); color:white;">HAT: 2dk</div>
                    <div class="bus-tag" style="background:var(--neon-gold); color:black;">İTİMAT</div>
                    <div class="bus-tag" style="background:var(--tr-kirmizi); color:white;">METRO</div>
                </div>
            </div>

            <div class="footer">
                <div style="font-size:10px; font-weight:bold; color:#888;">TÜRKİYE AKILLI ULAŞIM</div>
                <div class="digital-clock" id="clock">{simdi}</div>
            </div>
        </div>

        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <script>
            // Saat
            setInterval(() => {{ 
                document.getElementById('clock').textContent = new Date().toLocaleTimeString('tr-TR', {{hour:'2-digit', minute:'2-digit'}}); 
            }}, 1000);

            // Dinamik Harita ve Şehir Odaklama
            var center = {currentCoord['center']};
            var zoom = {currentCoord['zoom']};
            var map = L.map('map', {{zoomControl: false}}).setView(center, zoom);
            
            // Profesyonel Açık Renk Harita Teması
            L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png').addTo(map);

            // Hareketli Otobüs
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
            }}, 100);
        </script>
    </body>
    </html>
    """
