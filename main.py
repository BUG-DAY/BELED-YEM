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
        <title>Belediyem Türkiye 🇹🇷</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <style>
            :root {{ --tr-mavi: #1e3a8a; --tr-altin: #c5a059; --bg-soft: #f1f5f9; }}
            * {{ box-sizing: border-box; font-family: 'Inter', sans-serif; }}
            
            /* ARKA PLAN: TARİHİ DOKU */
            body {{ 
                background: var(--bg-soft);
                background-image: url('https://www.transparenttextures.com/patterns/shattered-island.png'); /* Hafif taş dokusu */
                margin: 0; padding: 15px; display: flex; flex-direction: column; height: 100vh; gap: 10px;
            }}

            /* 3. DİJİTAL EKRAN (DAHA KARE VE ŞIK) */
            .tv-frame {{
                width: 90%; max-width: 500px; margin: 0 auto;
                background: #111; border: 3px solid var(--tr-altin);
                border-radius: 8px; padding: 10px; box-shadow: 0 10px 30px rgba(0,0,0,0.4);
            }}
            .tv-display {{ background: #050505; height: 40px; overflow: hidden; display: flex; align-items: center; border: 1px solid #333; }}
            .scroll-text {{ color: #e11d48; font-weight: 800; white-space: nowrap; animation: scroll 12s linear infinite; font-family: 'Courier New', monospace; }}

            /* ÜST KÖŞE: AYARLAR VE OYUN */
            .top-right-panel {{
                position: absolute; top: 15px; right: 15px; z-index: 1000;
                display: flex; flex-direction: column; gap: 8px; align-items: flex-end;
            }}
            .small-btn {{ 
                background: white; border: 1.5px solid var(--tr-mavi); padding: 8px 12px;
                border-radius: 12px; font-size: 14px; cursor: pointer; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                display: flex; align-items: center; gap: 5px; font-weight: bold; color: var(--tr-mavi);
            }}

            /* 4. HARİTA (GENİŞLEMESİNE - TELEVİZYONUN ALTINDA) */
            .map-box {{ 
                width: 100%; height: 320px; background: white; border-radius: 20px; 
                padding: 10px; border: 2px solid var(--tr-mavi);
                box-shadow: 0 15px 35px rgba(30,58,138,0.15);
            }}
            #map {{ width: 100%; height: 100%; border-radius: 15px; }}

            /* DURAK ARAMA VE BİLGİ (SAĞ İNCE ŞERİT) */
            .info-bar {{
                position: absolute; right: 15px; top: 120px; width: 110px;
                background: rgba(255,255,255,0.9); backdrop-filter: blur(10px);
                border-radius: 20px; padding: 10px; border: 1px solid var(--tr-mavi);
                display: flex; flex-direction: column; gap: 10px; z-index: 500;
            }}
            .search-input {{ width: 100%; font-size: 10px; padding: 5px; border-radius: 5px; border: 1px solid #ccc; }}
            .bus-tag {{ background: var(--tr-mavi); color: white; font-size: 10px; padding: 5px; border-radius: 8px; text-align: center; font-weight: bold; }}

            /* 2. OYUN ALANI (EN ALT) */
            .game-footer {{
                margin-top: auto; background: white; border-radius: 15px 15px 0 0;
                padding: 10px; border-top: 3px solid var(--tr-altin); display: flex;
                justify-content: space-between; align-items: center;
            }}

            .digital-clock {{ font-size: 22px; font-weight: 900; color: var(--tr-mavi); }}

            @keyframes scroll {{ from {{ transform: translateX(100%); }} to {{ transform: translateX(-100%); }} }}
        </style>
    </head>
    <body>

        <!-- 3. Dijital Ekran (Karemsi TV) -->
        <div class="tv-frame">
            <div class="tv-display">
                <div class="scroll-text">🇹🇷 T.C. BELEDİYE TERMİNALİ | SİSTEM AKTİF | MEHMET TAHİR KOMUTASINDA...</div>
            </div>
        </div>

        <!-- 1. Sağ Üst Ayarlar -->
        <div class="top-right-panel">
            <div class="small-btn" onclick="alert('Ayarlar')">⚙️ Ayarlar</div>
            <div class="small-btn" onclick="alert('Oyun Başlıyor')">🕹️ Oyun</div>
        </div>

        <!-- 4. Harita (Genişlemesine) -->
        <div class="map-box">
            <div id="map"></div>
        </div>

        <!-- Sağ İnce Durak Paneli -->
        <div class="info-bar">
            <input type="text" class="search-input" placeholder="Hat Ara...">
            <div class="bus-tag">154: 2 Durak</div>
            <div class="bus-tag" style="background:#c5a059">İtimat: Yakın</div>
        </div>

        <!-- 2. Oyun ve Saat (En Alt) -->
        <div class="game-footer">
            <div style="font-size: 14px; font-weight: bold; color: #555;">🎮 Bekleme Alanı</div>
            <div class="digital-clock" id="clock">{simdi}</div>
        </div>

        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <script>
            // Saat
            setInterval(() => {{ 
                document.getElementById('clock').textContent = new Date().toLocaleTimeString('tr-TR', {{hour:'2-digit', minute:'2-digit'}}); 
            }}, 1000);

            // Harita (Adana)
            var map = L.map('map', {{zoomControl: false}}).setView([36.9914, 35.3308], 14);
            L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png').addTo(map);
            L.marker([36.9914, 35.3308]).addTo(map).bindPopup("<b>Mehmet Tahir Terminali</b>");
        </script>
    </body>
    </html>
    """
