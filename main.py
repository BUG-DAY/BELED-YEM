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
        <title>Belediyem - Akıllı Ulaşım Sistemleri 🛸</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <style>
            :root {{ --tr-mavi: #1e3a8a; --tr-altin: #c5a059; --tr-kirmizi: #e11d48; --glass: rgba(255,255,255,0.9); }}
            * {{ box-sizing: border-box; font-family: 'Segoe UI', Tahoma, sans-serif; }}
            
            body {{ 
                margin: 0; height: 100vh; display: flex; align-items: center; justify-content: center;
                background: #e2e8f0; background-image: url('https://www.transparenttextures.com/patterns/cubes.png');
            }}

            .terminal-square {{
                width: 95vw; height: 95vw; max-width: 520px; max-height: 520px;
                background: white; border-radius: 35px; overflow: hidden;
                position: relative; display: flex; flex-direction: column;
                box-shadow: 0 40px 100px rgba(0,0,0,0.3); border: 4px solid var(--tr-mavi);
            }}

            /* TV PANELİ */
            .tv-strip {{ background: #000; padding: 12px; border-bottom: 3px solid var(--tr-altin); z-index: 1000; }}
            .scroll {{ color: #00ff41; font-weight: 900; white-space: nowrap; animation: scroll 15s linear infinite; font-family: 'Courier New', monospace; font-size: 13px; }}

            .content {{ flex: 1; position: relative; display: flex; overflow: hidden; }}
            #map {{ flex: 1; z-index: 1; }}

            /* SAĞ PANEL - PROFESYONEL VERİ AKIŞI */
            .right-track {{
                width: 90px; background: var(--glass); backdrop-filter: blur(10px);
                border-left: 2px solid var(--tr-mavi); z-index: 50;
                display: flex; flex-direction: column; align-items: center; padding: 10px 5px; gap: 8px;
            }}
            .bus-card {{ 
                width: 100%; background: white; padding: 8px 2px; border-radius: 12px; 
                text-align: center; border: 1px solid #ddd; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            }}
            .bus-id {{ font-size: 10px; font-weight: 800; color: var(--tr-mavi); }}
            .bus-time {{ font-size: 11px; font-weight: 900; color: var(--tr-kirmizi); }}

            /* HAVA DURUMU (SUNUM İÇİN KRİTİK) */
            .weather-box {{
                position: absolute; top: 70px; left: 60px; z-index: 500;
                background: var(--glass); padding: 5px 12px; border-radius: 15px;
                font-size: 12px; font-weight: bold; color: #333; border: 1px solid #fff;
            }}

            .footer-bar {{ background: white; padding: 10px; text-align: center; border-top: 1.5px solid #eee; display: flex; justify-content: space-around; align-items: center; }}
            .clock {{ font-size: 20px; font-weight: 900; color: var(--tr-mavi); }}
            .belediye-logo {{ font-size: 10px; font-weight: bold; color: #666; }}

            @keyframes scroll {{ from {{ transform: translateX(100%); }} to {{ transform: translateX(-100%); }} }}
        </style>
    </head>
    <body>
        <div class="terminal-square">
            <div class="tv-strip">
                <div class="scroll">📡 YÜREĞİR AKILLI ULAŞIM SİSTEMİ | CANLI VERİ ENTEGRASYONU AKTİF | SUNUM MODU: MEHMET TAHİR</div>
            </div>

            <div class="weather-box">☀️ Adana: 28°C</div>

            <div class="content">
                <div id="map"></div>

                <div class="right-track">
                    <div class="bus-card">
                        <div class="bus-id">Hat 154</div>
                        <div class="bus-time" id="t1">Hesaplanıyor..</div>
                    </div>
                    <div class="bus-card">
                        <div class="bus-id">İtimat 1</div>
                        <div class="bus-time" id="t2">Hesaplanıyor..</div>
                    </div>
                    <div class="bus-card">
                        <div class="bus-id">Hat 172</div>
                        <div class="bus-time" id="t3">Hesaplanıyor..</div>
                    </div>
                </div>
            </div>

            <div class="footer-bar">
                <div class="belediye-logo">YÜREĞİR BELEDİYESİ</div>
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

            // Üç Farklı Hat İkonu
            function createBus(color) {{
                return L.divIcon({{
                    html: <div style="background: ${{color}}; border: 2px solid white; border-radius: 50%; width: 22px; height: 22px; display: flex; align-items:center; justify-content:center; color:white; font-size:10px;">🚌</div>,
                    className: 'bus-icon'
                }});
            }}

            var b1 = L.marker([36.9914, 35.3308], {{icon: createBus('#1e3a8a')}}).addTo(map);
            var b2 = L.marker([36.9950, 35.3400], {{icon: createBus('#c5a059')}}).addTo(map);
            var b3 = L.marker([36.9850, 35.3200], {{icon: createBus('#e11d48')}}).addTo(map);

            let angle = 0;
            setInterval(() => {{
                angle += 0.005;
                // Hat 154 (Dairesel)
                b1.setLatLng([36.9914 + Math.sin(angle)*0.006, 35.3308 + Math.cos(angle)*0.006]);
                // İtimat (Yatay)
                b2.setLatLng([36.9950, 35.3400 + Math.sin(angle)*0.008]);
                // Hat 172 (Dikey)
                b3.setLatLng([36.9850 + Math.cos(angle)*0.007, 35.3200]);

                // Canlı Süre Hesaplama (Simüle)
                document.getElementById('t1').textContent = Math.abs(Math.floor(Math.sin(angle)*5 + 6)) + " dk";
                document.getElementById('t2').textContent = Math.abs(Math.floor(Math.cos(angle)*4 + 5)) + " dk";
                document.getElementById('t3').textContent = Math.abs(Math.floor(Math.sin(angle)*3 + 4)) + " dk";
            }}, 100);
        </script>
    </body>
    </html>
    """
