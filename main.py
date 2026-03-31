from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import datetime

app = FastAPI()

# TÜRKİYE GENELİ ŞEHİR VE YOL VERİLERİ (Path Tracking Altyapısı)
SEHIR_VERILERI = {
    "Adana": {
        "merkez": [37.015, 35.315], "hava": "28°C Güneşli",
        "hatlar": [{"id": "154", "yol": [[37.012, 35.320], [37.018, 35.325], [37.021, 35.328]]},
                  {"id": "İtimat", "yol": [[37.025, 35.295], [37.019, 35.305], [37.015, 35.310]]}]
    },
    "İstanbul": {
        "merkez": [41.008, 28.978], "hava": "18°C Parçalı Bulutlu",
        "hatlar": [{"id": "34G", "yol": [[41.065, 29.010], [41.055, 28.970], [41.050, 28.950]]},
                  {"id": "500T", "yol": [[41.075, 29.015], [41.085, 29.035], [41.090, 29.045]]}]
    },
    "Ankara": {
        "merkez": [39.933, 32.859], "hava": "15°C Hafif Yağmurlu",
        "hatlar": [{"id": "EGO-413", "yol": [[39.920, 32.854], [39.930, 32.858], [39.935, 32.860]]}]
    },
    "İzmir": {
        "merkez": [38.423, 27.142], "hava": "22°C Açık",
        "hatlar": [{"id": "ESHOT-202", "yol": [[38.430, 27.150], [38.440, 27.160], [38.450, 27.170]]}]
    },
    "Bursa": {
        "merkez": [40.182, 29.061], "hava": "14°C Sisli",
        "hatlar": [{"id": "Bursaray", "yol": [[40.190, 29.070], [40.200, 29.080], [40.210, 29.090]]}]
    }
}

@app.get("/", response_class=HTMLResponse)
async def read_root(sehir: str = "Adana"):
    simdi = datetime.datetime.now().strftime("%H:%M")
    config = SEHIR_VERILERI.get(sehir, SEHIR_VERILERI["Adana"])
    
    return f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Ulaşım İzleme Terminali</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <style>
            :root {{ --neon-red: #ff0000; --deep-bg: #050505; --ui-blue: #007aff; }}
            * {{ box-sizing: border-box; font-family: 'Inter', sans-serif; -webkit-font-smoothing: antialiased; }}
            body {{ margin: 0; background: #111; height: 100vh; display: flex; align-items: center; justify-content: center; overflow: hidden; }}

            /* MOBİL CİHAZ ÇERÇEVESİ (DİKEY) */
            .mobile-frame {{
                width: 100vw; height: 100vh; max-width: 450px; max-height: 850px;
                background: var(--deep-bg); display: flex; flex-direction: column;
                border: 4px solid #333; border-radius: 40px; overflow: hidden; position: relative;
            }}

            /* DİJİTAL LED EKRAN (TV BANDI) */
            .digital-led {{
                background: #000; border-bottom: 3px solid #222; padding: 15px 10px;
                box-shadow: inset 0 0 15px rgba(255,0,0,0.2);
            }}
            .ticker-wrap {{ overflow: hidden; white-space: nowrap; }}
            .ticker-text {{
                display: inline-block; color: var(--neon-red); font-family: 'Courier New', monospace;
                font-weight: 900; font-size: 16px; text-transform: uppercase;
                animation: ticker 20s linear infinite; text-shadow: 0 0 8px rgba(255,0,0,0.6);
            }}

            /* HARİTA ALANI */
            #map {{ flex: 1; z-index: 1; filter: grayscale(0.2) contrast(1.1); }}

            /* ALT KONTROL PANELİ */
            .bottom-dock {{
                background: rgba(20,20,20,0.95); backdrop-filter: blur(20px);
                padding: 15px; border-top: 2px solid #333; display: flex; flex-direction: column; gap: 12px;
            }}
            .selector-row {{ display: flex; gap: 10px; align-items: center; }}
            select {{ 
                flex: 1; background: #222; color: #fff; border: 1px solid #444; 
                padding: 12px; border-radius: 12px; font-weight: bold; font-size: 14px;
            }}
            
            /* CANLI HAT KARTLARI */
            .live-stats {{ display: flex; gap: 8px; overflow-x: auto; padding-bottom: 5px; }}
            .mini-card {{ 
                min-width: 100px; background: #333; padding: 10px; border-radius: 12px; 
                border-left: 4px solid var(--ui-blue); text-align: center;
            }}
            .bus-id {{ font-size: 10px; color: #aaa; }}
            .bus-eta {{ font-size: 12px; font-weight: 900; color: #fff; }}

            @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}
        </style>
    </head>
    <body>

        <div class="mobile-frame">
            <div class="digital-led">
                <div class="ticker-wrap">
                    <div class="ticker-text" id="ticker-content">
                        ŞEHİR: {sehir.upper()} | HAVA: {config['hava']} | SİSTEM DURUMU: %100 AKTİF | MEHMET TAHİR TERMİNALİ CANLI YAYINDA...
                    </div>
                </div>
            </div>

            <div id="map"></div>

            <div class="bottom-dock">
                <div class="selector-row">
                    <select onchange="location.href='/?sehir=' + this.value">
                        {" ".join([f'<option value="{s}" {"selected" if sehir==s else ""}>{s}</option>' for s in SEHIR_VERILERI.keys()])}
                    </select>
                    <div style="color: #fff; font-weight: 900; font-size: 18px;" id="clock">{simdi}</div>
                </div>
                
                <div class="live-stats" id="bus-list">
                    </div>
            </div>
        </div>

        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <script>
            const data = {SEHIR_VERILERI};
            const current = data["{sehir}"];

            // Harita (Ciddi Tema)
            var map = L.map('map', {{ zoomControl: false }}).setView(current.merkez, 13);
            L.tileLayer('https://{{s}}.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}{{r}}.png').addTo(map);

            const markers = {{}};
            const list = document.getElementById('bus-list');

            current.hatlar.forEach(hat => {{
                // Rota Çizgisi
                L.polyline(hat.yol, {{ color: '#007aff', weight: 2, opacity: 0.4 }}).addTo(map);

                // Otobüs İkonu
                const icon = L.divIcon({{
                    html: <div style="background:#007aff; color:white; padding:5px; border-radius:50%; border:2px solid #fff; font-size:12px; box-shadow:0 0 10px rgba(0,122,255,0.5);">🚌</div>,
                    className: 'bus-ptr'
                }});
                markers[hat.id] = L.marker(hat.yol[0], {{ icon: icon }}).addTo(map);

                // Kart Ekle
                list.innerHTML += `
                    <div class="mini-card">
                        <div class="bus-id">HAT ${{hat.id}}</div>
                        <div class="bus-eta" id="eta-${{hat.id}}">Hesaplanıyor</div>
                    </div>
                `;
            }});

            // Gerçekçi Yol İzleme Simülasyonu
            let tick = 0;
            setInterval(() => {{
                tick++;
                current.hatlar.forEach(hat => {{
                    const p = hat.yol;
                    const idx = Math.floor((tick % (p.length * 20)) / 20);
                    const nIdx = (idx + 1) % p.length;
                    
                    const lat = p[idx][0] + (p[nIdx][0] - p[idx][0]) * ((tick % 20) / 20);
                    const lng = p[idx][1] + (p[nIdx][1] - p[idx][1]) * ((tick % 20) / 20);
                    
                    markers[hat.id].setLatLng([lat, lng]);
                    document.getElementById('eta-' + hat.id).textContent = (Math.abs(5 - idx)) + " DK KALDI";
                }});
            }}, 150);

            // Saat
            setInterval(() => {{ document.getElementById('clock').textContent = new Date().toLocaleTimeString('tr-TR', {{hour:'2-digit', minute:'2-digit'}}); }}, 1000);
        </script>
    </body>
    </html>
    """
