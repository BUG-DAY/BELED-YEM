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
        <title>Ulaşım Matrisi</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <style>
            :root {{ --blue: #2563eb; --pink: #db2777; --orange: #ea580c; --green: #10b981; --dark: #0f172a; }}
            * {{ box-sizing: border-box; font-family: 'Segoe UI', system-ui, sans-serif; margin: 0; padding: 0; user-select: none; -webkit-tap-highlight-color: transparent; }}
            body {{ background: #000; height: 100vh; display: flex; align-items: center; justify-content: center; overflow: hidden; }}

            /* ANA TELEFON ÇERÇEVESİ */
            .app-container {{
                width: 100vw; height: 100vh; max-width: 450px; max-height: 850px;
                background: #f8fafc; display: flex; flex-direction: column;
                position: relative; overflow: hidden;
            }}
            @media (min-width: 460px) {{ .app-container {{ border-radius: 35px; border: 8px solid #1e293b; height: 92vh; }} }}

            /* HARİTA (HER ZAMAN EN ARKADA ÇALIŞIR, BÖYLECE ASLA DONMAZ) */
            #map-layer {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; }}

            /* ---------------------------------------------------- */
            /* 1. ANA MENÜ (ÖN PERDE) */
            #home-overlay {{
                position: absolute; top: 0; left: 0; width: 100%; height: 100%;
                background: #f8fafc; z-index: 3000; display: flex; flex-direction: column;
                padding: 30px 25px; transition: transform 0.3s ease-in-out;
            }}
            .home-header {{ margin-bottom: 30px; margin-top: 20px; }}
            .welcome {{ font-size: 26px; font-weight: 900; color: var(--dark); line-height: 1.2; }}
            .welcome span {{ color: var(--blue); }}
            .sub-welcome {{ font-size: 15px; color: #64748b; font-weight: 600; margin-top: 5px; }}

            .menu-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }}
            .card {{
                background: white; border-radius: 24px; padding: 25px 10px; text-align: center;
                box-shadow: 0 8px 20px rgba(0,0,0,0.05); cursor: pointer;
                display: flex; flex-direction: column; align-items: center; gap: 12px; border: 2px solid transparent;
            }}
            .card:active {{ transform: scale(0.95); background: #f1f5f9; }}
            .icon-circle {{ width: 64px; height: 64px; border-radius: 20px; display: flex; align-items: center; justify-content: center; font-size: 32px; }}
            .card-label {{ font-size: 14px; font-weight: 800; color: var(--dark); }}

            .c-belediye .icon-circle {{ background: #dbeafe; color: var(--blue); }}
            .c-metro .icon-circle {{ background: #fce7f3; color: var(--pink); }}
            .c-ozel .icon-circle {{ background: #ffedd5; color: var(--orange); }}
            .c-kart .icon-circle {{ background: #d1fae5; color: var(--green); }}

            /* ---------------------------------------------------- */
            /* 2. MODÜL EKRANI BİLEŞENLERİ (HARİTA ÜSTÜ) */
            
            /* Üst Bar ve LED (Sadece modüllerde görünür) */
            #module-top {{
                position: absolute; top: 0; left: 0; width: 100%; z-index: 2000;
                display: none; flex-direction: column;
            }}
            .led-header {{ background: #000; padding: 10px; border-bottom: 2px solid var(--blue); }}
            .ticker {{ overflow: hidden; white-space: nowrap; }}
            .ticker-text {{ display: inline-block; color: #38bdf8; font-family: monospace; font-size: 13px; font-weight: bold; animation: scroll 15s linear infinite; }}
            
            .nav-bar {{ background: var(--dark); padding: 15px; display: flex; align-items: center; justify-content: center; position: relative; }}
            .back-btn {{ position: absolute; left: 15px; color: white; font-weight: bold; cursor: pointer; padding: 6px 12px; background: #334155; border-radius: 8px; font-size: 13px; }}
            .nav-title {{ color: white; font-weight: 800; font-size: 15px; letter-spacing: 1px; }}

            /* Alt Bilgi Çekmecesi */
            #module-bottom {{
                position: absolute; bottom: 0; left: 0; right: 0; background: white;
                border-radius: 25px 25px 0 0; box-shadow: 0 -10px 40px rgba(0,0,0,0.15);
                z-index: 2000; display: none; flex-direction: column; max-height: 50%;
            }}
            .drawer-bar {{ width: 40px; height: 5px; background: #cbd5e1; border-radius: 10px; margin: 12px auto; }}
            
            /* Arama Kutusu (Sadece Otobüste Çıkar) */
            #search-container {{ padding: 0 20px 10px; display: none; }}
            #search-input {{ width: 100%; padding: 10px 15px; border-radius: 10px; border: 2px solid #e2e8f0; font-size: 14px; font-weight: bold; outline: none; background: #f8fafc; color: var(--dark); }}
            #search-input:focus {{ border-color: var(--blue); }}

            .drawer-content {{ padding: 0 20px 20px; overflow-y: auto; flex: 1; }}
            
            /* Liste Elemanları (Otobüs / Metro Verileri) */
            .data-row {{ display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid #f1f5f9; }}
            .data-info {{ display: flex; flex-direction: column; gap: 4px; }}
            .data-id {{ font-size: 16px; font-weight: 900; color: var(--dark); }}
            .data-dest {{ font-size: 11px; color: #64748b; font-weight: 600; display: flex; gap: 5px; align-items: center; }}
            .data-val {{ font-size: 13px; font-weight: 900; background: #f1f5f9; padding: 6px 12px; border-radius: 10px; color: var(--blue); }}

            @keyframes scroll {{ from {{ transform: translateX(100%); }} to {{ transform: translateX(-100%); }} }}
        </style>
    </head>
    <body>

    <div class="app-container">
        
        <div id="map-layer"></div>

        <div id="home-overlay">
            <div class="home-header">
                <div class="welcome">Merhaba <span>Mehmet Tahir</span>,</div>
                <div class="sub-welcome">Bugün hangi aracı kullanacaksın?</div>
            </div>
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

        <div id="module-top">
            <div class="led-header">
                <div class="ticker"><div class="ticker-text" id="led-text">YÜKLENİYOR...</div></div>
            </div>
            <div class="nav-bar">
                <div class="back-btn" onclick="goHome()">❮ GERİ</div>
                <div class="nav-title" id="nav-title">BİLGİ EKRANI</div>
            </div>
        </div>

        <div id="module-bottom">
            <div class="drawer-bar"></div>
            <div id="search-container">
                <input type="text" id="search-input" placeholder="🔍 Hat veya Durak Ara (Örn: 154)">
            </div>
            <div class="drawer-content" id="data-list"></div>
        </div>

    </div>

    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
        let map;
        let markers = [];
        let moveInterval;
        const adanaCenter = [36.9914, 35.3308];

        // SİSTEM BAŞLADIĞINDA HARİTAYI GİZLİCE ARKADA KUR
        window.onload = function() {{
            map = L.map('map-layer', {{ zoomControl: false }}).setView(adanaCenter, 13);
            L.tileLayer('https://{{s}}.basemaps.cartocdn.com/rastertiles/voyager/{{z}}/{{x}}/{{y}}{{r}}.png', {{ maxZoom: 19 }}).addTo(map);
        }};

        // ANA MENÜYE DÖN (Perdeyi İndir)
        function goHome() {{
            // Perdeyi tekrar göster
            document.getElementById('home-overlay').style.transform = 'translateY(0)';
            
            // Modül parçalarını gizle
            document.getElementById('module-top').style.display = 'none';
            document.getElementById('module-bottom').style.display = 'none';
            
            // Arama kutusunu temizle
            document.getElementById('search-input').value = "";
            
            // Harita üzerindeki araçları temizle (arkaplanda rami yormasın)
            if(moveInterval) clearInterval(moveInterval);
            markers.forEach(m => map.removeLayer(m));
            markers = [];
        }}

        // KATEGORİYE GİR (Perdeyi Kaldır ve Verileri Yükle)
        function openModule(type) {{
            // 1. Ana menü perdesini yukarı kaydır (Çok havalı ve hızlı bir geçiş)
            document.getElementById('home-overlay').style.transform = 'translateY(-100%)';
            
            // 2. Modül parçalarını görünür yap
            document.getElementById('module-top').style.display = 'flex';
            document.getElementById('module-bottom').style.display = 'flex';
            
            // Harita boyutunu garantiye al
            setTimeout(() => {{ map.invalidateSize(); }}, 300);

            // 3. Verileri doldur
            const led = document.getElementById('led-text');
            const nav = document.getElementById('nav-title');
            const list = document.getElementById('data-list');
            const searchBox = document.getElementById('search-container');

            list.innerHTML = ""; // Listeyi temizle

            if(type === 'belediye') {{
                nav.innerText = "BELEDİYE OTOBÜSLERİ";
                led.innerText = "📡 CANLI GPS TAKİBİ AKTİF | ADANA BÜYÜKŞEHİR BELEDİYESİ HAT BİLGİLERİ...";
                searchBox.style.display = 'block'; // Arama kutusunu aç!

                const hatlar = [
                    {{ id:"154", varis:"Balcalı Hastanesi", durak:"📍 Şu an: Turgut Özal Blv.", sure:"2 Dk" }},
                    {{ id:"114", varis:"Merkez Otogar", durak:"📍 Şu an: Baraj Yolu", sure:"5 Dk" }},
                    {{ id:"172", varis:"Çukurova Üniversitesi", durak:"📍 Şu an: İstasyon", sure:"9 Dk" }},
                    {{ id:"İTİMAT", varis:"Çarşı", durak:"📍 Şu an: Adliye Önü", sure:"DURAKTA" }}
                ];

                hatlar.forEach(h => {{
                    list.innerHTML += `
                        <div class="data-row item-row">
                            <div class="data-info">
                                <span class="data-id">🚌 Hat ${{h.id}}</span>
                                <span class="data-dest">Hedef: ${{h.varis}}</span>
                                <span class="data-dest" style="color:#ea580c;">${{h.durak}}</span>
                            </div>
                            <div class="data-val">${{h.sure}}</div>
                        </div>`;
                }});

                // Haritaya Canlı Mavi Otobüsler
                const icon = L.divIcon({{ html: <div style="background:#2563eb; width:24px; height:24px; border-radius:50%; border:2px solid #fff; display:flex; align-items:center; justify-content:center; color:white; font-size:11px;">🚌</div>, className: 'm' }});
                for(let i=0; i<4; i++) {{
                    let m = L.marker([adanaCenter[0]+(Math.random()-0.5)*0.03, adanaCenter[1]+(Math.random()-0.5)*0.03], {{icon:icon}}).addTo(map);
                    markers.push(m);
                }}
                moveInterval = setInterval(() => {{
                    markers.forEach(m => {{ let c = m.getLatLng(); m.setLatLng([c.lat+(Math.random()-0.5)*0.001, c.lng+(Math.random()-0.5)*0.001]); }});
                }}, 1500);

            }} 
            else if(type === 'metro') {{
                nav.innerText = "METRO VE RAYLI SİSTEM";
                led.innerText = "🚇 METRO SEFERLERİ DAKİK İŞLİYOR | BİR SONRAKİ TREN YAKLAŞIYOR...";
                searchBox.style.display = 'none'; // Arama kutusunu kapat
                
                list.innerHTML = `
                    <div class="data-row"><div class="data-info"><span class="data-id">M1 - Hastane İstasyonu</span><span class="data-dest">Yön: Akıncılar</span></div><div class="data-val" style="color:#db2777; background:#fce7f3;">14:30</div></div>
                    <div class="data-row"><div class="data-info"><span class="data-id">M1 - Vilayet İstasyonu</span><span class="data-dest">Yön: Hastane</span></div><div class="data-val" style="color:#db2777; background:#fce7f3;">14:38</div></div>`;
            }} 
            else if(type === 'ozel') {{
                nav.innerText = "ÖZEL SEKTÖR OTOBÜSLERİ";
                led.innerText = "⚠️ ÖZEL HALK OTOBÜSÜ VE DOLMUŞ AĞI ENTEGRASYONU BEKLENİYOR...";
                searchBox.style.display = 'none';
                list.innerHTML = <div style="padding:20px; text-align:center; color:#64748b; font-size:13px; border:2px dashed #cbd5e1; border-radius:12px; margin-top:10px;"><b>Altyapı Hazır!</b><br>Özel Kooperatiflerin GPS verilerini açık sisteme entegre etmesi bekleniyor.</div>;
            }}
            else if(type === 'kart') {{
                nav.innerText = "KART DOLUM NOKTALARI";
                led.innerText = "💳 KENTKART DOLUM NOKTALARI HARİTADA GÖSTERİLİYOR...";
                searchBox.style.display = 'none';
                list.innerHTML = <div class="data-row"><div class="data-info"><span class="data-id">📍 Merkez Gişe</span><span class="data-dest">200m Mesafede</span></div><div class="data-val" style="color:#10b981; background:#d1fae5;">AÇIK</div></div>;
            }}
        }}

        // ARAMA FİLTRESİ (Sadece Belediye Otobüslerinde Çalışır)
        document.getElementById('search-input').addEventListener('keyup', function(e) {{
            let text = e.target.value.toUpperCase();
            let items = document.querySelectorAll('.item-row');
            items.forEach(item => {{
                item.style.display = item.innerText.toUpperCase().includes(text) ? "flex" : "none";
            }});
        }});
    </script>
    </body>
    </html>
    """
