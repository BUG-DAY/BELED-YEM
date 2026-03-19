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
        <title>Belediyem Komuta Merkezi 🛸</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <style>
            :root {{ --main-blue: #007aff; --accent-red: #ff3b30; --bg: #f5f7fa; }}
            * {{ box-sizing: border-box; font-family: 'Segoe UI', sans-serif; }}
            body {{ 
                background: var(--bg); margin: 0; padding: 10px; 
                display: flex; flex-direction: column; height: 100vh; gap: 10px;
            }}

            /* 2. REKLAM TELEVİZYONU (ÜST ORTA) */
            .tv-container {{
                width: 80%; margin: 0 auto; background: #222; border: 4px solid #444;
                border-radius: 12px; padding: 5px; box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            }}
            .tv-screen {{ background: #000; height: 30px; overflow: hidden; display: flex; align-items: center; border-radius: 4px; }}
            .scroll-text {{ color: var(--accent-red); font-weight: bold; white-space: nowrap; animation: scroll 15s linear infinite; font-family: monospace; }}

            /* ANA DİZİLİM */
            .main-frame {{ display: flex; flex: 1; gap: 10px; min-height: 0; }}

            /* 4. SOL PANEL (AYARLAR & OYUN - GENİŞ) */
            .left-panel {{ 
                width: 25%; background: white; border-radius: 20px; padding: 15px;
                display: flex; flex-direction: column; gap: 20px; border: 1px solid #ddd;
                box-shadow: 5px 0 15px rgba(0,0,0,0.02);
            }}
            .panel-box {{ background: var(--bg); padding: 10px; border-radius: 12px; border: 1px solid #eee; }}
            .panel-box h3 {{ margin: 0 0 10px 0; font-size: 14px; color: var(--main-blue); }}

            /* 1. HARİTA (ORTADA ŞIK) */
            .map-wrapper {{ 
                flex: 1; background: white; border-radius: 25px; padding: 8px;
                border: 2px solid var(--main-blue); box-shadow: 0 10px 30px rgba(0,122,255,0.1);
            }}
            #map {{ width: 100%; height: 100%; border-radius: 18px; }}

            /* 3. SAĞ PANEL (ARAMA & DURAK - İNCE UZUN) */
            .right-panel {{ 
                width: 18%; background: white; border-radius: 20px; padding: 10px;
                display: flex; flex-direction: column; gap: 10px; border: 1px solid #ddd;
            }}
            .search-box input {{ 
                width: 100%; padding: 8px; border-radius: 10px; border: 1px solid #ccc; font-size: 12px;
            }}
            .bus-info-card {{ 
                background: linear-gradient(to bottom, #fff, #f0f7ff); 
                padding: 10px; border-radius: 12px; border-left: 4px solid var(--main-blue);
            }}
            .info-label {{ font-size: 10px; color: #888; text-transform: uppercase; }}
            .info-value {{ font-size: 13px; font-weight: 800; color: var(--main-blue); }}

            /* ALT SAAT */
            .footer {{ text-align: center; font-weight: 900; color: var(--main-blue); font-size: 18px; }}

            @keyframes scroll {{ from {{ transform: translateX(100%); }} to {{ transform: translateX(-100%); }} }}
        </style>
    </head>
    <body>
        <!-- 2. TV Reklam Panosu -->
        <div class="tv-container">
            <div class="tv-screen">
                <div class="scroll-text">📺 CANLI YAYIN: ADANA BÜYÜKŞEHİR TERMİNALİ | MEHMET TAHİR SUNAR...</div>
            </div>
        </div>

        <div class="main-frame">
            <!-- 4. Sol Panel (Geniş) -->
            <div class="left-panel">
                <div class="panel-box">
                    <h3>⚙️ SİSTEM AYARI</h3>
                    <select style="width:100%;" onchange="location.href='/?sehir='+this.value">
                        <option value="Adana">Adana</option>
                        <option value="İstanbul">İstanbul</option>
                        <option value="Ankara">Ankara</option>
                    </select>
                </div>
                <div class="panel-box" style="flex:1;">
                    <h3>🎮 MOLA ALANI</h3>
                    <div style="text-align:center; font-size:30px; margin-top:20px;">🕹️</div>
                    <p style="font-size:11px; color:#666; text-align:center;">XOX ve mini oyunlar bu geniş alana gelecek.</p>
                </div>
            </div>

            <!-- 1. Harita (Orta) -->
            <div class="map-wrapper">
                <div id="map"></div>
            </div>

            <!-- 3. Sağ Panel (İnce Uzun) -->
            <div class="right-panel">
                <div class="search-box">
                    <input type="text" placeholder="Otobüs No Ara (Örn: 154)" id="busSearch">
                </div>
                <div class="bus-info-card">
                    <div class="info-label">Seçili Hat</div>
                    <div class="info-value" id="currentBus">Hat 154</div>
                    <hr style="border:0; border-top:1px solid #eee; margin:10px 0;">
                    <div class="info-label">Kalan Durak</div>
                    <div class="info-value" id="eta">3 Durak</div>
                    <div class="info-label" style="margin-top:10px;">Şu anki Durak</div>
                    <div class="info-value" style="font-size:11px;">Yüreğir İstasyonu</div>
                </div>
            </div>
        </div>

        <div class="footer" id="clock">{simdi}</div>

        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <script>
            // Saat
            setInterval(() => {{ document.getElementById('clock').textContent = new Date().toLocaleTimeString('tr-TR', {{hour:'2-digit', minute:'2-digit'}}); }}, 1000);

            // Dinamik Durak Verisi
            let durakSayisi = 5;
            setInterval(() => {{
                durakSayisi = durakSayisi > 0 ? durakSayisi - 1 : 5;
                document.getElementById('eta').textContent = durakSayisi === 0 ? "DURAKTA" : durakSayisi + " Durak";
            }}, 5000);

            // Harita
            var map = L.map('map', {{zoomControl: false}}).setView([36.9914, 35.3308], 14);
            L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png').addTo(map);
            L.marker([36.9914, 35.3308]).addTo(map).bindPopup("<b>Adana Komuta Merkezi</b>");
        </script>
    </body>
    </html>
    """
