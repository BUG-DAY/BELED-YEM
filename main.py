# ==============================================================================
# PROJE       : T.C. ULUSAL ULAŞIM MATRİSİ (UUM)
# SÜRÜM       : v9.0.0-ZERO-ERROR-CORE (BÖLÜM 1)
# ==============================================================================

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI(title="Ulaşım Matrisi Core")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DataCore:
    def _init_(self):
        self.cities = {
            "Adana": [36.9914, 35.3308], "Ankara": [39.9334, 32.8597], "Antalya": [36.8841, 30.7056],
            "Bursa": [40.1824, 29.0611], "Diyarbakır": [37.9144, 40.2110], "Erzurum": [39.9000, 41.2700],
            "Eskişehir": [39.7767, 30.5206], "Gaziantep": [37.0662, 37.3833], "İstanbul": [41.0082, 28.9784],
            "İzmir": [38.4237, 27.1428], "Kayseri": [38.7312, 35.4787], "Kocaeli": [40.8533, 29.8815],
            "Konya": [37.8714, 32.4846], "Mersin": [36.8121, 34.6415]
        }
    
    def get_data(self, c: str):
        if c not in self.cities: c = "Adana"
        return {"lat": self.cities[c][0], "lng": self.cities[c][1], "lines": [f"Hat {random.randint(10,99)}", f"Hat {random.randint(100,500)}", "Ekspres"]}

db = DataCore()

# 500 Hatasını bitiren SAF VERİ MİMARİSİ
@app.get("/api/v1/fleet")
async def get_fleet(city: str = "Adana"):
    info = db.get_data(city)
    fleet = []
    tot_spd = 0
    
    for ln in info["lines"]:
        eta = random.randint(1, 15)
        spd = random.randint(10, 55) if eta > 1 else 0
        tot_spd += spd
        fleet.append({
            "id": ln, "hedef": f"Durak {random.randint(100,999)}", 
            "kalan": "DURAKTA" if eta == 1 else f"{eta} Dk",
            "lat": info["lat"] + random.uniform(-0.035, 0.035), 
            "lng": info["lng"] + random.uniform(-0.035, 0.035),
            "hiz": spd
        })
    
    # Dakikaya göre sıralama (DURAKTA olanlar en üste)
    fleet.sort(key=lambda x: 0 if x["kalan"] == "DURAKTA" else int(x["kalan"].split()[0]))
    
    return {
        "sehir": city, 
        "merkez": {"lat": info["lat"], "lng": info["lng"]}, 
        "arac_sayisi": len(fleet), 
        "ortalama_hiz": int(tot_spd / len(fleet)) if fleet else 0, 
        "filo": fleet
    }# ==============================================================================
# PROJE       : T.C. ULUSAL ULAŞIM MATRİSİ (UUM)
# SÜRÜM       : v9.0.0-ZERO-ERROR-CORE (BÖLÜM 1)
# ==============================================================================

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI(title="Ulaşım Matrisi Core")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DataCore:
    def _init_(self):
        self.cities = {
            "Adana": [36.9914, 35.3308], "Ankara": [39.9334, 32.8597], "Antalya": [36.8841, 30.7056],
            "Bursa": [40.1824, 29.0611], "Diyarbakır": [37.9144, 40.2110], "Erzurum": [39.9000, 41.2700],
            "Eskişehir": [39.7767, 30.5206], "Gaziantep": [37.0662, 37.3833], "İstanbul": [41.0082, 28.9784],
            "İzmir": [38.4237, 27.1428], "Kayseri": [38.7312, 35.4787], "Kocaeli": [40.8533, 29.8815],
            "Konya": [37.8714, 32.4846], "Mersin": [36.8121, 34.6415]
        }
    
    def get_data(self, c: str):
        if c not in self.cities: c = "Adana"
        return {"lat": self.cities[c][0], "lng": self.cities[c][1], "lines": [f"Hat {random.randint(10,99)}", f"Hat {random.randint(100,500)}", "Ekspres"]}

db = DataCore()

# 500 Hatasını bitiren SAF VERİ MİMARİSİ
@app.get("/api/v1/fleet")
async def get_fleet(city: str = "Adana"):
    info = db.get_data(city)
    fleet = []
    tot_spd = 0
    
    for ln in info["lines"]:
        eta = random.randint(1, 15)
        spd = random.randint(10, 55) if eta > 1 else 0
        tot_spd += spd
        fleet.append({
            "id": ln, "hedef": f"Durak {random.randint(100,999)}", 
            "kalan": "DURAKTA" if eta == 1 else f"{eta} Dk",
            "lat": info["lat"] + random.uniform(-0.035, 0.035), 
            "lng": info["lng"] + random.uniform(-0.035, 0.035),
            "hiz": spd
        })
    
    # Dakikaya göre sıralama (DURAKTA olanlar en üste)
    fleet.sort(key=lambda x: 0 if x["kalan"] == "DURAKTA" else int(x["kalan"].split()[0]))
    
    return {
        "sehir": city, 
        "merkez": {"lat": info["lat"], "lng": info["lng"]}, 
        "arac_sayisi": len(fleet), 
        "ortalama_hiz": int(tot_spd / len(fleet)) if fleet else 0, 
        "filo": fleet
    }# ==============================================================================
# PROJE       : T.C. ULUSAL ULAŞIM MATRİSİ (UUM)
# SÜRÜM       : v9.0.0-ZERO-ERROR-CORE (BÖLÜM 1)
# ==============================================================================

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI(title="Ulaşım Matrisi Core")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DataCore:
    def _init_(self):
        self.cities = {
            "Adana": [36.9914, 35.3308], "Ankara": [39.9334, 32.8597], "Antalya": [36.8841, 30.7056],
            "Bursa": [40.1824, 29.0611], "Diyarbakır": [37.9144, 40.2110], "Erzurum": [39.9000, 41.2700],
            "Eskişehir": [39.7767, 30.5206], "Gaziantep": [37.0662, 37.3833], "İstanbul": [41.0082, 28.9784],
            "İzmir": [38.4237, 27.1428], "Kayseri": [38.7312, 35.4787], "Kocaeli": [40.8533, 29.8815],
            "Konya": [37.8714, 32.4846], "Mersin": [36.8121, 34.6415]
        }
    
    def get_data(self, c: str):
        if c not in self.cities: c = "Adana"
        return {"lat": self.cities[c][0], "lng": self.cities[c][1], "lines": [f"Hat {random.randint(10,99)}", f"Hat {random.randint(100,500)}", "Ekspres"]}

db = DataCore()

# 500 Hatasını bitiren SAF VERİ MİMARİSİ
@app.get("/api/v1/fleet")
async def get_fleet(city: str = "Adana"):
    info = db.get_data(city)
    fleet = []
    tot_spd = 0
    
    for ln in info["lines"]:
        eta = random.randint(1, 15)
        spd = random.randint(10, 55) if eta > 1 else 0
        tot_spd += spd
        fleet.append({
            "id": ln, "hedef": f"Durak {random.randint(100,999)}", 
            "kalan": "DURAKTA" if eta == 1 else f"{eta} Dk",
            "lat": info["lat"] + random.uniform(-0.035, 0.035), 
            "lng": info["lng"] + random.uniform(-0.035, 0.035),
            "hiz": spd
        })
    
    # Dakikaya göre sıralama (DURAKTA olanlar en üste)
    fleet.sort(key=lambda x: 0 if x["kalan"] == "DURAKTA" else int(x["kalan"].split()[0]))
    
    return {
        "sehir": city, 
        "merkez": {"lat": info["lat"], "lng": info["lng"]}, 
        "arac_sayisi": len(fleet), 
        "ortalama_hiz": int(tot_spd / len(fleet)) if fleet else 0, 
        "filo": fleet
    }# ==============================================================================
# PROJE       : T.C. ULUSAL ULAŞIM MATRİSİ (UUM)
# SÜRÜM       : v9.0.0-ZERO-ERROR-CORE (BÖLÜM 1)
# ==============================================================================

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI(title="Ulaşım Matrisi Core")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DataCore:
    def _init_(self):
        self.cities = {
            "Adana": [36.9914, 35.3308], "Ankara": [39.9334, 32.8597], "Antalya": [36.8841, 30.7056],
            "Bursa": [40.1824, 29.0611], "Diyarbakır": [37.9144, 40.2110], "Erzurum": [39.9000, 41.2700],
            "Eskişehir": [39.7767, 30.5206], "Gaziantep": [37.0662, 37.3833], "İstanbul": [41.0082, 28.9784],
            "İzmir": [38.4237, 27.1428], "Kayseri": [38.7312, 35.4787], "Kocaeli": [40.8533, 29.8815],
            "Konya": [37.8714, 32.4846], "Mersin": [36.8121, 34.6415]
        }
    
    def get_data(self, c: str):
        if c not in self.cities: c = "Adana"
        return {"lat": self.cities[c][0], "lng": self.cities[c][1], "lines": [f"Hat {random.randint(10,99)}", f"Hat {random.randint(100,500)}", "Ekspres"]}

db = DataCore()

# 500 Hatasını bitiren SAF VERİ MİMARİSİ
@app.get("/api/v1/fleet")
async def get_fleet(city: str = "Adana"):
    info = db.get_data(city)
    fleet = []
    tot_spd = 0
    
    for ln in info["lines"]:
        eta = random.randint(1, 15)
        spd = random.randint(10, 55) if eta > 1 else 0
        tot_spd += spd
        fleet.append({
            "id": ln, "hedef": f"Durak {random.randint(100,999)}", 
            "kalan": "DURAKTA" if eta == 1 else f"{eta} Dk",
            "lat": info["lat"] + random.uniform(-0.035, 0.035), 
            "lng": info["lng"] + random.uniform(-0.035, 0.035),
            "hiz": spd
        })
    
    # Dakikaya göre sıralama (DURAKTA olanlar en üste)
    fleet.sort(key=lambda x: 0 if x["kalan"] == "DURAKTA" else int(x["kalan"].split()[0]))
    
    return {
        "sehir": city, 
        "merkez": {"lat": info["lat"], "lng": info["lng"]}, 
        "arac_sayisi": len(fleet), 
        "ortalama_hiz": int(tot_spd / len(fleet)) if fleet else 0, 
        "filo": fleet
    }# ==============================================================================
# HTML ŞABLONLARI (BÖLÜM 2)
# ==============================================================================

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
        <title>Ulaşım Matrisi</title>
        <style>
            * { box-sizing: border-box; font-family: 'Segoe UI', sans-serif; text-decoration: none; user-select: none; }
            body { background: #020617; height: 100vh; display: flex; align-items: center; justify-content: center; margin: 0; }
            .app { width: 100vw; height: 100vh; max-width: 450px; background: #f8fafc; display: flex; flex-direction: column; }
            @media (min-width: 460px) { .app { max-height: 850px; border-radius: 35px; border: 8px solid #1e293b; overflow: hidden; } }
            .dash { padding: 40px 25px; flex: 1; display: flex; flex-direction: column; }
            .title { font-size: 28px; font-weight: 900; color: #0f172a; line-height: 1.2; margin-bottom: 35px; }
            .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }
            .card { background: white; border-radius: 24px; padding: 30px 10px; text-align: center; box-shadow: 0 8px 20px rgba(0,0,0,0.04); display: flex; flex-direction: column; align-items: center; gap: 15px; }
            .card:active { transform: scale(0.95); background: #f1f5f9; }
            .ic { width: 70px; height: 70px; border-radius: 22px; display: flex; align-items: center; justify-content: center; font-size: 35px; }
            .lb { font-size: 15px; font-weight: 900; color: #0f172a; }
        </style>
    </head>
    <body>
        <div class="app">
            <div class="dash">
                <div class="title">Merhaba <span style="color:#2563eb;">Mehmet Tahir</span>,<br><div style="font-size:16px; color:#64748b; font-weight:600; margin-top:8px;">Hangi aracı kullanacaksın?</div></div>
                <div class="grid">
                    <a href="/belediye?city=Adana" class="card"><div class="ic" style="background:#dbeafe; color:#2563eb;">🚌</div><div class="lb">Belediye</div></a>
                    <a href="/metro" class="card"><div class="ic" style="background:#fce7f3; color:#db2777;">🚇</div><div class="lb">Metro</div></a>
                    <a href="/ozel" class="card"><div class="ic" style="background:#ffedd5; color:#ea580c;">🚐</div><div class="lb">Özel Sektör</div></a>
                    <a href="/kart" class="card"><div class="ic" style="background:#d1fae5; color:#10b981;">💳</div><div class="lb">Kart Dolum</div></a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

@app.get("/belediye", response_class=HTMLResponse)
async def belediye(city: str = "Adana"):
    opts = ""
    for c in sorted(db.cities.keys()):
        sel = "selected" if c == city else ""
        opts += f"<option value='{c}' {sel}>{c}</option>"
        
    html = """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
        <title>Canlı Filo</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <style>
            * { box-sizing: border-box; font-family: 'Segoe UI', sans-serif; text-decoration: none; }
            body { background: #020617; height: 100vh; display: flex; align-items: center; justify-content: center; margin: 0; }
            .app { width: 100vw; height: 100vh; max-width: 450px; background: #f8fafc; display: flex; flex-direction: column; position: relative; }
            @media (min-width: 460px) { .app { max-height: 850px; border-radius: 35px; border: 8px solid #1e293b; overflow: hidden; } }
            .led { background: #000; padding: 10px; border-bottom: 2px solid #2563eb; display: flex; align-items: center; }
            .tk-wrap { overflow: hidden; white-space: nowrap; flex: 1; }
            .tk-text { display: inline-block; color: #38bdf8; font-family: monospace; font-size: 13px; font-weight: bold; animation: scroll 20s linear infinite; }
            @keyframes scroll { from { transform: translateX(100%); } to { transform: translateX(-100%); } }
            .nav { background: #0f172a; padding: 15px; display: flex; align-items: center; justify-content: space-between; z-index: 2000; }
            .bck { color: white; font-weight: 900; padding: 8px 12px; background: #334155; border-radius: 8px; font-size: 13px; }
            .sel { background: #1e293b; color: white; border: 1px solid #38bdf8; padding: 8px 15px; border-radius: 8px; font-weight: bold; outline: none; }
            .map-box { flex: 0.6; width: 100%; position: relative; background: #e2e8f0; }
            #map { position: absolute; top: 0; bottom: 0; left: 0; right: 0; z-index: 1; }
            .drw { flex: 0.4; background: white; border-radius: 20px 20px 0 0; box-shadow: 0 -10px 20px rgba(0,0,0,0.1); z-index: 1000; display: flex; flex-direction: column; margin-top: -15px; }
            .src-box { padding: 15px 20px 10px; border-bottom: 1px solid #f1f5f9; }
            .src { width: 100%; padding: 10px 15px; border-radius: 10px; border: 2px solid #e2e8f0; font-size: 14px; font-weight: bold; outline: none; background: #f8fafc; }
            .list { padding: 0 20px 10px; overflow-y: auto; flex: 1; }
            .row { display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid #f1f5f9; }
            .info { display: flex; flex-direction: column; gap: 4px; }
            .id { font-size: 15px; font-weight: 900; color: #0f172a; }
            .dst { font-size: 11px; color: #64748b; font-weight: 600; }
            .eta { font-size: 12px; font-weight: 900; background: #dbeafe; padding: 6px 12px; border-radius: 10px; color: #2563eb; }
        </style>
    </head>
    <body>
        <div class="app">
            <div class="led"><div class="tk-wrap"><div class="tk-text" id="led">📡 SİSTEM BAŞLATILIYOR...</div></div></div>
            <div class="nav">
                <a href="/" class="bck">❮ GERİ</a>
                <select class="sel" onchange="location.href='/belediye?city=' + this.value">{{OPTS}}</select>
            </div>
            <div class="map-box"><div id="map"></div></div>
            <div class="drw">
                <div class="src-box"><input type="text" id="src" class="src" placeholder="🔍 Hat veya Durak Ara..."></div>
                <div class="list" id="fleet"><div style="text-align:center; padding:30px; color:#94a3b8; font-size:12px;">🔄 API Bağlantısı Kuruluyor...</div></div>
            </div>
        </div>
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <script>
            class UlasimEngine {
                constructor() {
                    this.map = null;
                    this.layer = L.layerGroup();
                    this.fetchData();
                    setInterval(() => this.fetchData(), 4000);
                    
                    document.getElementById('src').addEventListener('keyup', (e) => {
                        let val = e.target.value.toUpperCase();
                        document.querySelectorAll('.item').forEach(r => {
                            r.style.display = r.innerText.toUpperCase().includes(val) ? "flex" : "none";
                        });
                    });
                }
                async fetchData() {
                    try {
                        const res = await fetch('/api/v1/fleet?city={{CITY}}');
                        const data = await res.json();
                        
                        if (!this.map) {
                            this.map = L.map('map', { zoomControl: false }).setView([data.merkez.lat, data.merkez.lng], 13);
                            L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {maxZoom: 19}).addTo(this.map);
                            this.layer.addTo(this.map);
                            setTimeout(() => this.map.invalidateSize(), 100);
                        } else {
                            this.map.setView([data.merkez.lat, data.merkez.lng], 13);
                        }
                        
                        const cont = document.getElementById('fleet');
                        cont.innerHTML = '';
                        this.layer.clearLayers();
                        const icon = L.divIcon({ html: '<div style="background:#2563eb; width:22px; height:22px; border-radius:50%; border:2px solid #fff; display:flex; align-items:center; justify-content:center; color:white; font-size:10px; box-shadow:0 2px 5px rgba(0,0,0,0.3);">🚌</div>', className: 'm' });

                        data.filo.forEach(b => {
                            const bg = b.kalan === 'DURAKTA' ? 'background:#d1fae5; color:#059669;' : '';
                            cont.innerHTML += `
                                <div class="row item">
                                    <div class="info">
                                        <span class="id">🚌 ${b.id}</span>
                                        <span class="dst">Hedef: ${b.hedef} | Hız: ${b.hiz} km/s</span>
                                    </div>
                                    <div class="eta" style="${bg}">${b.kalan}</div>
                                </div>`;
                            L.marker([b.lat, b.lng], {icon: icon}).addTo(this.layer);
                        });
                        
                        const now = new Date().toLocaleTimeString('tr-TR');
                        const msg = 📡 CANLI BİLGİ: ${data.sehir.toUpperCase()} | ARAÇ: ${data.arac_sayisi} | ORT. HIZ: ${data.ortalama_hiz} KM/S | GÜNCELLEME: ${now} | DURUM: OPTİMAL...;
                        document.getElementById('led').innerText = msg + " \u00A0\u00A0\u00A0\u00A0 " + msg;
                    } catch (e) {
                        document.getElementById('led').innerText = "⚠️ BAĞLANTI HATASI...";
                    }
                }
            }
            document.addEventListener('DOMContentLoaded', () => { window.App = new UlasimEngine(); });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html.replace("{{OPTS}}", opts).replace("{{CITY}}", city))

@app.get("/{mod}", response_class=HTMLResponse)
async def mods(mod: str):
    if mod not in ["metro", "ozel", "kart"]: return "<a href='/'>Geri</a>"
    t = {"metro": "RAYLI SİSTEMLER", "ozel": "ÖZEL SEKTÖR", "kart": "KART DOLUM"}[mod]
    html = """
    <!DOCTYPE html><html lang="tr"><head><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { box-sizing: border-box; font-family: sans-serif; text-decoration: none; }
        body { background: #020617; height: 100vh; display: flex; align-items: center; justify-content: center; margin: 0; }
        .app { width: 100vw; height: 100vh; max-width: 450px; background: #f8fafc; display: flex; flex-direction: column; position:relative; }
        @media (min-width: 460px) { .app { max-height: 850px; border-radius: 35px; border: 8px solid #1e293b; overflow:hidden; } }
        .nav { background: #0f172a; padding: 15px; display: flex; align-items: center; justify-content: center; position: relative; }
        .bck { position: absolute; left: 15px; color: white; font-weight: bold; padding: 8px 12px; background: #334155; border-radius: 8px; font-size: 13px; }
        .msg { margin: auto; padding: 30px; text-align: center; color: #1e293b; font-weight: bold; font-size: 15px; border: 2px dashed #cbd5e1; border-radius: 15px; width: 80%; line-height:1.5; }
    </style></head><body><div class="app"><div class="nav"><a href="/" class="bck">❮ GERİ</a>
    <div style="color:white; font-weight:900;">{{T}}</div></div>
    <div class="msg">⚠️ Güvenli API Bağlantısı Bekleniyor...<br><br><span style="font-size:12px; color:#64748b;">Altyapı hazır. Entegrasyon sağlandığında aktifleşecektir.</span></div></div></body></html>
    """
    return HTMLResponse(content=html.replace("{{T}}", t))
