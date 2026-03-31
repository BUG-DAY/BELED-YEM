from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import datetime

app = FastAPI(title="Ulaşım Matrisi")

# Tüm şehir altyapısı burada (yeni şehir eklemek çok kolay)
CITIES = {
    "Adana": {
        "center": [36.9914, 35.3308],
        "name": "Adana",
        "bus_led": "📡 ADANA BÜYÜKŞEHİR BELEDİYESİ • CANLI TAKİP AKTİF",
        "metro_led": "🚇 ADANA METRO • DAKİK SEFERLER",
        "bus_color": "#2563eb"
    },
    "Ankara": {
        "center": [39.9334, 32.8597],
        "name": "Ankara",
        "bus_led": "📡 EGO GENEL MÜDÜRLÜĞÜ • CANLI OTOBÜS TAKİBİ",
        "metro_led": "🚇 ANKARAY & METRO • GERÇEK ZAMANLI",
        "bus_color": "#10b981"
    },
    "Istanbul": {
        "center": [41.0082, 28.9784],
        "name": "İstanbul",
        "bus_led": "📡 İETT & METROBÜS • CANLI FİLO TAKİBİ",
        "metro_led": "🚇 İSTANBUL METRO • METROBÜS • TRAMVAY",
        "bus_color": "#db2777"
    }
    # Buraya yeni şehir ekleyebilirsin → "Izmir": { ... }
}

@app.get("/", response_class=HTMLResponse)
async def read_root(sehir: str = "Adana"):
    simdi = datetime.datetime.now().strftime("%H:%M")
    city_key = sehir.capitalize()
    city = CITIES.get(city_key, CITIES["Adana"])

    center_lat, center_lng = city["center"]
    city_name = city["name"]
    bus_led = city["bus_led"]
    metro_led = city["metro_led"]
    bus_color = city["bus_color"]

    html = f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>{city_name} Ulaşım Matrisi</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <style>
            :root {{ --blue: #2563eb; --pink: #db2777; --orange: #ea580c; --green: #10b981; --dark: #0f172a; }}
            * {{ box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin:0; padding:0; user-select:none; -webkit-tap-highlight-color:transparent; }}
            body {{ background:#000; height:100vh; display:flex; align-items:center; justify-content:center; overflow:hidden; }}
            
            .app-container {{ 
                width:100vw; height:100vh; max-width:450px; max-height:850px;
                background:#f8fafc; position:relative; overflow:hidden; border-radius:0;
            }}
            @media (min-width:460px) {{ 
                .app-container {{ border-radius:42px; border:14px solid #1e293b; height:92vh; box-shadow:0 0 40px rgba(0,0,0,0.4); }} 
            }}

            #map-layer {{ position:absolute; top:0; left:0; width:100%; height:100%; z-index:1; }}

            #home-overlay {{
                position:absolute; top:0; left:0; width:100%; height:100%; background:#f8fafc; z-index:3000;
                display:flex; flex-direction:column; padding:35px 25px; transition:transform 0.5s cubic-bezier(0.32, 0.72, 0, 1);
            }}
            .welcome {{ font-size:28px; font-weight:900; color:var(--dark); line-height:1.05; }}
            .welcome span {{ color:var(--blue); }}
            .sub-welcome {{ font-size:15.5px; color:#64748b; font-weight:600; margin-top:8px; }}

            .menu-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:18px; margin-top:30px; }}
            .card {{
                background:white; border-radius:26px; padding:28px 14px; text-align:center;
                box-shadow:0 12px 30px rgba(0,0,0,0.08); cursor:pointer; transition:all 0.25s ease;
            }}
            .card:active {{ transform:scale(0.94); box-shadow:0 8px 20px rgba(0,0,0,0.1); }}
            .icon-circle {{ width:72px; height:72px; border-radius:24px; display:flex; align-items:center; justify-content:center; font-size:36px; }}
            .card-label {{ font-size:15px; font-weight:800; margin-top:14px; color:var(--dark); }}

            #module-top {{ position:absolute; top:0; left:0; width:100%; z-index:2000; display:none; flex-direction:column; }}
            .led-header {{ background:#000; padding:12px 16px; border-bottom:3px solid var(--blue); }}
            .ticker-text {{ 
                color:#67e8f9; font-family:monospace; font-size:13.8px; font-weight:700;
                white-space:nowrap; overflow:hidden; animation: scroll 25s linear infinite;
            }}

            .nav-bar {{ background:var(--dark); padding:16px 20px; display:flex; align-items:center; position:relative; }}
            .back-btn {{ 
                position:absolute; left:16px; color:white; font-weight:700; cursor:pointer; 
                padding:9px 17px; background:#334155; border-radius:12px; font-size:14px;
            }}
            .nav-title {{ color:white; font-weight:800; font-size:16px; margin:0 auto; letter-spacing:0.5px; }}

            #module-bottom {{
                position:absolute; bottom:0; left:0; right:0; background:white;
                border-radius:32px 32px 0 0; box-shadow:0 -15px 60px rgba(0,0,0,0.2);
                z-index:2000; display:none; flex-direction:column; max-height:56%;
            }}
            .drawer-bar {{ width:46px; height:5.5px; background:#cbd5e1; border-radius:999px; margin:14px auto; }}
            #search-container {{ padding:14px 22px 10px; }}
            #search-input {{
                width:100%; padding:15px 18px; border-radius:14px; border:2px solid #e2e8f0;
                font-size:15.5px; font-weight:600; background:#f8fafc; outline:none;
            }}
            #search-input:focus {{ border-color:var(--blue); }}

            .drawer-content {{ padding:0 22px 24px; overflow-y:auto; flex:1; }}
            .data-row {{ 
                display:flex; justify-content:space-between; align-items:center; 
                padding:15px 0; border-bottom:1px solid #f1f5f9;
            }}
            .data-id {{ font-size:17px; font-weight:900; color:var(--dark); }}
            .data-dest {{ font-size:13px; color:#64748b; font-weight:600; }}
            .data-val {{ 
                font-size:14px; font-weight:900; padding:8px 16px; 
                border-radius:12px; background:#f1f5f9; min-width:68px; text-align:center;
            }}
            .loading {{ padding:40px 20px; text-align:center; color:#64748b; font-size:15px; }}

            @keyframes scroll {{ from {{ transform: translateX(120%); }} to {{ transform: translateX(-120%); }} }}
        </style>
    </head>
    <body>
    <div class="app-container">
        <div id="map-layer"></div>

        <!-- Ana Menü -->
        <div id="home-overlay">
            <div class="welcome">Merhaba <span>Mehmet Tahir</span>,</div>
            <div class="sub-welcome">{city_name} • {simdi}</div>
            <div class="menu-grid">
                <div class="card c-belediye" onclick="openModule('belediye')"><div class="icon-circle">🚌</div><div class="card-label">Belediye Otobüs</div></div>
                <div class="card c-metro" onclick="openModule('metro')"><div class="icon-circle">🚇</div><div class="card-label">Metro & Raylı</div></div>
                <div class="card c-ozel" onclick="openModule('ozel')"><div class="icon-circle">🚐</div><div class="card-label">Özel Sektör</div></div>
                <div class="card c-kart" onclick="openModule('kart')"><div class="icon-circle">💳</div><div class="card-label">Kart Dolum</div></div>
            </div>
        </div>

        <!-- Modül Üst Bar (LED her zaman aktif) -->
        <div id="module-top">
            <div class="led-header">
                <div class="ticker"><div class="ticker-text" id="led-text">BAĞLANIYOR...</div></div>
            </div>
            <div class="nav-bar">
                <div class="back-btn" onclick="goHome()">❮ GERİ</div>
                <div class="nav-title" id="nav-title"></div>
            </div>
        </div>

        <!-- Alt Çekmece -->
        <div id="module-bottom">
            <div class="drawer-bar"></div>
            <div id="search-container" style="display:none;">
                <input type="text" id="search-input" placeholder="🔍 Hat, durak veya istasyon ara...">
            </div>
            <div class="drawer-content" id="data-list"></div>
        </div>
    </div>

    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
        let map, moveInterval = null;
        let markers = [];
        const cityCenter = [{center_lat}, {center_lng}];
        const busColor = "{bus_color}";
        const cityName = "{city_name}";

        window.onload = () => {{
            map = L.map('map-layer', {{ zoomControl: false, attributionControl: false }}).setView(cityCenter, 13);
            L.tileLayer('https://{{s}}.basemaps.cartocdn.com/rastertiles/voyager/{{z}}/{{x}}/{{y}}{{r}}.png', {{ maxZoom: 19 }}).addTo(map);
        }};

        function goHome() {{
            document.getElementById('home-overlay').style.transform = 'translateY(0)';
            document.getElementById('module-top').style.display = 'none';
            document.getElementById('module-bottom').style.display = 'none';
            if (moveInterval) clearInterval(moveInterval);
            markers.forEach(m => map.removeLayer(m));
            markers = [];
        }}

        async function openModule(type) {{
            // Premium geçiş
            document.getElementById('home-overlay').style.transform = 'translateY(-100%)';
            document.getElementById('module-top').style.display = 'flex';
            document.getElementById('module-bottom').style.display = 'flex';

            const led = document.getElementById('led-text');
            const title = document.getElementById('nav-title');
            const list = document.getElementById('data-list');
            const search = document.getElementById('search-container');

            list.innerHTML = '<div class="loading">Veriler yükleniyor, lütfen bekleyin...</div>';
            search.style.display = type === 'belediye' ? 'block' : 'none';

            setTimeout(() => map.invalidateSize(), 450);

            if (type === 'belediye') {{
                title.innerText = ${{cityName}} BELEDİYE OTOBÜSLERİ;
                led.innerText = "{bus_led}";

                // Gerçek entegrasyon burada olacak (şu an premium demo)
                list.innerHTML = `
                    <div class="data-row"><div class="data-info"><span class="data-id">🚌 Hat 154</span><span class="data-dest">Balcalı Hastanesi</span><span class="data-dest" style="color:#ea580c;">Turgut Özal Blv.</span></div><div class="data-val">2 dk</div></div>
                    <div class="data-row"><div class="data-info"><span class="data-id">🚌 Hat 114</span><span class="data-dest">Merkez Otogar</span><span class="data-dest" style="color:#ea580c;">Baraj Yolu</span></div><div class="data-val">5 dk</div></div>
                    <div class="data-row"><div class="data-info"><span class="data-id">🚌 Hat 172</span><span class="data-dest">Çukurova Üni.</span><span class="data-dest" style="color:#ea580c;">İstasyon</span></div><div class="data-val">9 dk</div></div>
                `;

                // Canlı araç simülasyonu (çok akıcı)
                const icon = L.divIcon({{
                    html: <div style="background:${{busColor}}; width:28px; height:28px; border-radius:50%; border:3.5px solid #fff; color:white; font-size:14px; display:flex; align-items:center; justify-content:center; box-shadow:0 2px 8px rgba(0,0,0,0.3);">🚌</div>,
                    className: ''
                }});

                markers.forEach(m => map.removeLayer(m));
                markers = [];
                for (let i = 0; i < 6; i++) {{
                    const m = L.marker([cityCenter[0] + (Math.random()-0.5)*0.055, cityCenter[1] + (Math.random()-0.5)*0.055], {{icon}}).addTo(map);
                    markers.push(m);
                }}
                if (moveInterval) clearInterval(moveInterval);
                moveInterval = setInterval(() => {{
                    markers.forEach(m => {{
                        const p = m.getLatLng();
                        m.setLatLng([p.lat + (Math.random()-0.5)*0.0013, p.lng + (Math.random()-0.5)*0.0013]);
                    }});
                }}, 1300);

            }} else if (type === 'metro') {{
                title.innerText = ${{cityName}} METRO & RAYLI SİSTEM;
                led.innerText = "{metro_led}";

                list.innerHTML = `
                    <div class="data-row"><div class="data-info"><span class="data-id">M1</span><span class="data-dest">Hastane → Akıncılar</span></div><div class="data-val" style="background:#fce7f3;color:#db2777;">14:32</div></div>
                    <div class="data-row"><div class="data-info"><span class="data-id">M1</span><span class="data-dest">Vilayet → Hastane</span></div><div class="data-val" style="background:#fce7f3;color:#db2777;">14:41</div></div>
                `;
            }} else if (type === 'ozel') {{
                title.innerText = "ÖZEL HALK OTOBÜSLERİ & DOLMUŞ";
                led.innerText = "Özel sektör entegrasyonu devam ediyor...";
                list.innerHTML = '<div class="loading">Yakında bu bölümde de canlı takip aktif olacak.</div>';
            }} else if (type === 'kart') {{
                title.innerText = "KENTKART & DOLUM NOKTALARI";
                led.innerText = "💳 EN YAKIN DOLUM NOKTALARI HARİTADA";
                list.innerHTML = '<div class="loading">Kart dolum noktaları yakında eklenecek.</div>';
            }}
        }}

        // Arama (hızlı ve akıcı)
        document.getElementById('search-input').addEventListener('input', (e) => {{
            const term = e.target.value.toUpperCase();
            document.querySelectorAll('.data-row').forEach(row => {{
                row.style.display = row.textContent.toUpperCase().includes(term) ? 'flex' : 'none';
            }});
        }});
    </script>
    </body>
    </html>
    """
    return html
