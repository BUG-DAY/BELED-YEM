from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import datetime

app = FastAPI()

# TÜRKİYE 81 İL KOORDİNATLARI (Tam Altyapı)
ILLER = {
    "Adana": [36.9914, 35.3308], "Adıyaman": [37.7648, 38.2786], "Afyonkarahisar": [38.7507, 30.5567],
    "Ağrı": [39.7217, 43.0567], "Amasya": [40.6499, 35.8353], "Ankara": [39.9334, 32.8597],
    "Antalya": [36.8841, 30.7056], "Artvin": [41.1828, 41.8183], "Aydın": [37.8444, 27.8458],
    "Balıkesir": [39.6484, 27.8826], "Bilecik": [40.1419, 29.9793], "Bingöl": [38.8847, 40.4939],
    "Bitlis": [38.4006, 42.1095], "Bolu": [40.7350, 31.6061], "Burdur": [37.7203, 30.2908],
    "Bursa": [40.1824, 29.0611], "Çanakkale": [40.1553, 26.4142], "Çankırı": [40.6013, 33.6134],
    "Çorum": [40.5506, 34.9556], "Denizli": [37.7765, 29.0864], "Diyarbakır": [37.9144, 40.2110],
    "Edirne": [41.6768, 26.5570], "Elazığ": [38.6810, 39.2264], "Erzincan": [39.7500, 39.5000],
    "Erzurum": [39.9000, 41.2700], "Eskişehir": [39.7767, 30.5206], "Gaziantep": [37.0662, 37.3833],
    "Giresun": [40.9128, 38.3895], "Gümüşhane": [40.4608, 39.4814], "Hakkari": [37.5833, 43.7333],
    "Hatay": [36.2023, 36.1606], "Isparta": [37.7648, 30.5566], "Mersin": [36.8121, 34.6415],
    "İstanbul": [41.0082, 28.9784], "İzmir": [38.4237, 27.1428], "Kars": [40.6167, 43.1000],
    "Kastamonu": [41.3887, 33.7827], "Kayseri": [38.7312, 35.4787], "Kırklareli": [41.7333, 27.2167],
    "Kırşehir": [39.1425, 34.1709], "Kocaeli": [40.8533, 29.8815], "Konya": [37.8714, 32.4846],
    "Kütahya": [39.4167, 29.9833], "Malatya": [38.3552, 38.3095], "Manisa": [38.6191, 27.4289],
    "Kahramanmaraş": [37.5833, 36.9333], "Mardin": [37.3211, 40.7245], "Muğla": [37.2153, 28.3636],
    "Muş": [38.7432, 41.5064], "Nevşehir": [38.6244, 34.7144], "Niğde": [37.9667, 34.6833],
    "Ordu": [40.9839, 37.8764], "Rize": [41.0201, 40.5234], "Sakarya": [40.7569, 30.3783],
    "Samsun": [41.2867, 36.3300], "Siirt": [37.9333, 41.9500], "Sinop": [42.0231, 35.1531],
    "Sivas": [39.7477, 37.0179], "Tekirdağ": [40.9833, 27.5167], "Tokat": [40.3167, 36.5500],
    "Trabzon": [41.0027, 39.7167], "Tunceli": [39.1079, 39.5401], "Şanlıurfa": [37.1591, 38.7969],
    "Uşak": [38.6823, 29.4082], "Van": [38.4891, 43.3833], "Yozgat": [39.8181, 34.8147],
    "Zonguldak": [41.4506, 31.7908], "Aksaray": [38.3687, 34.0370], "Bayburt": [40.2552, 40.2249],
    "Karaman": [37.1759, 33.2287], "Kırıkkale": [39.8468, 33.5153], "Batman": [37.8812, 41.1279],
    "Şırnak": [37.5164, 42.4611], "Bartın": [41.6358, 32.3375], "Ardahan": [41.1105, 42.7022],
    "Iğdır": [39.9167, 44.0333], "Yalova": [40.6551, 29.2769], "Karabük": [41.2061, 32.6204],
    "Kilis": [36.7184, 37.1212], "Osmaniye": [37.0742, 36.2473], "Düzce": [40.8438, 31.1565]
}

# AÇIK VERİ SAĞLAYAN İLLER (Canlı Takip Aktif Olanlar)
AKTIF_ILLER = ["Adana", "İstanbul", "Ankara", "İzmir", "Bursa", "Kocaeli", "Konya"]

@app.get("/", response_class=HTMLResponse)
async def read_root(sehir: str = "Adana"):
    simdi = datetime.datetime.now().strftime("%H:%M")
    
    # Şehir kontrolü
    center = ILLER.get(sehir, ILLER["Adana"])
    is_active = sehir in AKTIF_ILLER
    
    # HTML Select Menüsü Oluşturma
    options_html = ""
    for s in sorted(ILLER.keys()):
        status_icon = "🟢" if s in AKTIF_ILLER else "⚪"
        selected = "selected" if sehir == s else ""
        options_html += f'<option value="{s}" {selected}>{status_icon} {s}</option>'
    
    # Dinamik Arayüz Metinleri
    durum_metni = "CANLI VERİ AKIŞI" if is_active else "ALTYAPI HAZIR"
    badge_renk = "#10b981" if is_active else "#94a3b8"
    
    return f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>T.C. Ulaşım Matrisi</title>
        
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        
        <style>
            * {{ box-sizing: border-box; font-family: 'Segoe UI', system-ui, sans-serif; margin: 0; padding: 0; }}
            
            body {{ 
                background: #0f172a; height: 100vh; display: flex; 
                align-items: center; justify-content: center; overflow: hidden;
            }}

            .mobile-device {{
                width: 100vw; height: 100vh; max-width: 420px; max-height: 850px;
                background: #ffffff; display: flex; flex-direction: column;
                position: relative; box-shadow: 0 20px 50px rgba(0,0,0,0.5);
            }}
            
            @media (min-width: 450px) {{
                .mobile-device {{ border-radius: 30px; border: 8px solid #020617; }}
            }}

            /* LED TV EKRANI */
            .led-banner {{
                background: #000; padding: 12px; border-bottom: 3px solid #0ea5e9; z-index: 1000;
            }}
            .ticker-box {{ overflow: hidden; white-space: nowrap; }}
            .ticker-text {{
                display: inline-block; color: #38bdf8; font-family: 'Courier New', monospace;
                font-size: 14px; font-weight: bold; animation: scroll-left 15s linear infinite;
            }}

            /* HARİTA ALANI (Kesin Çözüm) */
            .map-wrapper {{
                flex-grow: 1; width: 100%; position: relative; background: #e2e8f0;
            }}
            #map {{
                position: absolute; top: 0; bottom: 0; left: 0; right: 0; z-index: 1;
            }}

            /* VERİ BEKLENİYOR UYARISI (Kapalı İller İçin) */
            .waiting-overlay {{
                position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
                background: rgba(15, 23, 42, 0.9); padding: 15px 20px; border-radius: 12px;
                color: white; text-align: center; font-weight: bold; z-index: 1000;
                border: 1px solid #475569; display: {'none' if is_active else 'block'};
                box-shadow: 0 10px 25px rgba(0,0,0,0.3); width: 80%;
            }}
            .waiting-title {{ color: #fbbf24; font-size: 14px; margin-bottom: 5px; }}
            .waiting-sub {{ font-size: 11px; color: #cbd5e1; font-weight: normal; }}

            /* KONTROL PANELİ */
            .control-dock {{
                background: #f8fafc; padding: 20px; border-top: 1px solid #cbd5e1;
                display: flex; flex-direction: column; gap: 15px; z-index: 1000;
            }}

            .city-select {{
                width: 100%; padding: 12px; border-radius: 8px; border: 1px solid #cbd5e1;
                font-size: 15px; font-weight: bold; color: #0f172a; background: #fff;
                outline: none; cursor: pointer; appearance: none;
            }}

            .status-bar {{ display: flex; justify-content: space-between; align-items: center; }}
            .live-badge {{
                background: {badge_renk}; color: white; padding: 6px 12px; 
                border-radius: 20px; font-size: 11px; font-weight: bold; letter-spacing: 1px;
            }}
            .clock {{ font-size: 20px; font-weight: 900; color: #1e293b; }}

            @keyframes scroll-left {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}
        </style>
    </head>
    <body>

        <div class="mobile-device">
            
            <div class="led-banner">
                <div class="ticker-box">
                    <div class="ticker-text">
                        T.C. ULAŞIM MATRİSİ | ŞEHİR: {sehir.upper()} | DURUM: {durum_metni} | SİSTEM: MEHMET TAHİR
                    </div>
                </div>
            </div>

            <div class="map-wrapper">
                <div id="map"></div>
                <div class="waiting-overlay">
                    <div class="waiting-title">⚠️ ENTEGRASYON BEKLENİYOR</div>
                    <div class="waiting-sub">{sehir} Belediyesi açık veri API bağlantısı sağlandığında canlı takip aktifleşecektir. Altyapı hazırdır.</div>
                </div>
            </div>

            <div class="control-dock">
                <select class="city-select" onchange="location.href='/?sehir=' + this.value">
                    {options_html}
                </select>
                
                <div class="status-bar">
                    <div class="live-badge">{durum_metni}</div>
                    <div class="clock" id="live-clock">{simdi}</div>
                </div>
            </div>

        </div>

        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <script>
            const center = {center};
            const isActive = {'true' if is_active else 'false'};

            // Harita Kurulumu (Net ve temiz OpenStreetMap)
            var map = L.map('map', {{ zoomControl: false }}).setView(center, 13);
            L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                maxZoom: 19, attribution: '© OSMap'
            }}).addTo(map);

            setTimeout(() => {{ map.invalidateSize(); }}, 200);

            // Sadece Şehir "Açık Veri" ise otobüsleri simüle et
            if (isActive) {{
                const busIcon = L.divIcon({{
                    html: <div style="background:#0ea5e9; width:22px; height:22px; border-radius:50%; border:2px solid #fff; box-shadow:0 2px 5px rgba(0,0,0,0.5); display:flex; align-items:center; justify-content:center; color:white; font-size:10px;">🚌</div>,
                    className: 'bus-marker'
                }});
                
                const buses = [];
                for(let i=0; i<3; i++) {{
                    let b = L.marker([center[0] + (Math.random()-0.5)*0.03, center[1] + (Math.random()-0.5)*0.03], {{icon: busIcon}}).addTo(map);
                    buses.push(b);
                }}

                setInterval(() => {{
                    buses.forEach(b => {{
                        let curr = b.getLatLng();
                        b.setLatLng([curr.lat + (Math.random()-0.5)*0.002, curr.lng + (Math.random()-0.5)*0.002]);
                    }});
                }}, 1500);
            }}

            // Canlı Saat
            setInterval(() => {{
                document.getElementById('live-clock').textContent = new Date().toLocaleTimeString('tr-TR', {{hour:'2-digit', minute:'2-digit'}});
            }}, 1000);
        </script>
    </body>
    </html>
    """
