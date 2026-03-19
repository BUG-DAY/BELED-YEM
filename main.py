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
        <title>Belediyem Kare 🛸</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <style>
            :root {{ --tr-mavi: #1e3a8a; --tr-kirmizi: #e11d48; --bg: #f8fafc; }}
            * {{ box-sizing: border-box; font-family: 'Inter', sans-serif; }}
            
            body {{ 
                background: #cbd5e1; /* Dış arka plan koyu */
                margin: 0; display: flex; align-items: center; justify-content: center; height: 100vh;
            }}

            /* ANA KARE ÇERÇEVE */
            .app-container {{
                width: 95vw; height: 95vw; max-width: 500px; max-height: 500px; /* Tam Kare Yapı */
                background: white; border-radius: 30px; overflow: hidden;
                display: flex; flex-direction: column; position: relative;
                box-shadow: 0 25px 50px rgba(0,0,0,0.3); border: 8px solid #334155;
            }}

            /* TV PANELİ (ÜSTTE KAREMSİ) */
            .tv-header {{
                background: #000; padding: 10px; border-bottom: 4px solid var(--tr-mavi);
            }}
            .scroll-text {{ color: var(--tr-kirmizi); font-weight: 900; white-space: nowrap; animation: scroll 10s linear infinite; font-size: 14px; font-family: monospace; }}

            /* ORTA ALAN: HARİTA VE PANELLER */
            .main-view {{ flex: 1; position: relative; display: flex; overflow: hidden; }}

            /* HARİTA (MERKEZDE) */
            #map {{ flex: 1; z-index: 1; }}

            /* SOL GİZLİ PANEL (UZUNLAMASINA) */
            .left-side-menu {{
                position: absolute; left: 0; top: 0; bottom: 0; width: 45px;
                background: rgba(30, 58, 138, 0.9); backdrop-filter: blur(5px);
                z-index: 100; display: flex; flex-direction: column; align-items: center; gap: 20px; padding-top: 15px;
                transition: width 0.3s; overflow: hidden;
            }}
            .left-side-menu:active, .left-side-menu:hover {{ width: 120px; }} /* Üstüne gelince veya basınca açılır */
            .menu-icon {{ color: white; font-size: 20px; cursor: pointer; display: flex; align-items: center; gap: 10px; }}
            .menu-text {{ display: none; font-size: 12px; font-weight: bold; }}
            .left-side-menu:hover .menu-text {{ display: block; }}

            /* SAĞ İNCE DURAK PANELİ */
            .right-track {{
                width: 70px; background: rgba(255,255,255,0.9); border-left: 2px solid var(--tr-mavi);
                z-index: 50; display: flex; flex-direction: column; align-items: center; padding: 10px 5px; gap: 10px;
            }}
            .bus-card {{ background: var(--tr-mavi); color: white; font-size: 9px; padding: 8px 2px; border-radius: 8px; width: 100%; text-align: center; font-weight: bold; }}

            /* ALT SAAT */
            .bottom-bar {{ background: white; padding: 5px; text-align: center; border-top: 2px solid #eee; }}
            .digital-clock {{ font-size: 18px; font-weight: 900; color: var(--tr-mavi); }}

            @keyframes scroll {{ from {{ transform: translateX(100%); }} to {{ transform: translateX(-100%); }} }}
        </style>
    </head>
    <body>

        <div class="app-container">
            <!-- Üst TV Paneli -->
            <div class="tv-header">
                <div class="scroll-text">📺 TERMİNAL CANLI AKIŞ: MEHMET TAHİR SİSTEMİ %100 AKTİF...</div>
            </div>

            <div class="main-view">
                <!-- Sol Gizli Menü (Gerektiğinde Uzunlamasına Açılır) -->
                <div class="left-side-menu">
                    <div class="menu-icon">⚙️ <span class="menu-text">AYARLAR</span></div>
                    <div class="menu-icon">🎮 <span class="menu-text">OYUNLAR</span></div>
                    <div class="menu-icon">🗺️ <span class="menu-text">ROTALAR</span></div>
                </div>

                <!-- Harita -->
                <div id="map"></div>

                <!-- Sağ İnce Takip -->
                <div class="right-track">
                    <div style="font-size:10px; font-weight:bold; color:var(--tr-mavi);">CANLI</div>
                    <div class="bus-card">154: 2dk</div>
                    <div class="bus-card" style="background:#c5a059">İTİMAT</div>
                </div>
            </div>

            <!-- Alt Saat -->
            <div class="bottom-bar">
                <div class="digital-clock" id="clock">{simdi}</div>
            </div>
        </div>

        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <script>
            setInterval(() => {{ 
                document.getElementById('clock').textContent = new Date().toLocaleTimeString('tr-TR', {{hour:'2-digit', minute:'2-digit'}}); 
            }}, 1000);

            var map = L.map('map', {{zoomControl: false}}).setView([36.9914, 35.3308], 14);
            L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png').addTo(map);
            L.marker([36.9914, 35.3308]).addTo(map);
        </script>
    </body>
    </html>
    """
