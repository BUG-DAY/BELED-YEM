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
        <title>Ulaşım Komuta Merkezi</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <style>
            :root {{ --blue: #2563eb; --pink: #db2777; --orange: #ea580c; --green: #10b981; --dark: #0f172a; }}
            * {{ box-sizing: border-box; font-family: 'Segoe UI', system-ui, sans-serif; margin: 0; padding: 0; }}
            body {{ background: #000; height: 100vh; display: flex; align-items: center; justify-content: center; overflow: hidden; }}

            /* ANA PANEL */
            .app-container {{
                width: 100vw; height: 100vh; max-width: 450px; max-height: 850px;
                background: #f8fafc; display: flex; flex-direction: column;
                position: relative; overflow: hidden;
            }}
            @media (min-width: 460px) {{ .app-container {{ border-radius: 35px; border: 8px solid #1e293b; height: 92vh; }} }}

            /* ÜST LED EKRAN */
            .led-header {{ background: #000; padding: 12px; border-bottom: 2px solid var(--blue); z-index: 2000; position: relative; }}
            .ticker {{ overflow: hidden; white-space: nowrap; }}
            .ticker-text {{
                display: inline-block; color: #38bdf8; font-family: monospace;
                font-size: 14px; font-weight: bold; animation: scroll 15s linear infinite;
            }}

            /* NAVİGASYON ÇUBUĞU */
            .nav-bar {{ background: var(--dark); padding: 15px; display: flex; align-items: center; justify-content: center; position: relative; }}
            .back-btn {{ position: absolute; left: 15px; color: white; font-weight: bold; cursor: pointer; padding: 5px 10px; display: none; background: #334155; border-radius: 8px; }}
            .nav-title {{ color: white; font-weight: 800; font-size: 14px; letter-spacing: 1px; }}

            /* EKRAN 1: ANA MENÜ */
            #home-screen {{ flex: 1; padding: 25px; display: flex; flex-direction: column; gap: 20px; z-index: 100; background: #f8fafc; }}
            .welcome {{ font-size: 22px; font-weight: 900; color: var(--dark); margin-bottom: 5px; }}
            .menu-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }}
            
            .card {{
                background: white; border-radius: 24px; padding: 25px 10px; text-align: center;
                box-shadow: 0 10px 25px rgba(0,0,0,0.05); cursor: pointer;
                display: flex; flex-direction: column; align-items: center; gap: 12px;
                border: 2px solid transparent; transition: 0.2s;
            }}
            .card:active {{ transform: scale(0.95); background: #f1f5f9; }}
            .icon-circle {{ width: 60px; height: 60px; border-radius: 20px; display: flex; align-items: center; justify-content: center; font-size: 30px; }}
            .card-label {{ font-size: 13px; font-weight: 800; color: var(--dark); }}

            .c-belediye .icon-circle {{ background: #dbeafe; color: var(--blue); }}
            .c-metro .icon-circle {{ background: #fce7f3; color: var(--pink); }}
            .c-ozel .icon-circle {{ background: #ffedd5; color: var(--orange); }}
            .c-kart .icon-circle {{ background: #d1fae5; color: var(--green); }}

            /* EKRAN 2: HARİTA VE DETAY */
            #map-screen {{ flex: 1; display: none; flex-direction: column; position: relative; }}
            .map-box {{ flex: 1; width: 100%; position: relative; }}
            #map {{ position: absolute; top: 0; bottom: 0; left: 0; right: 0; z-index: 1; }}

            /* ALT BİLGİ ÇEKMECESİ */
            .drawer {{
                position: absolute; bottom: 0; left: 0; right: 0; background: white;
                border-radius: 30px 30px 0 0; box-shadow: 0 -10px 40px rgba(0,0,0,0.1);
                z-index: 1000; display: flex; flex-direction: column; max-height: 40%;
            }}
            .drawer-bar {{ width: 40px; height: 5px; background: #e2e8f0; border-radius: 10px; margin: 12px auto; }}
            .drawer-content {{ padding: 0 25px 20px; overflow-y: auto; }}
            
            .data-row {{ display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid #f1f5f9; }}
            .data-info {{ display: flex; flex-direction: column; }}
            .data-id {{ font-size: 15px; font-weight: 800; color: var(--dark); }}
            .data-sub {{ font-size: 11px; color: #64748b; font-weight: 600; }}
            .data-val {{ font-size: 12px; font-weight: 800; background: #f1f5f9; padding: 5px 10px; border-radius: 8px; color: var(--blue); }}

            /* SAAT */
            .footer-clock {{ background: white; padding: 15px; text-align: center; border-top: 1px solid #eee; }}
            .time-text {{ font-size: 22px; font-weight: 900; color: var(--dark); }}

            @keyframes scroll {{ from {{ transform: translateX(100%); }} to {{ transform: translateX(-100%); }} }}
        </style>
    </head>
    <body>

    <div class="app-container">
        <div class="led-header">
            <div class="ticker"><div class="ticker-text" id="led-content">T.C. ULAŞIM MATRİSİ | SİSTEM AKTİF | MEHMET TAHİR KOMUTASINDA...</div></div>
        </div>

        <div class="nav-bar">
            <div id="back-btn" class="back-btn" onclick="showHome()">❮ GERİ</div>
            <div class="nav-title" id="nav-title">KOMUTA MERKEZİ</div>
        </div>

        <div id="home-screen">
            <div class="welcome">Hoş geldin, <br><span style="color:var(--blue);">Mehmet Tahir</span></div>
            <div class="menu-grid">
                <div class="card c-belediye" onclick="openModule('belediye')">
                    <div class="icon-circle">🚌</div><div class="card-label">Belediye</div>
                </div>
                <div class="card c-metro" onclick="openModule('metro')">
                    <div class="icon-circle">🚇</div><div class="card-label">Metro</div>
                </div>
                <div class="card c-ozel" onclick="openModule('ozel')">
                    <div class="icon-circle">🚐</div><div class="card-label">Özel Sektör</div>
                </div>
                <div class="card c-kart" onclick="openModule('kart')">
                    <div class="icon-circle">💳</div><div class="card-label">Kart Dolum</div>
                </div>
            </div>
        </div>

        <div id="map-screen">
            <div class="map-box"><div id="map"></div></div>
            <div class="drawer">
                <div class="drawer-bar"></div>
                <div class="drawer-content" id="drawer-data"></div>
            </div>
        </div>

        <div class="footer-clock">
            <div class="time-text" id="clock">{simdi}</div>
        </div>
    </div>

    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
        let map;
        let markers = [];
        let simInterval;
        const adana = [36.9914, 35.3308];

        // 1. ANA MENÜYE DÖN
        function showHome() {{
            document.getElementById('map-screen').style.display = 'none';
            document.getElementById('back-btn').style.display = 'none';
            document.getElementById('home-screen').style.display = 'flex';
            document.getElementById('nav-title').innerText = "KOMUTA MERKEZİ";
            document.getElementById('led-content').innerText = "T.C. ULAŞIM MATRİSİ | SİSTEM AKTİF | MEHMET TAHİR KOMUTASINDA...";
            
            if(simInterval) clearInterval(simInterval);
            if(map) {{ map.remove(); map = null; }} // Haritayı tamamen yokediyoruz ki çakışmasın
        }}

        // 2. MODÜLÜ AÇ (BELEDİYE, METRO VB.)
        function openModule(type) {{
            document.getElementById('home-screen').style.display = 'none';
            document.getElementById('map-screen').style.display = 'flex';
            document.getElementById('back-btn').style.display = 'block';

            // Haritayı her seferinde taptaze başlatıyoruz (Beyaz ekranın kesin çözümü)
            if(!map) {{
                map = L.map('map', {{ zoomControl: false }}).setView(adana, 13);
                L.tileLayer('https://{{s}}.basemaps.cartocdn.com/rastertiles/voyager/{{z}}/{{x}}/{{y}}{{r}}.png').addTo(map);
            }}
            setTimeout(() => {{ map.invalidateSize(); }}, 300);

            renderModule(type);
        }}

        // 3. VERİLERİ VE HARİTAYI DOLDUR
        function renderModule(type) {{
            const dataBox = document.getElementById('drawer-data');
            const led = document.getElementById('led-content');
            dataBox.innerHTML = "";
            markers = [];

            if(type === 'belediye') {{
                led.innerText = "📡 CANLI TAKİP: BELEDİYE OTOBÜSLERİ YOLDA... 154 HATTI YAKLAŞIYOR...";
                document.getElementById('nav-title').innerText = "BELEDİYE HATLAR";
                const hatlar = [{{id:"154", r:"Barajyolu", s:"2 Dk"}}, {{id:"114", r:"Özal", s:"5 Dk"}}, {{id:"İTİMAT", r:"Çarşı", s:"DURAKTA"}}];
                hatlar.forEach(h => {{
                    dataBox.innerHTML += <div class="data-row"><div class="data-info"><span class="data-id">${{h.id}}</span><span class="data-sub">${{h.r}}</span></div><div class="data-val">${{h.s}}</div></div>;
                }});
                
                const icon = L.divIcon({{ html: <div style="background:#2563eb; width:22px; height:22px; border-radius:50%; border:2px solid #fff; display:flex; align-items:center; justify-content:center; color:white; font-size:10px;">🚌</div>, className: 'm' }});
                for(let i=0; i<3; i++) {{
                    let m = L.marker([adana[0]+(Math.random()-0.5)*0.02, adana[1]+(Math.random()-0.5)*0.02], {{icon:icon}}).addTo(map);
                    markers.push(m);
                }}
                simInterval = setInterval(() => {{
                    markers.forEach(m => {{ let c = m.getLatLng(); m.setLatLng([c.lat+(Math.random()-0.5)*0.001, c.lng+(Math.random()-0.5)*0.001]); }});
                }}, 2000);

            }} else if(type === 'metro') {{
                led.innerText = "🚇 RAYLI SİSTEM: SEFERLER DAKİK İŞLİYOR... BİR SONRAKİ METRO 4 DK SONRA...";
                document.getElementById('nav-title').innerText = "METRO SAATLERİ";
                dataBox.innerHTML = `
                    <div class="data-row"><div class="data-info"><span class="data-id">Hastane İstasyonu</span><span class="data-sub">Kalkış Yönü: Akıncılar</span></div><div class="data-val" style="color:#db2777">14:30</div></div>
                    <div class="data-row"><div class="data-info"><span class="data-id">Vilayet İstasyonu</span><span class="data-sub">Kalkış Yönü: Hastane</span></div><div class="data-val" style="color:#db2777">14:38</div></div>`;
            }} else if(type === 'ozel') {{
                led.innerText = "🚐 ÖZEL SEKTÖR: KOOPERATİF VERİ BAĞLANTISI BEKLENİYOR...";
                dataBox.innerHTML = <div style="padding:20px; text-align:center; color:#64748b; font-size:13px; border:2px dashed #eee; border-radius:15px;">Özel Sektör (ÖHO) API entegrasyonu aşamasındadır. Altyapı %100 hazırdır.</div>;
            }} else if(type === 'kart') {{
                led.innerText = "💳 KENTKART: SİZE EN YAKIN DOLUM NOKTALARI HARİTADA İŞARETLENDİ...";
                dataBox.innerHTML = <div class="data-row"><div class="data-info"><span class="data-id">Merkez Gişe</span><span class="data-sub">200m mesafede</span></div></div>;
            }}
        }}

        // Saat
        setInterval(() => {{ document.getElementById('clock').textContent = new Date().toLocaleTimeString('tr-TR', {{hour:'2-digit', minute:'2-digit'}}); }}, 1000);
    </script>
    </body>
    </html>
    """
