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
        <title>Belediyem Anadolu 🇹🇷</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <style>
            :root {{ --tr-mavi: #1e3a8a; --tr-altin: #c5a059; --tr-kirmizi: #e11d48; }}
            * {{ box-sizing: border-box; font-family: 'Inter', sans-serif; }}
            
            /* KÖŞELERİ DOLDURAN ARKA PLAN */
            body {{ 
                margin: 0; height: 100vh; display: flex; align-items: center; justify-content: center;
                background: #f1f5f9;
                /* Selçuklu Yıldızı ve Mimari Doku Simülasyonu */
                background-image: 
                    radial-gradient(circle at 10% 10%, rgba(30, 58, 138, 0.05) 0%, transparent 20%),
                    radial-gradient(circle at 90% 90%, rgba(197, 160, 89, 0.1) 0%, transparent 20%),
                    url('https://www.transparenttextures.com/patterns/az-subtle.png'); /* Hafif geometrik doku */
                background-attachment: fixed;
            }}

            /* ALT TARAF SİLÜET (ADANA / TÜRKİYE ESİNTİSİ) */
            body::after {{
                content: ""; position: absolute; bottom: 0; left: 0; right: 0; height: 150px;
                background: url('https://www.transparenttextures.com/patterns/carbon-fibre.png');
                mask-image: linear-gradient(to top, rgba(0,0,0,0.1) 0%, transparent 100%);
                -webkit-mask-image: linear-gradient(to top, rgba(0,0,0,0.1) 0%, transparent 100%);
                z-index: -1;
            }}

            /* ANA KARE TERMİNAL */
            .terminal-square {{
                width: 92vw; height: 92vw; max-width: 480px; max-height: 480px;
                background: white; border-radius: 40px; overflow: hidden;
                position: relative; display: flex; flex-direction: column;
                box-shadow: 0 30px 60px rgba(0,0,0,0.2), 0 0 0 10px rgba(255,255,255,0.8);
                border: 4px solid var(--tr-mavi);
                z-index: 10;
            }}

            /* TV PANELİ */
            .tv-strip {{ background: #000; padding: 12px; border-bottom: 3px solid var(--tr-altin); }}
            .scroll {{ color: var(--tr-kirmizi); font-weight: 900; white-space: nowrap; animation: scroll 12s linear infinite; font-family: monospace; font-size: 14px; }}

            .content {{ flex: 1; position: relative; display: flex; }}

            /* HARİTA */
            #map {{ flex: 1; z-index: 1; }}

            /* SOL TEKNOLOJİK PANEL */
            .left-dock {{
                position: absolute; left: 0; top: 0; bottom: 0; width: 45px;
                background: rgba(30, 58, 138, 0.85); backdrop-filter: blur(10px);
                z-index: 100; display: flex; flex-direction: column; align-items: center; gap: 20px; padding-top: 20px;
                transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1); overflow: hidden;
                border-right: 1px solid rgba(255,255,255,0.2);
            }}
            .left-dock:hover {{ width: 130px; }}
            .icon {{ color: white; font-size: 22px; cursor: pointer; display: flex; align-items: center; gap: 12px; transition: 0.2s; }}
            .label {{ display: none; font-size: 11px; font-weight: 800; letter-spacing: 1px; }}
            .left-dock:hover .label {{ display: block; }}

            /* SAĞ TAKİP ŞERİDİ */
            .right-track {{
                width: 75px; background: rgba(255,255,255,0.95);
                z-index: 50; display: flex; flex-direction: column; align-items: center; padding: 10px 5px; gap: 12px;
                border-left: 1.5px solid #eee;
            }}
            .bus-tag {{ background: var(--tr-mavi); color: white; font-size: 9px; padding: 10px 2px; border-radius: 10px; width: 100%; text-align: center; font-weight: bold; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}

            /* ALT BİLGİ */
            .footer-bar {{ background: white; padding: 10px; text-align: center; border-top: 1.5px solid #eee; }}
            .clock {{ font-size: 20px; font-weight: 900; color: var(--tr-mavi); letter-spacing: 1px; }}

            @keyframes scroll {{ from {{ transform: translateX(100%); }} to {{ transform: translateX(-100%); }} }}
        </style>
    </head>
    <body>

        <div class="terminal-square">
            <div class="tv-strip">
                <div class="scroll">📡 ADANA YÜREĞİR TERMİNALİ | SİSTEM: ÇEVRİMİÇİ | MEHMET TAHİR KOMUTASI ALTINDA...</div>
            </div>

            <div class="content">
                <div class="left-dock">
                    <div class="icon">⚙️ <span class="label">AYARLAR</span></div>
                    <div class="icon">🎮 <span class="label">OYUNLAR</span></div>
                    <div class="icon">🛰️ <span class="label">RADAR</span></div>
                </div>

                <div id="map"></div>

                <div class="right-track">
                    <div style="font-size:9px; font-weight:900; color:var(--tr-altin); margin-bottom:5px;">CANLI</div>
                    <div class="bus-tag">154: 2dk</div>
                    <div class="bus-tag" style="background:#c5a059">İTİMAT</div>
                    <div class="bus-tag" style="background:#e11d48">172: DURAK</div>
                </div>
            </div>

            <div class="footer-bar">
                <div class="clock" id="clock">{simdi}</div>
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
