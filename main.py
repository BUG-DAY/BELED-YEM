from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import datetime

app = FastAPI(title="Adana Ulaşım Matrisi")

@app.get("/", response_class=HTMLResponse)
async def read_root(sehir: str = "Adana"):
    simdi = datetime.datetime.now().strftime("%H:%M")
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Adana Ulaşım Matrisi</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <style>
            :root {{
                --blue: #2563eb;
                --pink: #db2777;
                --orange: #ea580c;
                --green: #10b981;
                --dark: #0f172a;
            }}
            * {{ 
                box-sizing: border-box; 
                font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; 
                margin: 0; padding: 0; 
                user-select: none; 
                -webkit-tap-highlight-color: transparent; 
            }}
            body {{ 
                background: #000; 
                height: 100vh; 
                display: flex; 
                align-items: center; 
                justify-content: center; 
                overflow: hidden; 
            }}

            .app-container {{
                width: 100vw; 
                height: 100vh; 
                max-width: 450px; 
                max-height: 850px;
                background: #f8fafc; 
                display: flex; 
                flex-direction: column;
                position: relative; 
                overflow: hidden;
                box-shadow: 0 0 30px rgba(0,0,0,0.3);
            }}
            @media (min-width: 460px) {{
                .app-container {{ 
                    border-radius: 40px; 
                    border: 12px solid #1e293b; 
                    height: 92vh; 
                }}
            }}

            #map-layer {{ 
                position: absolute; 
                top: 0; left: 0; 
                width: 100%; height: 100%; 
                z-index: 1; 
            }}

            /* Home Overlay */
            #home-overlay {{
                position: absolute; 
                top: 0; left: 0; 
                width: 100%; height: 100%;
                background: #f8fafc; 
                z-index: 3000; 
                display: flex; 
                flex-direction: column;
                padding: 30px 25px; 
                transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            }}
            .welcome {{ 
                font-size: 28px; 
                font-weight: 900; 
                color: var(--dark); 
                line-height: 1.1; 
            }}
            .welcome span {{ color: var(--blue); }}
            .sub-welcome {{ 
                font-size: 15.5px; 
                color: #64748b; 
                font-weight: 600; 
                margin-top: 8px; 
            }}

            .menu-grid {{
                display: grid; 
                grid-template-columns: 1fr 1fr; 
                gap: 16px;
                margin-top: 20px;
            }}
            .card {{
                background: white; 
                border-radius: 24px; 
                padding: 24px 12px; 
                text-align: center;
                box-shadow: 0 10px 25px rgba(0,0,0,0.06);
                cursor: pointer;
                display: flex; 
                flex-direction: column; 
                align-items: center; 
                gap: 14px; 
                transition: all 0.2s ease;
                border: 2px solid transparent;
            }}
            .card:active {{
                transform: scale(0.93);
                background: #f1f5f9;
            }}
            .icon-circle {{
                width: 68px; 
                height: 68px; 
                border-radius: 22px; 
                display: flex; 
                align-items: center; 
                justify-content: center; 
                font-size: 34px;
            }}
            .card-label {{ 
                font-size: 14.5px; 
                font-weight: 800; 
                color: var(--dark); 
            }}

            .c-belediye .icon-circle {{ background: #dbeafe; color: var(--blue); }}
            .c-metro .icon-circle {{ background: #fce7f3; color: var(--pink); }}
            .c-ozel .icon-circle {{ background: #ffedd5; color: var(--orange); }}
            .c-kart .icon-circle {{ background: #d1fae5; color: var(--green); }}

            /* Module Components */
            #module-top {{
                position: absolute; 
                top: 0; left: 0; 
                width: 100%; 
                z-index: 2000;
                display: none; 
                flex-direction: column;
            }}
            .led-header {{
                background: #000; 
                padding: 11px 15px; 
                border-bottom: 3px solid var(--blue);
            }}
            .ticker-text {{
                color: #38bdf8; 
                font-family: monospace; 
                font-size: 13.2px; 
                font-weight: bold;
                white-space: nowrap;
                overflow: hidden;
                animation: scroll 18s linear infinite;
            }}

            .nav-bar {{
                background: var(--dark); 
                padding: 15px 20px; 
                display: flex; 
                align-items: center; 
                position: relative;
            }}
            .back-btn {{
                position: absolute; 
                left: 15px; 
                color: white; 
                font-weight: 700; 
                cursor: pointer; 
                padding: 7px 14px; 
                background: #334155; 
                border-radius: 10px; 
                font-size: 13.5px;
            }}
            .nav-title {{
                color: white; 
                font-weight: 800; 
                font-size: 15.5px; 
                margin: 0 auto;
            }}

            #module-bottom {{
                position: absolute; 
                bottom: 0; left: 0; right: 0; 
                background: white;
                border-radius: 28px 28px 0 0; 
                box-shadow: 0 -12px 50px rgba(0,0,0,0.18);
                z-index: 2000; 
                display: none; 
                flex-direction: column; 
                max-height: 52%;
            }}
            .drawer-bar {{
                width: 42px; height: 5px; 
                background: #cbd5e1; 
                border-radius: 10px; 
                margin: 12px auto;
            }}
            #search-container {{ padding: 12px 20px 8px; }}
            #search-input {{
                width: 100%; 
                padding: 14px 16px; 
                border-radius: 12px; 
                border: 2px solid #e2e8f0; 
                font-size: 15px; 
                font-weight: 600; 
                background: #f8fafc;
                outline: none;
            }}
            #search-input:focus {{ border-color: var(--blue); }}

            .drawer-content {{ 
                padding: 0 20px 20px; 
                overflow-y: auto; 
                flex: 1;
            }}
            .data-row {{
                display: flex; 
                justify-content: space-between; 
                align-items: center; 
                padding: 14px 0; 
                border-bottom: 1px solid #f1f5f9;
            }}
            .data-id {{ 
                font-size: 16.5px; 
                font-weight: 900; 
                color: var(--dark); 
            }}
            .data-dest {{ 
                font-size: 12.5px; 
                color: #64748b; 
                font-weight: 600; 
            }}
            .data-val {{
                font-size: 13.5px; 
                font-weight: 900; 
                padding: 7px 14px; 
                border-radius: 10px; 
            }}

            @keyframes scroll {{ 
                from {{ transform: translateX(100%); }} 
                to {{ transform: translateX(-100%); }} 
            }}
        </style>
    </head>
    <body>
    <div class="app-container">
        <div id="map-layer"></div>

        <!-- Ana Menü -->
        <div id="home-overlay">
            <div class="home-header">
                <div class="welcome">Merhaba <span>Mehmet Tahir</span>,</div>
                <div class="sub-welcome">Bugün hangi aracı kullanacaksın? • {simdi}</div>
            </div>
            <div class="menu-grid">
                <div class="card c-belediye" onclick="openModule('belediye')">
                    <div class="icon-circle">🚌</div>
                    <div class="card-label">Belediye</div>
                </div>
                <div class="card c-metro" onclick="openModule('metro')">
                    <div class="icon-circle">🚇</div>
                    <div class="card-label">Metro</div>
                </div>
                <div class="card c-ozel" onclick="openModule('ozel')">
                    <div class="icon-circle">🚐</div>
                    <div class="card-label">Özel Sektör</div>
                </div>
                <div class="card c-kart" onclick="openModule('kart')">
                    <div class="icon-circle">💳</div>
                    <div class="card-label">Kart Dolum</div>
                </div>
            </div>
        </div>

        <!-- Modül Üst Bar -->
        <div id="module-top">
            <div class="led-header">
                <div class="ticker"><div class="ticker-text" id="led-text">YÜKLENİYOR...</div></div>
            </div>
            <div class="nav-bar">
                <div class="back-btn" onclick="goHome()">❮ GERİ</div>
                <div class="nav-title" id="nav-title">Ulaşım Bilgileri</div>
            </div>
        </div>

        <!-- Alt Çekmece -->
        <div id="module-bottom">
            <div class="drawer-bar"></div>
            <div id="search-container">
                <input type="text" id="search-input" placeholder="🔍 Hat veya Durak Ara (örn: 154)">
            </div>
            <div class="drawer-content" id="data-list"></div>
        </div>
    </div>

    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
        let map, moveInterval;
        let markers = [];
        const adanaCenter = [36.9914, 35.3308];

        window.onload = function() {{
            map = L.map('map-layer', {{ zoomControl: false, attributionControl: false }})
                   .setView(adanaCenter, 13);
            
            L.tileLayer('https://{{s}}.basemaps.cartocdn.com/rastertiles/voyager/{{z}}/{{x}}/{{y}}{{r}}.png', {{
                maxZoom: 19,
                className: 'map-tiles'
            }}).addTo(map);
        }};

        function goHome() {{
            document.getElementById('home-overlay').style.transform = 'translateY(0)';
            document.getElementById('module-top').style.display = 'none';
            document.getElementById('module-bottom').style.display = 'none';
            
            document.getElementById('search-input').value = "";
            
            if (moveInterval) clearInterval(moveInterval);
            markers.forEach(m => map.removeLayer(m));
            markers = [];
        }}

        function openModule(type) {{
            const home = document.getElementById('home-overlay');
            const topBar = document.getElementById('module-top');
            const bottom = document.getElementById('module-bottom');
            const led = document.getElementById('led-text');
            const title = document.getElementById('nav-title');
            const list = document.getElementById('data-list');
            const searchBox = document.getElementById('search-container');

            home.style.transform = 'translateY(-100%)';
            topBar.style.display = 'flex';
            bottom.style.display = 'flex';

            list.innerHTML = "";
            searchBox.style.display = 'none';

            setTimeout(() => map.invalidateSize(), 350);

            if (type === 'belediye') {{
                title.innerText = "BELEDİYE OTOBÜSLERİ";
                led.innerText = "📡 CANLI GPS TAKİBİ AKTİF • ADANA BÜYÜKŞEHİR BELEDİYESİ";
                searchBox.style.display = 'block';

                const hatlar = [
                    {{ id: "154", varis: "Balcalı Hastanesi", durak: "Turgut Özal Blv.", sure: "2 dk" }},
                    {{ id: "114", varis: "Merkez Otogar", durak: "Baraj Yolu", sure: "5 dk" }},
                    {{ id: "172", varis: "Çukurova Üni.", durak: "İstasyon", sure: "9 dk" }},
                    {{ id: "İTİMAT", varis: "Çarşı", durak: "Adliye Önü", sure: "DURAKTA" }}
                ];

                hatlar.forEach(h => {{
                    const row = document.createElement('div');
                    row.className = "data-row item-row";
                    row.innerHTML = `
                        <div class="data-info">
                            <span class="data-id">🚌 Hat ${h.id}</span>
                            <span class="data-dest">→ ${h.varis}</span>
                            <span class="data-dest" style="color:#ea580c;">📍 ${h.durak}</span>
                        </div>
                        <div class="data-val" style="background:#dbeafe;color:#1e40af;">${h.sure}</div>
                    `;
                    list.appendChild(row);
                }});

                // Canlı araç simülasyonu
                const busIcon = L.divIcon({{
                    html: <div style="background:#2563eb;width:26px;height:26px;border-radius:50%;border:3px solid #fff;display:flex;align-items:center;justify-content:center;color:white;font-size:13px;">🚌</div>,
                    className: ''
                }));

                markers = [];
                for (let i = 0; i < 5; i++) {{
                    const m = L.marker([
                        adanaCenter[0] + (Math.random() - 0.5) * 0.04,
                        adanaCenter[1] + (Math.random() - 0.5) * 0.04
                    ], {{ icon: busIcon }}).addTo(map);
                    markers.push(m);
                }}

                if (moveInterval) clearInterval(moveInterval);
                moveInterval = setInterval(() => {{
                    markers.forEach(m => {{
                        const pos = m.getLatLng();
                        m.setLatLng([
                            pos.lat + (Math.random() - 0.5) * 0.0012,
                            pos.lng + (Math.random() - 0.5) * 0.0012
                        ]);
                    }});
                }}, 1800);

            }} 
            else if (type === 'metro') {{
                title.innerText = "METRO & RAYLI SİSTEM";
                led.innerText = "🚇 METRO SEFERLERİ • DAKİK ÇALIŞIYOR";
                list.innerHTML = `
                    <div class="data-row">
                        <div class="data-info">
                            <span class="data-id">M1 - Hastane</span>
                            <span class="data-dest">Yön: Akıncılar</span>
                        </div>
                        <div class="data-val" style="color:#db2777;background:#fce7f3;">14:30</div>
                    </div>
                    <!-- diğer metro satırları eklenebilir -->
                `;
            }} 
            else if (type === 'ozel') {{
                title.innerText = "ÖZEL HALK OTOBÜSLERİ";
                led.innerText = "Özel sektör entegrasyonu devam ediyor...";
                list.innerHTML = `<div style="padding:30px 20px;text-align:center;color:#64748b;background:#f8fafc;border-radius:16px;margin:15px 0;">
                    <b>Özel Kooperatif GPS verileri</b><br>yakında bu uygulamada olacak.
                </div>`;
            }} 
            else if (type === 'kart') {{
                title.innerText = "KENTKART DOLUM";
                led.innerText = "💳 EN YAKIN DOLUM NOKTALARI";
                list.innerHTML = `<div class="data-row">
                    <div class="data-info">
                        <span class="data-id">Merkez Gişe</span>
                        <span class="data-dest">≈ 180 metre</span>
                    </div>
                    <div class="data-val" style="color:#10b981;background:#d1fae5;">AÇIK</div>
                </div>`;
            }}
        }}

        // Arama filtreleme
        document.getElementById('search-input').addEventListener('input', function(e) {{
            const term = e.target.value.toUpperCase().trim();
            document.querySelectorAll('.item-row').forEach(row => {{
                row.style.display = row.textContent.toUpperCase().includes(term) ? 'flex' : 'none';
            }});
        }});
    </script>
    </body>
    </html>
    """
    return html_content
