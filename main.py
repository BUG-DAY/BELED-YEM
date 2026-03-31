from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import datetime

app = FastAPI()

# ---------------------------------------------------------
# 1. ANA MENÜ (Sadece Menü - LED Yok - Harita Yok)
# ---------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def ana_ekran():
    return """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Ulaşım Matrisi | Ana Menü</title>
        <style>
            :root { --blue: #2563eb; --pink: #db2777; --orange: #ea580c; --green: #10b981; --dark: #0f172a; }
            * { box-sizing: border-box; font-family: 'Segoe UI', system-ui, sans-serif; margin: 0; padding: 0; user-select: none; }
            body { background: #000; height: 100vh; display: flex; align-items: center; justify-content: center; overflow: hidden; }
            
            .app-container { width: 100vw; height: 100vh; max-width: 450px; max-height: 850px; background: #f8fafc; display: flex; flex-direction: column; overflow: hidden; }
            @media (min-width: 460px) { .app-container { border-radius: 35px; border: 8px solid #1e293b; height: 92vh; } }
            
            .home-content { padding: 40px 25px; flex: 1; display: flex; flex-direction: column; }
            .welcome { font-size: 28px; font-weight: 900; color: var(--dark); line-height: 1.2; margin-bottom: 30px; }
            .welcome span { color: var(--blue); }
            .sub-welcome { font-size: 16px; color: #64748b; font-weight: 600; margin-top: 8px; }

            .menu-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }
            /* Gerçek link geçişleri için a etiketleri kullanıyoruz */
            .card {
                background: white; border-radius: 24px; padding: 30px 10px; text-align: center;
                box-shadow: 0 8px 20px rgba(0,0,0,0.06); cursor: pointer; text-decoration: none;
                display: flex; flex-direction: column; align-items: center; gap: 15px; border: 2px solid transparent;
            }
            .card:active { transform: scale(0.95); background: #f1f5f9; }
            .icon-circle { width: 70px; height: 70px; border-radius: 22px; display: flex; align-items: center; justify-content: center; font-size: 35px; }
            .card-label { font-size: 15px; font-weight: 900; color: var(--dark); }

            .c-belediye .icon-circle { background: #dbeafe; color: var(--blue); }
            .c-metro .icon-circle { background: #fce7f3; color: var(--pink); }
            .c-ozel .icon-circle { background: #ffedd5; color: var(--orange); }
            .c-kart .icon-circle { background: #d1fae5; color: var(--green); }
        </style>
    </head>
    <body>
        <div class="app-container">
            <div class="home-content">
                <div class="welcome">Merhaba <span>Mehmet Tahir</span>,<br><div class="sub-welcome">Bugün hangi aracı kullanacaksın?</div></div>
                <div class="menu-grid">
                    <a href="/belediye" class="card c-belediye"><div class="icon-circle">🚌</div><div class="card-label">Belediye</div></a>
                    <a href="/metro" class="card c-metro"><div class="icon-circle">🚇</div><div class="card-label">Metro</div></a>
                    <a href="/ozel" class="card c-ozel"><div class="icon-circle">🚐</div><div class="card-label">Özel Sektör</div></a>
                    <a href="/kart" class="card c-kart"><div class="icon-circle">💳</div><div class="card-label">Kart Dolum</div></a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

# ---------------------------------------------------------
# 2. BELEDİYE OTOBÜSÜ EKRANI (Ayrı Bir Sayfa - Harita ve LED Var)
# ---------------------------------------------------------
@app.get("/belediye", response_class=HTMLResponse)
async def belediye_ekrani():
    return """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Belediye Otobüsleri</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <style>
            :root { --blue: #2563eb; --dark: #0f172a; }
            * { box-sizing: border-box; font-family: 'Segoe UI', system-ui, sans-serif; margin: 0; padding: 0; text-decoration: none; }
            body { background: #000; height: 100vh; display: flex; align-items: center; justify-content: center; overflow: hidden; }
            .app-container { width: 100vw; height: 100vh; max-width: 450px; max-height: 850px; background: #f8fafc; display: flex; flex-direction: column; position: relative; overflow: hidden; }
            @media (min-width: 460px) { .app-container { border-radius: 35px; border: 8px solid #1e293b; height: 92vh; } }
            
            /* Üst Bar ve LED */
            .led-header { background: #000; padding: 10px; border-bottom: 2px solid var(--blue); }
            .ticker { overflow: hidden; white-space: nowrap; }
            .ticker-text { display: inline-block; color: #38bdf8; font-family: monospace; font-size: 13px; font-weight: bold; animation: scroll 15s linear infinite; }
            @keyframes scroll { from { transform: translateX(100%); } to { transform: translateX(-100%); } }
            
            .nav-bar { background: var(--dark); padding: 15px; display: flex; align-items: center; justify-content: center; position: relative; z-index: 2000; }
            .back-btn { position: absolute; left: 15px; color: white; font-weight: bold; padding: 6px 12px; background: #334155; border-radius: 8px; font-size: 13px; }
            .nav-title { color: white; font-weight: 900; font-size: 15px; letter-spacing: 1px; }

            /* Harita ve Liste (Moovit Mantığı) */
            .map-box { flex: 0.5; width: 100%; position: relative; background: #e2e8f0; }
            #map { position: absolute; top: 0; bottom: 0; left: 0; right: 0; z-index: 1; }
            
            .drawer { flex: 0.5; background: white; border-radius: 20px 20px 0 0; box-shadow: 0 -10px 20px rgba(0,0,0,0.1); z-index: 1000; display: flex; flex-direction: column; margin-top: -15px; }
            .search-box { padding: 15px 20px; }
            .search-input { width: 100%; padding: 12px 15px; border-radius: 12px; border: 2px solid #e2e8f0; font-size: 14px; font-weight: bold; outline: none; background: #f8fafc; color: var(--dark); }
            .drawer-content { padding: 0 20px 20px; overflow-y: auto; flex: 1; }
            
            .data-row { display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid #f1f5f9; }
            .data-info { display: flex; flex-direction: column; gap: 4px; }
            .data-id { font-size: 16px; font-weight: 900; color: var(--dark); }
            .data-dest { font-size: 11px; color: #64748b; font-weight: 600; display: flex; gap: 5px; align-items: center; }
            .data-val { font-size: 13px; font-weight: 900; background: #dbeafe; padding: 6px 12px; border-radius: 10px; color: var(--blue); }
        </style>
    </head>
    <body>
        <div class="app-container">
            <div class="led-header"><div class="ticker"><div class="ticker-text">📡 BELEDİYE OTOBÜSLERİ CANLI TAKİP SİSTEMİ | GPS AKTİF...</div></div></div>
            <div class="nav-bar">
                <a href="/" class="back-btn">❮ GERİ</a>
                <div class="nav-title">BELEDİYE OTOBÜSLERİ</div>
            </div>
            
            <div class="map-box"><div id="map"></div></div>
            
            <div class="drawer">
                <div class="search-box">
                    <input type="text" id="searchInput" class="search-input" placeholder="🔍 Hat Ara (Örn: 154)">
                </div>
                <div class="drawer-content">
                    <div class="data-row item"><div class="data-info"><span class="data-id">🚌 Hat 154</span><span class="data-dest">Hedef: Balcalı Hastanesi</span><span class="data-dest" style="color:#ea580c">📍 Şu an: Turgut Özal Blv.</span></div><div class="data-val">2 Dk</div></div>
                    <div class="data-row item"><div class="data-info"><span class="data-id">🚌 Hat 114</span><span class="data-dest">Hedef: Merkez Otogar</span><span class="data-dest" style="color:#ea580c">📍 Şu an: Baraj Yolu</span></div><div class="data-val">5 Dk</div></div>
                    <div class="data-row item"><div class="data-info"><span class="data-id">🚌 Hat 172</span><span class="data-dest">Hedef: Çukurova Üniv.</span><span class="data-dest" style="color:#ea580c">📍 Şu an: İstasyon Kavşağı</span></div><div class="data-val">9 Dk</div></div>
                </div>
            </div>
        </div>
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <script>
            var map = L.map('map', { zoomControl: false }).setView([36.9914, 35.3308], 13);
            L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', { maxZoom: 19 }).addTo(map);
            
            // Canlı Otobüs Simülasyonu
            const icon = L.divIcon({ html: <div style="background:#2563eb; width:22px; height:22px; border-radius:50%; border:2px solid #fff; display:flex; align-items:center; justify-content:center; color:white; font-size:10px;">🚌</div>, className: 'm' });
            let markers = [];
            for(let i=0; i<3; i++) { markers.push(L.marker([36.9914+(Math.random()-0.5)*0.03, 35.3308+(Math.random()-0.5)*0.03], {icon:icon}).addTo(map)); }
            setInterval(() => { markers.forEach(m => { let c = m.getLatLng(); m.setLatLng([c.lat+(Math.random()-0.5)*0.002, c.lng+(Math.random()-0.5)*0.002]); }); }, 1500);

            // Arama Motoru
            document.getElementById('searchInput').addEventListener('keyup', function(e) {
                let text = e.target.value.toUpperCase();
                let items = document.querySelectorAll('.item');
                items.forEach(item => { item.style.display = item.innerText.toUpperCase().includes(text) ? "flex" : "none"; });
            });
        </script>
    </body>
    </html>
    """

# ---------------------------------------------------------
# 3. METRO EKRANI (Ayrı Sayfa)
# ---------------------------------------------------------
@app.get("/metro", response_class=HTMLResponse)
async def metro_ekrani():
    return """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Metro Seferleri</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <style>
            :root { --pink: #db2777; --dark: #0f172a; }
            * { box-sizing: border-box; font-family: 'Segoe UI', system-ui, sans-serif; margin: 0; padding: 0; text-decoration: none; }
            body { background: #000; height: 100vh; display: flex; align-items: center; justify-content: center; overflow: hidden; }
            .app-container { width: 100vw; height: 100vh; max-width: 450px; max-height: 850px; background: #f8fafc; display: flex; flex-direction: column; position: relative; overflow: hidden; }
            @media (min-width: 460px) { .app-container { border-radius: 35px; border: 8px solid #1e293b; height: 92vh; } }
            
            .led-header { background: #000; padding: 10px; border-bottom: 2px solid var(--pink); }
            .ticker { overflow: hidden; white-space: nowrap; }
            .ticker-text { display: inline-block; color: #f472b6; font-family: monospace; font-size: 13px; font-weight: bold; animation: scroll 15s linear infinite; }
            @keyframes scroll { from { transform: translateX(100%); } to { transform: translateX(-100%); } }
            
            .nav-bar { background: var(--dark); padding: 15px; display: flex; align-items: center; justify-content: center; position: relative; z-index: 2000; }
            .back-btn { position: absolute; left: 15px; color: white; font-weight: bold; padding: 6px 12px; background: #334155; border-radius: 8px; font-size: 13px; }
            .nav-title { color: white; font-weight: 900; font-size: 15px; letter-spacing: 1px; }

            .map-box { flex: 0.5; width: 100%; position: relative; background: #e2e8f0; }
            #map { position: absolute; top: 0; bottom: 0; left: 0; right: 0; z-index: 1; }
            
            .drawer { flex: 0.5; background: white; border-radius: 20px 20px 0 0; box-shadow: 0 -10px 20px rgba(0,0,0,0.1); z-index: 1000; padding: 20px; overflow-y: auto; margin-top: -15px;}
            
            .data-row { display: flex; justify-content: space-between; align-items: center; padding: 15px 0; border-bottom: 1px solid #f1f5f9; }
            .data-info { display: flex; flex-direction: column; gap: 4px; }
            .data-id { font-size: 16px; font-weight: 900; color: var(--dark); }
            .data-dest { font-size: 11px; color: #64748b; font-weight: 600; }
            .data-val { font-size: 14px; font-weight: 900; background: #fce7f3; padding: 8px 15px; border-radius: 10px; color: var(--pink); }
        </style>
    </head>
    <body>
        <div class="app-container">
            <div class="led-header"><div class="ticker"><div class="ticker-text">🚇 METRO SEFERLERİ DAKİK İŞLİYOR | SONRAKİ TREN YAKLAŞIYOR...</div></div></div>
            <div class="nav-bar">
                <a href="/" class="back-btn">❮ GERİ</a>
                <div class="nav-title">METRO SAATLERİ</div>
            </div>
            <div class="map-box"><div id="map"></div></div>
            <div class="drawer">
                <div class="data-row"><div class="data-info"><span class="data-id">M1 - Hastane İstasyonu</span><span class="data-dest">Yön: Akıncılar</span></div><div class="data-val">14:30</div></div>
                <div class="data-row"><div class="data-info"><span class="data-id">M1 - Vilayet İstasyonu</span><span class="data-dest">Yön: Hastane</span></div><div class="data-val">14:38</div></div>
            </div>
        </div>
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <script>
            var map = L.map('map', { zoomControl: false }).setView([36.9914, 35.3308], 13);
            L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', { maxZoom: 19 }).addTo(map);
        </script>
    </body>
    </html>
    """

# ---------------------------------------------------------
# 4. ÖZEL SEKTÖR / KART DOLUM EKRANI
# ---------------------------------------------------------
@app.get("/{modul}", response_class=HTMLResponse)
async def diger_ekranlar(modul: str):
    if modul not in ["ozel", "kart"]: return "<a href='/'>Geri Dön</a>"
    
    baslik = "ÖZEL SEKTÖR" if modul == "ozel" else "KART DOLUM"
    metin = "⚠️ Özel Sektör API Entegrasyonu Bekleniyor..." if modul == "ozel" else "📍 Kentkart Merkez Gişe: 200m Mesafede"
    
    return f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {{ box-sizing: border-box; font-family: 'Segoe UI', sans-serif; text-decoration: none; }}
            body {{ background: #000; height: 100vh; display: flex; align-items: center; justify-content: center; margin: 0; }}
            .app-container {{ width: 100vw; height: 100vh; max-width: 450px; max-height: 850px; background: #f8fafc; display: flex; flex-direction: column; }}
            .nav-bar {{ background: #0f172a; padding: 15px; display: flex; align-items: center; justify-content: center; position: relative; }}
            .back-btn {{ position: absolute; left: 15px; color: white; font-weight: bold; padding: 6px 12px; background: #334155; border-radius: 8px; font-size: 13px; }}
            .content {{ padding: 30px; text-align: center; color: #1e293b; font-weight: bold; font-size: 16px; margin-top: 50px; border: 2px dashed #cbd5e1; border-radius: 15px; margin: 30px; }}
        </style>
    </head>
    <body>
        <div class="app-container">
            <div class="nav-bar">
                <a href="/" class="back-btn">❮ GERİ</a>
                <div style="color:white; font-weight:900;">{baslik}</div>
            </div>
            <div class="content">{metin}</div>
        </div>
    </body>
    </html>
    """
