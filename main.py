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
        <title>Belediyem - Modüler Sistem</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <style>
            * {{ box-sizing: border-box; font-family: 'Segoe UI', system-ui, sans-serif; margin: 0; padding: 0; user-select: none; }}
            body {{ background: #f1f5f9; height: 100vh; display: flex; align-items: center; justify-content: center; overflow: hidden; }}

            /* TELEFON ÇERÇEVESİ */
            .mobile-app {{
                width: 100vw; height: 100vh; max-width: 420px; max-height: 850px;
                background: #f8fafc; display: flex; flex-direction: column;
                position: relative; overflow: hidden;
            }}
            @media (min-width: 450px) {{ .mobile-app {{ border-radius: 30px; border: 8px solid #0f172a; box-shadow: 0 20px 50px rgba(0,0,0,0.3); height: 90vh; }} }}

            /* ÜST HEADER */
            .top-bar {{ background: #0f172a; padding: 15px; text-align: center; border-bottom: 3px solid #3b82f6; position: relative; z-index: 1000; }}
            .app-title {{ color: white; font-weight: 900; font-size: 16px; letter-spacing: 1px; }}
            .app-sub {{ color: #94a3b8; font-size: 11px; font-weight: bold; margin-top: 2px; }}
            .back-btn {{ position: absolute; left: 15px; top: 15px; color: white; font-weight: bold; font-size: 18px; cursor: pointer; display: none; }}

            /* --- 1. EKRAN: ANA MENÜ --- */
            #home-screen {{ flex: 1; padding: 20px; display: flex; flex-direction: column; gap: 15px; overflow-y: auto; }}
            .menu-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 10px; }}
            
            .menu-card {{
                background: white; border-radius: 20px; padding: 20px 10px; text-align: center;
                box-shadow: 0 10px 20px rgba(0,0,0,0.05); cursor: pointer; border: 2px solid transparent;
                transition: transform 0.2s, border-color 0.2s; display: flex; flex-direction: column; align-items: center; gap: 10px;
            }}
            .menu-card:active {{ transform: scale(0.95); }}
            
            .emoji-box {{ width: 60px; height: 60px; border-radius: 18px; display: flex; align-items: center; justify-content: center; font-size: 30px; }}
            .card-title {{ font-size: 13px; font-weight: 800; color: #1e293b; }}
            .card-sub {{ font-size: 10px; color: #64748b; font-weight: 600; }}

            /* Kart Renkleri */
            .card-belediye .emoji-box {{ background: #dbeafe; color: #2563eb; }} .card-belediye:hover {{ border-color: #3b82f6; }}
            .card-ozel .emoji-box {{ background: #ffedd5; color: #ea580c; }} .card-ozel:hover {{ border-color: #f97316; }}
            .card-metro .emoji-box {{ background: #fce7f3; color: #db2777; }} .card-metro:hover {{ border-color: #ec4899; }}
            .card-kart .emoji-box {{ background: #d1fae5; color: #059669; }} .card-kart:hover {{ border-color: #10b981; }}

            /* --- 2. EKRAN: HARİTA VE ALT PANEL --- */
            #map-screen {{ flex: 1; display: none; flex-direction: column; position: relative; }}
            .map-container {{ flex: 1; width: 100%; position: relative; background: #e2e8f0; }}
            #map {{ position: absolute; top: 0; bottom: 0; left: 0; right: 0; z-index: 1; }}

            /* ALTTAN ÇIKAN ZARİF BİLGİ PANELİ (Sağdaki koca panelin yerine) */
            .bottom-sheet {{
                position: absolute; bottom: 0; left: 0; right: 0; background: white;
                border-radius: 24px 24px 0 0; box-shadow: 0 -10px 30px rgba(0,0,0,0.1);
                z-index: 1000; display: flex; flex-direction: column; max-height: 45%;
                transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }}
            .sheet-handle {{ width: 40px; height: 5px; background: #cbd5e1; border-radius: 5px; margin: 10px auto; }}
            .sheet-header {{ padding: 0 20px 10px; font-weight: 900; color: #0f172a; font-size: 15px; border-bottom: 1px solid #f1f5f9; }}
            .sheet-content {{ padding: 10px 20px; overflow-y: auto; flex: 1; display: flex; flex-direction: column; gap: 10px; }}

            /* Liste Elemanları */
            .list-item {{ display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid #f8fafc; }}
            .item-left {{ display: flex; flex-direction: column; gap: 2px; }}
            .item-code {{ font-size: 14px; font-weight: 900; color: #1e293b; }}
            .item-desc {{ font-size: 11px; color: #64748b; font-weight: 600; }}
            .item-time {{ font-size: 13px; font-weight: 900; background: #f1f5f9; padding: 5px 10px; border-radius: 8px; color: #3b82f6; }}

            /* Anlaşma Bekleniyor Uyarısı */
            .alert-box {{ background: #fff7ed; border: 1px solid #fed7aa; padding: 15px; border-radius: 12px; text-align: center; margin-top: 20px; }}
            .alert-title {{ color: #ea580c; font-weight: 900; font-size: 14px; margin-bottom: 5px; }}
            .alert-sub {{ color: #9a3412; font-size: 12px; }}
        </style>
    </head>
    <body>

        <div class="mobile-app">
            
            <div class="top-bar">
                <div class="back-btn" id="backBtn" onclick="goHome()">❮</div>
                <div class="app-title">T.C. ULAŞIM MATRİSİ</div>
                <div class="app-sub" id="header-sub">MEHMET TAHİR | ADANA MERKEZ</div>
            </div>

            <div id="home-screen">
                <h2 style="font-size: 18px; color: #0f172a; margin-top: 5px;">Kategori Seçin</h2>
                <div class="menu-grid">
                    
                    <div class="menu-card card-belediye" onclick="openMap('belediye')">
                        <div class="emoji-box">🚌</div>
                        <div class="card-title">Belediye Otobüsü</div>
                        <div class="card-sub">Canlı GPS Takibi</div>
                    </div>

                    <div class="menu-card card-metro" onclick="openMap('metro')">
                        <div class="emoji-box">🚇</div>
                        <div class="card-title">Metro & Raylı</div>
                        <div class="card-sub">Sefer Saatleri</div>
                    </div>

                    <div class="menu-card card-ozel" onclick="openMap('ozel')">
                        <div class="emoji-box">🚐</div>
                        <div class="card-title">Özel Sektör</div>
                        <div class="card-sub">ÖHO & Dolmuş</div>
                    </div>

                    <div class="menu-card card-kart" onclick="openMap('kart')">
                        <div class="emoji-box">💳</div>
                        <div class="card-title">Kart Dolum</div>
                        <div class="card-sub">Akıllı Noktalar</div>
                    </div>

                </div>
            </div>

            <div id="map-screen">
                <div class="map-container">
                    <div id="map"></div>
                </div>
                
                <div class="bottom-sheet">
                    <div class="sheet-handle"></div>
                    <div class="sheet-header" id="sheet-title">Yükleniyor...</div>
                    <div class="sheet-content" id="sheet-data">
                        </div>
                </div>
            </div>

        </div>

        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <script>
            // Adana Odaklı Koordinatlar (Senin memleket)
            const center = [36.9914, 35.3308];
            let map;
            let markers = [];
            let moveInterval;

            // DOM Elementleri
            const homeScreen = document.getElementById('home-screen');
            const mapScreen = document.getElementById('map-screen');
            const backBtn = document.getElementById('backBtn');
            const sheetTitle = document.getElementById('sheet-title');
            const sheetData = document.getElementById('sheet-data');
            const headerSub = document.getElementById('header-sub');

            // --- HARİTA BAŞLATMA ---
            function initMap() {{
                if (!map) {{
                    map = L.map('map', {{ zoomControl: false }}).setView(center, 13);
                    L.tileLayer('https://{{s}}.basemaps.cartocdn.com/rastertiles/voyager/{{z}}/{{x}}/{{y}}{{r}}.png', {{
                        maxZoom: 19, attribution: '© OSMap'
                    }}).addTo(map);
                }}
            }}

            // --- SAYFA GEÇİŞLERİ ---
            function goHome() {{
                mapScreen.style.display = 'none';
                homeScreen.style.display = 'flex';
                backBtn.style.display = 'none';
                headerSub.innerText = "MEHMET TAHİR | ADANA MERKEZ";
                
                // Temizlik
                if(moveInterval) clearInterval(moveInterval);
                markers.forEach(m => map.removeLayer(m));
                markers = [];
            }}

            function openMap(type) {{
                homeScreen.style.display = 'none';
                mapScreen.style.display = 'flex';
                backBtn.style.display = 'block';
                
                initMap();
                // Haritanın gri kalmasını engellemek için SİHİRLİ KOD
                setTimeout(() => {{ map.invalidateSize(); }}, 100);

                loadData(type);
            }}

            // --- KATEGORİ VERİLERİNİ YÜKLEME ---
            function loadData(type) {{
                sheetData.innerHTML = ''; // Temizle
                
                if (type === 'belediye') {{
                    headerSub.innerText = "BELEDİYE OTOBÜSLERİ (CANLI)";
                    sheetTitle.innerText = "Yaklaşan Belediye Otobüsleri";
                    
                    const hatlar = [
                        {{kod: "154", rota: "Barajyolu - Terminal", sure: "2 Dk"}},
                        {{kod: "114", rota: "Turgut Özal - Balcalı", sure: "5 Dk"}},
                        {{kod: "172", rota: "Merkez - Hastane", sure: "8 Dk"}}
                    ];
                    
                    hatlar.forEach(h => {{
                        sheetData.innerHTML += `
                            <div class="list-item">
                                <div class="item-left">
                                    <div class="item-code">${{h.kod}}</div>
                                    <div class="item-desc">${{h.rota}}</div>
                                </div>
                                <div class="item-time" style="color:#2563eb; background:#dbeafe;">${{h.sure}}</div>
                            </div>
                        `;
                    }});

                    // Haritaya Canlı Mavi Otobüsler Ekle
                    const icon = L.divIcon({{ html: <div style="background:#2563eb; width:22px; height:22px; border-radius:50%; border:2px solid #fff; display:flex; align-items:center; justify-content:center; color:white; font-size:10px;">🚌</div>, className: 'dummy' }});
                    for(let i=0; i<3; i++) {{
                        let m = L.marker([center[0] + (Math.random()-0.5)*0.03, center[1] + (Math.random()-0.5)*0.03], {{icon: icon}}).addTo(map);
                        markers.push(m);
                    }}
                    moveInterval = setInterval(() => {{
                        markers.forEach(m => {{ let c = m.getLatLng(); m.setLatLng([c.lat + (Math.random()-0.5)*0.002, c.lng + (Math.random()-0.5)*0.002]); }});
                    }}, 1500);

                }} 
                else if (type === 'metro') {{
                    headerSub.innerText = "METRO VE RAYLI SİSTEM";
                    sheetTitle.innerText = "Adana Metro İstasyonları";
                    
                    const istasyonlar = [
                        {{isim: "Hastane", saat: "14:00, 14:15"}},
                        {{isim: "Anadolu Lisesi", saat: "14:05, 14:20"}},
                        {{isim: "Vilayet", saat: "14:12, 14:27"}},
                        {{isim: "Kocavezir", saat: "14:18, 14:33"}}
                    ];

                    istasyonlar.forEach(ist => {{
                        sheetData.innerHTML += `
                            <div class="list-item">
                                <div class="item-left">
                                    <div class="item-code">🚇 ${{ist.isim}} İstasyonu</div>
                                    <div class="item-desc">Sonraki Seferler</div>
                                </div>
                                <div class="item-time" style="color:#db2777; background:#fce7f3;">${{ist.saat}}</div>
                            </div>
                        `;
                    }});

                    // Haritaya Sabit Pembe İstasyonlar Ekle
                    const icon = L.divIcon({{ html: <div style="background:#db2777; width:16px; height:16px; border-radius:50%; border:2px solid #fff;"></div>, className: 'dummy' }});
                    for(let i=0; i<4; i++) {{
                        let m = L.marker([center[0] + (Math.random()-0.5)*0.03, center[1] + (Math.random()-0.5)*0.03], {{icon: icon}}).addTo(map);
                        markers.push(m);
                    }}
                }}
                else if (type === 'ozel') {{
                    headerSub.innerText = "ÖZEL HALK OTOBÜSLERİ";
                    sheetTitle.innerText = "Entegrasyon Bekleniyor";
                    
                    sheetData.innerHTML = `
                        <div class="alert-box">
                            <div class="alert-title">⚠️ ALTYAPI HAZIR</div>
                            <div class="alert-sub">Özel sektör kooperatifleri ile veri paylaşım anlaşması sağlandığında (API entegrasyonu), canlı takip sistemi anında aktifleşecektir.</div>
                        </div>
                    `;
                }}
                else if (type === 'kart') {{
                    headerSub.innerText = "KART DOLUM NOKTALARI";
                    sheetTitle.innerText = "Size En Yakın Noktalar";
                    
                    sheetData.innerHTML += `
                        <div class="list-item"><div class="item-left"><div class="item-code">📍 Merkez Gişe</div><div class="item-desc">200m mesafede</div></div></div>
                        <div class="list-item"><div class="item-left"><div class="item-code">🏪 Büfe Şirin</div><div class="item-desc">450m mesafede</div></div></div>
                    `;
                    
                    // Haritaya Sabit Yeşil Noktalar
                    const icon = L.divIcon({{ html: <div style="background:#10b981; width:16px; height:16px; border-radius:50%; border:2px solid #fff;"></div>, className: 'dummy' }});
                    for(let i=0; i<2; i++) {{
                        let m = L.marker([center[0] + (Math.random()-0.5)*0.01, center[1] + (Math.random()-0.5)*0.01], {{icon: icon}}).addTo(map);
                        markers.push(m);
                    }}
                }}
            }}
        </script>
    </body>
    </html>
    """
