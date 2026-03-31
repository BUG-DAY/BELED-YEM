from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import datetime

app = FastAPI()

# AÇIK VERİ SAĞLAYAN İLLER VE GERÇEKÇİ OTOBÜS SAATLERİ (Moovit Mantığı)
VERILER = {
    "Adana": {
        "coords": [36.9914, 35.3308],
        "hatlar": [("154", "Barajyolu", "2 Dk"), ("114", "Çukurova", "5 Dk"), ("172", "Balcalı", "8 Dk"), ("İtimat 1", "Merkez", "DURAKTA"), ("Cemalpasa", "Meydan", "12 Dk")]
    },
    "İstanbul": {
        "coords": [41.0082, 28.9784],
        "hatlar": [("34G", "Beylikdüzü", "1 Dk"), ("500T", "Tuzla", "4 Dk"), ("15F", "Kadıköy", "7 Dk"), ("11ÜS", "Üsküdar", "9 Dk")]
    },
    "Ankara": {
        "coords": [39.9334, 32.8597],
        "hatlar": [("413", "Altınpark", "3 Dk"), ("297", "Batıkent", "6 Dk"), ("114", "Kızılay", "10 Dk"), ("220", "Mamak", "15 Dk")]
    },
    "İzmir": {
        "coords": [38.4237, 27.1428],
        "hatlar": [("202", "Havalimanı", "5 Dk"), ("90", "Gaziemir", "8 Dk"), ("690", "F.Altay", "11 Dk")]
    },
    "Bursa": {
        "coords": [40.1824, 29.0611],
        "hatlar": [("38", "Terminal", "4 Dk"), ("94", "Heykel", "7 Dk"), ("B39", "Nilüfer", "12 Dk")]
    },
    "Kocaeli": {
        "coords": [40.8533, 29.8815],
        "hatlar": [("200", "Kartal", "5 Dk"), ("134", "Umuttepe", "8 Dk"), ("11", "Otogar", "14 Dk")]
    },
    "Konya": {
        "coords": [37.8714, 32.4846],
        "hatlar": [("1", "Kampüs", "2 Dk"), ("4", "Meram", "6 Dk"), ("64", "Bosna", "9 Dk")]
    }
}

@app.get("/", response_class=HTMLResponse)
async def read_root(sehir: str = "Adana"):
    simdi = datetime.datetime.now().strftime("%H:%M")
    
    # Şehir verisini güvenli çekme
    aktif_veri = VERILER.get(sehir, VERILER["Adana"])
    lat, lng = aktif_veri["coords"]
    
    # Moovit Tarzı Sağ Panel Otobüs Listesi HTML'i
    otobus_html = ""
    for kod, guzergah, sure in aktif_veri["hatlar"]:
        renk = "#10b981" if "Dk" in sure and int(sure.split()[0]) < 4 or sure == "DURAKTA" else "#3b82f6"
        otobus_html += f"""
        <div class="bus-item">
            <div class="bus-left">
                <div class="bus-code">{kod}</div>
                <div class="bus-route">{guzergah}</div>
            </div>
            <div class="bus-time" style="color: {renk};">{sure}</div>
        </div>
        """
    
    # Şehir Seçici HTML'i
    secici_html = ""
    for s in sorted(VERILER.keys()):
        sel = "selected" if sehir == s else ""
        secici_html += f'<option value="{s}" {sel}>{s}</option>'

    return f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Yerli Ulaşım Matrisi</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <style>
            * {{ box-sizing: border-box; font-family: 'Segoe UI', system-ui, sans-serif; margin: 0; padding: 0; }}
            body {{ background: #e2e8f0; height: 100vh; display: flex; align-items: center; justify-content: center; overflow: hidden; }}

            /* SADE VE PROFESYONEL ÇERÇEVE */
            .app-frame {{
                width: 100vw; height: 100vh; max-width: 500px; max-height: 850px;
                background: #ffffff; display: flex; flex-direction: column;
                position: relative; box-shadow: 0 10px 40px rgba(0,0,0,0.15);
            }}
            @media (min-width: 500px) {{ .app-frame {{ border-radius: 20px; border: 4px solid #1e293b; height: 90vh; }} }}

            /* 3. MADDE: DİJİTAL EKRAN (Geri Döndü) */
            .digital-led {{
                background: #000; padding: 10px; border-bottom: 2px solid #0ea5e9; z-index: 1000;
            }}
            .led-scroll {{ overflow: hidden; white-space: nowrap; }}
            .led-text {{
                display: inline-block; color: #38bdf8; font-family: 'Courier New', monospace;
                font-size: 14px; font-weight: bold; animation: scroll-left 15s linear infinite;
            }}

            /* 4. MADDE: HARİTA KESİN ÇÖZÜMÜ */
            .map-area {{ flex: 1; position: relative; width: 100%; background: #cbd5e1; }}
            #map {{ position: absolute; top: 0; bottom: 0; left: 0; right: 0; width: 100%; height: 100%; z-index: 1; }}

            /* 1. MADDE: YERLİ MOOVİT SAĞ PANEL */
            .moovit-panel {{
                position: absolute; top: 10px; right: 10px; bottom: 10px; width: 160px;
                background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px);
                border-radius: 12px; border: 1px solid #cbd5e1; box-shadow: 0 5px 15px rgba(0,0,0,0.2);
                z-index: 1000; display: flex; flex-direction: column; overflow: hidden;
            }}
            
            .search-box {{ padding: 10px; background: #f8fafc; border-bottom: 1px solid #e2e8f0; }}
            .search-input {{
                width: 100%; padding: 8px; border-radius: 6px; border: 1px solid #94a3b8;
                font-size: 12px; font-weight: bold; outline: none;
            }}
            
            .bus-list {{ flex: 1; overflow-y: auto; padding: 5px; display: flex; flex-direction: column; gap: 5px; }}
            .bus-item {{
                background: #fff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 8px;
                display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 4px rgba(0,0,0,0.02);
            }}
            .bus-code {{ font-size: 13px; font-weight: 900; color: #1e293b; }}
            .bus-route {{ font-size: 9px; color: #64748b; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 60px; }}
            .bus-time {{ font-size: 11px; font-weight: 900; }}

            /* ALT KONTROL PANELİ */
            .bottom-dock {{
                background: #ffffff; padding: 15px; border-top: 1px solid #cbd5e1;
                display: flex; justify-content: space-between; align-items: center; z-index: 1000;
            }}
            .city-select {{
                padding: 10px; border-radius: 8px; border: 2px solid #3b82f6;
                font-size: 15px; font-weight: bold; background: #f0f9ff; color: #1e293b; outline: none; cursor: pointer; width: 60%;
            }}
            .clock-badge {{ background: #1e293b; color: white; padding: 8px 15px; border-radius: 8px; font-weight: bold; font-size: 16px; }}

            @keyframes scroll-left {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}
        </style>
    </head>
    <body>

        <div class="app-frame">
            
            <div class="digital-led">
                <div class="led-scroll">
                    <div class="led-text">
                        T.C. AÇIK VERİ ULAŞIM AĞI | ŞEHİR: {sehir.upper()} | CANLI GPS TAKİBİ VE DURAK SAATLERİ AKTİF...
                    </div>
                </div>
            </div>

            <div class="map-area">
                <div id="map"></div>
                
                <div class="moovit-panel">
                    <div class="search-box">
                        <input type="text" class="search-input" id="busSearch" placeholder="🔍 Hat Ara...">
                    </div>
                    <div class="bus-list" id="busListContainer">
                        {otobus_html}
                    </div>
                </div>
            </div>

            <div class="bottom-dock">
                <select class="city-select" onchange="location.href='/?sehir=' + this.value">
                    {secici_html}
                </select>
                <div class="clock-badge" id="live-clock">{simdi}</div>
            </div>

        </div>

        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <script>
            // 1. HARİTA KESİN YÜKLEME KODU
            var map = L.map('map', {{ zoomControl: false }}).setView([{lat}, {lng}], 13);
            
            L.tileLayer('https://{{s}}.basemaps.cartocdn.com/rastertiles/voyager/{{z}}/{{x}}/{{y}}{{r}}.png', {{
                maxZoom: 19, attribution: '© OSMap'
            }}).addTo(map);

            // Haritanın gri/beyaz kalmasını önleyen sihirli dokunuş
            window.onload = function() {{
                setTimeout(function() {{
                    map.invalidateSize();
                    window.dispatchEvent(new Event('resize'));
                }}, 300);
            }};

            // 2. OTOBÜS ARAMA FİLTRESİ (Aşırı Hızlı Vanilla JS)
            document.getElementById('busSearch').addEventListener('keyup', function(e) {{
                let filter = e.target.value.toUpperCase();
                let items = document.querySelectorAll('.bus-item');
                items.forEach(item => {{
                    let text = item.textContent.toUpperCase();
                    item.style.display = text.includes(filter) ? "flex" : "none";
                }});
            }});

            // 3. HARİTAYA RASTGELE CANLI OTOBÜS İKONLARI
            const busIcon = L.divIcon({{
                html: <div style="background:#10b981; width:24px; height:24px; border-radius:50%; border:2px solid white; display:flex; align-items:center; justify-content:center; color:white; font-size:11px; box-shadow:0 2px 5px rgba(0,0,0,0.3);">🚍</div>,
                className: 'dummy'
            }});
            
            const buses = [];
            for(let i=0; i<4; i++) {{
                let b = L.marker([{lat} + (Math.random()-0.5)*0.04, {lng} + (Math.random()-0.5)*0.04], {{icon: busIcon}}).addTo(map);
                buses.push(b);
            }}

            setInterval(() => {{
                buses.forEach(b => {{
                    let curr = b.getLatLng();
                    b.setLatLng([curr.lat + (Math.random()-0.5)*0.002, curr.lng + (Math.random()-0.5)*0.002]);
                }});
            }}, 2000);

            // 4. CANLI SAAT
            setInterval(() => {{
                document.getElementById('live-clock').textContent = new Date().toLocaleTimeString('tr-TR', {{hour:'2-digit', minute:'2-digit'}});
            }}, 1000);
        </script>
    </body>
    </html>
    """
