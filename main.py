from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import datetime

app = FastAPI()

sehir_detaylari = {
    "Adana": {"duraklar": ["154 - 2 dk", "172 - Yakın", "İtimat 1 - 15 dk"], "koordinat": [36.9914, 35.3308], "zoom": 14},
    "İstanbul": {"duraklar": ["Metro - 1 dk", "Vapur - 5 dk", "500T - Durak"], "koordinat": [41.0082, 28.9784], "zoom": 12},
    "Ankara": {"duraklar": ["Ankaray - 3 dk", "EGO 413 - 10 dk"], "koordinat": [39.9334, 32.8597], "zoom": 13}
}

@app.get("/", response_class=HTMLResponse)
async def read_root(sehir: str = "Adana"):
    simdi = datetime.datetime.now().strftime("%H:%M")
    detay = sehir_detaylari.get(sehir, sehir_detaylari["Adana"])
    otobus_listesi_html = "".join([f"<li>{hat}</li>" for hat in detay["duraklar"]])
    lat, lon, zoom = detay["koordinat"][0], detay["koordinat"][1], detay["zoom"]

    return f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Belediyem Premium 🛸</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <style>
            :root {{ --main-blue: #007aff; --bg: #f2f2f7; --card: rgba(255, 255, 255, 0.9); }}
            * {{ box-sizing: border-box; font-family: -apple-system, sans-serif; }}
            body {{ 
                background: var(--bg); margin: 0; padding: 15px; 
                display: flex; flex-direction: column; height: 100vh; gap: 12px;
            }}

            /* REKLAM BANDI (SABİT ÜST) */
            .ads-container {{ 
                background: var(--main-blue); color: white; padding: 12px; 
                border-radius: 18px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,122,255,0.2);
            }}
            .scroll {{ display: inline-block; white-space: nowrap; animation: scroll 15s linear infinite; font-weight: 600; font-size: 13px; }}

            /* ANA GÖVDE (HARİTA VE SAĞ PANEL) */
            .content-area {{ display: flex; flex: 1; gap: 10px; min-height: 0; }}

            /* HARİTA KUTUSU (BİRAZ KÜÇÜLTÜLMÜŞ VE YUVARLATILMIŞ) */
            #map {{ 
                flex: 1; border-radius: 25px; border: 3px solid white;
                box-shadow: inset 0 0 10px rgba(0,0,0,0.05), 0 10px 20px rgba(0,0,0,0.05);
            }}

            /* SAĞ DOCK (İNCE PANEL) */
            .right-dock {{
                width: 85px; background: var(--card); backdrop-filter: blur(10px);
                border-radius: 22px; padding: 12px 5px; display: flex; 
                flex-direction: column; align-items: center; border: 1px solid white;
            }}
            .right-dock h4 {{ color: var(--main-blue); font-size: 10px; margin: 0 0 10px 0; letter-spacing: 1px; }}
            ul {{ list-style: none; padding: 0; margin: 0; width: 100%; }}
            li {{ 
                background: white; color: var(--main-blue); font-size: 9px; 
                padding: 10px 4px; margin-bottom: 8px; border-radius: 12px; 
                text-align: center; font-weight: 700; border: 1px solid #e5e5ea;
            }}

            /* ALT KONTROLLER */
            .bottom-bar {{ display: flex; justify-content: space-between; align-items: center; padding: 5px; }}
            .btn-group {{ display: flex; gap: 12px; }}
            .circle-btn {{ 
                width: 50px; height: 50px; background: white; color: var(--main-blue); 
                border-radius: 50%; display: flex; align-items: center; justify-content: center; 
                font-size: 22px; box-shadow: 0 5px 15px rgba(0,0,0,0.08); border: 1px solid #ddd;
            }}
            .digital-clock {{ 
                background: white; padding: 10px 20px; border-radius: 20px; 
                font-weight: 800; color: #1c1c1e; font-size: 16px; border: 1px solid #ddd;
            }}

            /* MODAL */
            .glass-modal {{ 
                display: none; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
                width: 80%; background: white; border-radius: 25px; padding: 20px; z-index: 2000;
                box-shadow: 0 25px 50px rgba(0,0,0,0.2); border: 1px solid #eee;
            }}

            @keyframes scroll {{ from {{ transform: translateX(100%); }} to {{ transform: translateX(-100%); }} }}
        </style>
    </head>
    <body>
        <div class="ads-container">
            <div class="scroll">🏙️ BELEDİYEM PREMIUM: Mehmet Tahir Özel Versiyon | Hatlar %100 Senkronize...</div>
        </div>

        <div class="content-area">
            <div id="map"></div>
            
            <div class="right-dock">
                <h4>HATLAR</h4>
                <ul>{otobus_listesi_html}</ul>
            </div>
        </div>

        <div class="bottom-bar">
            <div class="btn-group">
                <div class="circle-btn" onclick="toggleM('s-modal')">⚙️</div>
                <div class="circle-btn" onclick="toggleM('g-modal')">🎮</div>
            </div>
            <div class="digital-clock" id="clock">{simdi}</div>
        </div>

        <div id="s-modal" class="glass-modal">
            <div style="display:flex; justify:space-between; align-items:center;">
                <h3 style="margin:0; color:var(--main-blue);">Ayarlar</h3>
                <span onclick="toggleM('s-modal')" style="font-size:24px; cursor:pointer;">&times;</span>
            </div>
            <select style="width:100%; padding:12px; margin-top:15px; border-radius:12px; border:1px solid #ddd;" onchange="location.href='/?sehir=' + this.value">
                <option value="Adana" {"selected" if sehir=="Adana" else ""}>Adana</option>
                <option value="İstanbul" {"selected" if sehir=="İstanbul" else ""}>İstanbul</option>
                <option value="Ankara" {"selected" if sehir=="Ankara" else ""}>Ankara</option>
            </select>
        </div>

        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <script>
            function toggleM(id) {{ 
                const m = document.getElementById(id); 
                m.style.display = (m.style.display === 'block') ? 'none' : 'block'; 
            }}
            
            setInterval(() => {{ 
                document.getElementById('clock').textContent = new Date().toLocaleTimeString('tr-TR', {{hour:'2-digit', minute:'2-digit'}}); 
            }}, 1000);

            var map = L.map('map', {{zoomControl: false}}).setView([{lat}, {lon}], {zoom});
            L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png').addTo(map);
            L.marker([{lat}, {lon}]).addTo(map).bindPopup("<b>{sehir} Terminal</b>");
        </script>
    </body>
    </html>
    """
