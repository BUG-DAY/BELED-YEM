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
        <title>Ulaşım Matrisi | {sehir}</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <style>
            * {{ box-sizing: border-box; font-family: 'Inter', system-ui, -apple-system, sans-serif; margin: 0; padding: 0; }}
            body {{ background: #0f172a; height: 100vh; display: flex; align-items: center; justify-content: center; overflow: hidden; }}

            /* ANA CİHAZ ÇERÇEVESİ */
            .app-wrapper {{
                width: 100vw; height: 100vh; max-width: 430px; max-height: 880px;
                background: #f8fafc; display: flex; flex-direction: column;
                position: relative; overflow: hidden; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            }}
            @media (min-width: 450px) {{ .app-wrapper {{ border-radius: 40px; border: 10px solid #1e293b; height: 92vh; }} }}

            /* ÜST PANEL */
            .nav-header {{ background: #0f172a; padding: 20px 15px; text-align: center; position: relative; z-index: 2000; }}
            .back-btn {{ 
                position: absolute; left: 20px; top: 50%; transform: translateY(-50%); 
                color: white; font-size: 24px; cursor: pointer; display: none; padding: 10px;
            }}
            .main-title {{ color: white; font-weight: 800; font-size: 16px; letter-spacing: 1px; }}
            .sub-status {{ color: #38bdf8; font-size: 11px; font-weight: 700; margin-top: 4px; text-transform: uppercase; }}

            /* --- EKRAN 1: ANA MENÜ --- */
            #home-screen {{ flex: 1; padding: 25px; display: flex; flex-direction: column; gap: 20px; background: #f8fafc; z-index: 10; }}
            .welcome-msg {{ font-size: 20px; font-weight: 800; color: #1e293b; margin-bottom: 5px; }}
            .grid-container {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }}
            
            .card {{
                background: white; border-radius: 24px; padding: 25px 15px; text-align: center;
                box-shadow: 0 4px 15px rgba(0,0,0,0.05); cursor: pointer;
                display: flex; flex-direction: column; align-items: center; gap: 12px;
                border: 2px solid transparent; transition: all 0.2s ease;
            }}
            .card:active {{ transform: scale(0.95); background: #f1f5f9; }}
            
            .icon-circle {{ width: 64px; height: 64px; border-radius: 20px; display: flex; align-items: center; justify-content: center; font-size: 32px; }}
            .card-name {{ font-size: 14px; font-weight: 800; color: #1e293b; }}

            /* Renk Temaları */
            .c-bus .icon-circle {{ background: #dbeafe; color: #2563eb; }}
            .c-metro .icon-circle {{ background: #fce7f3; color: #db2777; }}
            .c-spec .icon-circle {{ background: #ffedd5; color: #ea580c; }}
            .c-card .icon-circle {{ background: #d1fae5; color: #059669; }}

            /* --- EKRAN 2: HARİTA MODU --- */
            #map-screen {{ flex: 1; display: none; flex-direction: column; position: relative; }}
            .map-box {{ flex: 1; width: 100%; position: relative; }}
            #map {{ position: absolute; top: 0; bottom: 0; left: 0; right: 0; z-index: 1; }}

            /* ALT BİLGİ ÇEKMECESİ (MODERN MOOVIT TARZI) */
            .bottom-drawer {{
                position: absolute; bottom: 0; left: 0; right: 0; background: white;
                border-radius: 30px 30px 0 0; box-shadow: 0 -10px 40px rgba(0,0,0,0.1);
                z-index: 1000; display: flex; flex-direction: column; max-height: 40%;
                border-top: 1px solid #e2e8f0;
            }}
            .drawer-knob {{ width: 40px; height: 5px; background: #e2e8f0; border-radius: 10px; margin: 12px auto; }}
            .drawer-title {{ padding: 0 25px 15px; font-weight: 800; color: #0f172a; font-size: 16px; }}
            .drawer-list {{ padding: 0 25px 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 12px; }}

            .row-item {{ display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid #f1f5f9; }}
            .row-main {{ display: flex; flex-direction: column; }}
            .row-id {{ font-size: 15px; font-weight: 800; color: #1e293b; }}
            .row-sub {{ font-size: 11px; color: #64748b; font-weight: 600; }}
            .row-badge {{ font-size: 12px; font-weight: 800; padding: 6px 12px; border-radius: 10px; }}

            /* SAAT KUTUSU */
            .time-dock {{ padding: 15px 25px; background: white; border-top: 1px solid #f1f5f9; text-align: center; }}
            .digital-clock {{ font-size: 24px; font-weight: 900; color: #0f172a; }}
        </style>
    </head>
    <body>

    <div class="app-wrapper">
        <div class="nav-header">
            <div id="btn-back" class="back-btn" onclick="showHome()">❮</div>
            <div class="main-title">ULAŞIM KOMUTA MERKEZİ</div>
            <div id="status-text" class="sub-status">MEHMET TAHİR | SİSTEM AKTİF</div>
        </div>

        <div id="home-screen">
            <div class="welcome-msg">Merhaba Mehmet Tahir, <br><span style="color:#64748b; font-size:14px; font-weight:600;">Nereye gitmek istersin?</span></div>
            
            <div class="grid-container">
                <div class="card c-bus" onclick="showMap('belediye')">
                    <div class="icon-circle">🚌</div>
                    <div class="card-name">Belediye</div>
                </div>
                <div class="card c-metro" onclick="showMap('metro')">
                    <div class="icon-circle">🚇</div>
                    <div class="card-name">Metro</div>
                </div>
                <div class="card c-spec" onclick="showMap('ozel')">
                    <div class="icon-circle">🚐</div>
                    <div class="card-name">Özel Sektör</div>
                </div>
                <div class="card c-card" onclick="showMap('kart')">
                    <div class="icon-circle">💳</div>
                    <div class="card-name">Kart Dolum</div>
                </div>
            </div>
        </div>

        <div id="map-screen">
            <div class="map-box">
                <div id="map"></div>
            </div>
            
            <div class="bottom-drawer">
                <div class="drawer-knob"></div>
                <div class="drawer-title" id="drawer-label">Canlı Takip</div>
                <div class="drawer-list" id="drawer-content">
                    </div>
            </div>
        </div>

        <div class="time-dock">
            <div class="digital-clock" id="clock">{simdi}</div>
        </div>
    </div>

    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
        let map;
        let busMarkers = [];
        let simInterval;
        const adanaPos = [36.9914, 35.3308];

        // 1. HARİTAYI BAŞLATMA
        function initMap() {{
            if (!map) {{
                map = L.map('map', {{ zoomControl: false }}).setView(adanaPos, 13);
                L.tileLayer('https://{{s}}.basemaps.cartocdn.com/rastertiles/voyager/{{z}}/{{x}}/{{y}}{{r}}.png').addTo(map);
            }}
        }}

        // 2. ANA MENÜYE DÖNÜŞ
        function showHome() {{
            document.getElementById('map-screen').style.display = 'none';
            document.getElementById('btn-back').style.display = 'none';
            document.getElementById('home-screen').style.display = 'flex';
            document.getElementById('status-text').innerText = "MEHMET TAHİR | SİSTEM AKTİF";
            
            if(simInterval) clearInterval(simInterval);
            busMarkers.forEach(m => map.removeLayer(m));
            busMarkers = [];
        }}

        // 3. HARİTAYI AÇMA VE VERİ YÜKLEME
        function showMap(type) {{
            document.getElementById('home-screen').style.display = 'none';
            document.getElementById('map-screen').style.display = 'flex';
            document.getElementById('btn-back').style.display = 'block';
            
            initMap();
            // Harita boyutunu düzeltme (Kritik kod!)
            setTimeout(() => {{ map.invalidateSize(); }}, 200);

            const content = document.getElementById('drawer-content');
            const label = document.getElementById('drawer-label');
            content.innerHTML = ""; // Temizle

            if(type === 'belediye') {{
                label.innerText = "Canlı Otobüs Takibi";
                document.getElementById('status-text').innerText = "📍 BELEDİYE HATLAR";
                
                const hatlar = [
                    {{id: "154", r: "Barajyolu - Balcalı", s: "2 Dk"}},
                    {{id: "114", r: "Çukurova - Merkez", s: "5 Dk"}},
                    {{id: "İTİMAT", r: "Vilayet - Meydan", s: "1 Dk"}}
                ];
                
                hatlar.forEach(h => {{
                    content.innerHTML += `
                        <div class="row-item">
                            <div class="row-main"><span class="row-id">${{h.id}}</span><span class="row-sub">${{h.r}}</span></div>
                            <div class="row-badge" style="background:#dbeafe; color:#2563eb;">${{h.s}}</div>
                        </div>`;
                }});

                // Simülasyon
                const icon = L.divIcon({{ html: <div style="background:#2563eb; width:22px; height:22px; border-radius:50%; border:2px solid #fff; display:flex; align-items:center; justify-content:center; color:white; font-size:10px;">🚌</div>, className: 'm' }});
                for(let i=0; i<3; i++) {{
                    let m = L.marker([adanaPos[0]+(Math.random()-0.5)*0.02, adanaPos[1]+(Math.random()-0.5)*0.02], {{icon:icon}}).addTo(map);
                    busMarkers.push(m);
                }}
                simInterval = setInterval(() => {{
                    busMarkers.forEach(m => {{ let c = m.getLatLng(); m.setLatLng([c.lat+(Math.random()-0.5)*0.001, c.lng+(Math.random()-0.5)*0.001]); }});
                }}, 2000);

            }} else if(type === 'metro') {{
                label.innerText = "Metro Sefer Saatleri";
                document.getElementById('status-text').innerText = "📍 METRO İSTASYONLARI";
                content.innerHTML = `
                    <div class="row-item"><div class="row-main"><span class="row-id">🚇 Hastane</span><span class="row-sub">Sonraki Kalkış</span></div><div class="row-badge" style="background:#fce7f3; color:#db2777;">14:15</div></div>
                    <div class="row-item"><div class="row-main"><span class="row-id">🚇 Vilayet</span><span class="row-sub">Sonraki Kalkış</span></div><div class="row-badge" style="background:#fce7f3; color:#db2777;">14:22</div></div>
                `;
            }} else if(type === 'ozel') {{
                label.innerText = "Özel Sektör Verisi";
                document.getElementById('status-text').innerText = "📍 ENTEGRASYON MODU";
                content.innerHTML = <div style="text-align:center; padding:20px; color:#64748b; font-size:13px; border:2px dashed #e2e8f0; border-radius:15px;">Özel Kooperatif API bağlantısı bekleniyor. <br>Altyapı %100 hazırdır.</div>;
            }} else if(type === 'kart') {{
                label.innerText = "Dolum Noktaları";
                document.getElementById('status-text').innerText = "📍 YAKIN DOLUM NOKTALARI";
                content.innerHTML = <div class="row-item"><div class="row-main"><span class="row-id">📍 Merkez Gişe</span><span class="row-sub">150m Yakınında</span></div></div>;
            }}
        }}

        // Saat
        setInterval(() => {{ document.getElementById('clock').textContent = new Date().toLocaleTimeString('tr-TR', {{hour:'2-digit', minute:'2-digit'}}); }}, 1000);
    </script>
    </body>
    </html>
    """
